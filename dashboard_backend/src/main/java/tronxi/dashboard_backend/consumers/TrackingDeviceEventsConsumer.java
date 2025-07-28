package tronxi.dashboard_backend.consumers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
import tronxi.dashboard_backend.models.Event;
import tronxi.dashboard_backend.persistence.jpa.EventJPA;
import tronxi.dashboard_backend.producers.TrackingDeviceEventsProducer;

import java.io.IOException;

import static tronxi.dashboard_backend.configuration.RabbitmqConfiguration.EVENTS_QUEUE;

@Component
@RequiredArgsConstructor
@RabbitListener(queues = EVENTS_QUEUE)
public class TrackingDeviceEventsConsumer {

    private final ObjectMapper objectMapper;
    private final TrackingDeviceEventsProducer trackingDeviceEventsProducer;

    private final EventJPA eventJPA;

    @RabbitHandler
    public void consume(byte[] eventBytes) {

        try {
            Event event = objectMapper.readValue(eventBytes, Event.class);
            trackingDeviceEventsProducer.send(event);
            eventJPA.save(event);
        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
