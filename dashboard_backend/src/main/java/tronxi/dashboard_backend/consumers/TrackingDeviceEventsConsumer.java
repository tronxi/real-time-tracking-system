package tronxi.dashboard_backend.consumers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.amqp.rabbit.annotation.RabbitHandler;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;
import tronxi.dashboard_backend.models.Event;

import java.io.IOException;

import static tronxi.dashboard_backend.configuration.RabbitmqConfiguration.EVENTS_QUEUE;

@Component
@RequiredArgsConstructor
@RabbitListener(queues = EVENTS_QUEUE)
public class TrackingDeviceEventsConsumer {

    private final ObjectMapper objectMapper;

    @RabbitHandler
    public void deletedUser(byte[] eventBytes) {

        try {
            Event event = objectMapper.readValue(eventBytes, Event.class);
            System.out.println(event);

        } catch (IOException e) {
            System.out.println(e.getMessage());
        }
    }
}
