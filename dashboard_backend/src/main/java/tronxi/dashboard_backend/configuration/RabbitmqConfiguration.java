package tronxi.dashboard_backend.configuration;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.Declarables;
import org.springframework.amqp.core.FanoutExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitmqConfiguration {

    public static final String EVENTS_QUEUE = "tracking_device_events.dashboard_backend";
    public static final String EVENTS_EXCHANGE = "tracking_device_events";

    @Bean
    public Declarables createRabbitmqSchema() {
        return new Declarables(
                new FanoutExchange(EVENTS_EXCHANGE, false, false, null),
                new Queue(EVENTS_QUEUE),
                new Binding(EVENTS_QUEUE, Binding.DestinationType.QUEUE, EVENTS_EXCHANGE, "", null)
        );
    }
}