package tronxi.dashboard_backend.models;

import jakarta.persistence.*;
import lombok.Data;
import tronxi.dashboard_backend.configuration.MapToJsonConverter;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Entity
@Table(name = "events")
@Data
public class Event {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String type;

    private LocalDateTime datetime;

    @Column(columnDefinition = "jsonb")
    @Convert(converter = MapToJsonConverter.class)
    private Map<String, String> payload = new HashMap<>();
}
