package tronxi.dashboard_backend.producers;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Component;
import tronxi.dashboard_backend.models.Event;

@Component
@RequiredArgsConstructor
public class TrackingDeviceEventsProducer {

    private final SimpMessagingTemplate simpMessagingTemplate;
    private final ObjectMapper objectMapper;
    public void send(Event event) {
        try {
            String stringMessage = objectMapper.writeValueAsString(event);
            simpMessagingTemplate.convertAndSend("/topic/events", stringMessage);
        } catch (JsonProcessingException e) {
            System.out.println(e.getMessage());;
        }
    }
}
