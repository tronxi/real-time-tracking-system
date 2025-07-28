package tronxi.dashboard_backend.persistence.jpa;

import org.springframework.data.jpa.repository.JpaRepository;
import tronxi.dashboard_backend.models.Event;

import java.util.List;

public interface EventJPA extends JpaRepository<Event, Long> {
    List<Event> findByDatetimeBetween(java.time.LocalDateTime from, java.time.LocalDateTime to);
}