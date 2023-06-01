package tronxi.dashboard_backend.models;

import lombok.Data;

import java.util.Map;

@Data
public class Event {
    private String type;
    private String datetime;
    private Map<String, String> payload;
}
