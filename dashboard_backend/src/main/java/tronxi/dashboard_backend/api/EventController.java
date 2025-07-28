package tronxi.dashboard_backend.api;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import jakarta.annotation.Resource;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import tronxi.dashboard_backend.models.Event;
import tronxi.dashboard_backend.persistence.jpa.EventJPA;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequiredArgsConstructor
@RequestMapping("events")
public class EventController {

    private final EventJPA eventJPA;

    @GetMapping("/range")
    public ResponseEntity<List<Event>> retrieveByDateRange(
            @RequestParam("from") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime from,
            @RequestParam("to") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime to) {

        return ResponseEntity.ok(eventJPA.findByDatetimeBetween(from, to));
    }

    @GetMapping("/range/download")
    public ResponseEntity<ByteArrayResource> downloadByDateRange(
            @RequestParam("from") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime from,
            @RequestParam("to") @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime to) throws IOException {

        List<Event> events = eventJPA.findByDatetimeBetween(from, to);

        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        StringBuilder jsonlBuilder = new StringBuilder();
        for (Event event : events) {
            jsonlBuilder.append(objectMapper.writeValueAsString(event)).append("\n");
        }

        byte[] fileContent = jsonlBuilder.toString().getBytes(StandardCharsets.UTF_8);
        ByteArrayResource resource = new ByteArrayResource(fileContent);

        String filename = String.format("events_%s_to_%s.jsonl", from.toLocalDate(), to.toLocalDate());

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + filename)
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .contentLength(fileContent.length)
                .body(resource);
    }


    @GetMapping("/save")
    public ResponseEntity<Void> save() {
        Event event = new Event();
        event.setType("test");
        Map<String, String> payload = new HashMap<>();
        payload.put("test", "test");
        payload.put("test2", "test2");
        event.setPayload(payload);
        event.setDatetime(LocalDateTime.now());
        eventJPA.save(event);
        return ResponseEntity.ok().build();
    }

}
