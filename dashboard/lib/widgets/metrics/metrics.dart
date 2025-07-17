import 'package:dashboard/models/event.dart';
import 'package:dashboard/shared/responsive_query.dart';
import 'package:flutter/material.dart';

class Metrics extends StatefulWidget {
  final Event latestEvent;

  const Metrics({Key? key, required this.latestEvent}) : super(key: key);

  @override
  State<Metrics> createState() => _MetricsState();
}

class _MetricsState extends State<Metrics> {
  final ScrollController _controller = ScrollController();
  late Map<String, String> latestTMPayload;
  late String logs;
  late String latestTMDatetime;

  @override
  void initState() {
    super.initState();
    logs = "";
    latestTMDatetime = "Unknown";
    latestTMPayload = {};
  }

  @override
  Widget build(BuildContext context) {
    _setValues();

    final isDesktop = ResponsiveQuery.isDesktop(context);
    final int columns = isDesktop ? 3 : 1;

    final properties = [
      _Property(property: "Lat", value: latestTMPayload['lat'] ?? "Unknown"),
      _Property(property: "Long", value: latestTMPayload['long'] ?? "Unknown"),
      _Property(property: "GPS Altitude", value: latestTMPayload['gps_altitude'] ?? "Unknown"),
      _Property(property: "Speed", value: latestTMPayload['speed'] ?? "Unknown"),
      _Property(property: "Last Connection", value: latestTMDatetime),
      _Property(property: "CPU Temp", value: latestTMPayload['cpuTemperature'] ?? "Unknown"),
      _Property(property: "Altitude", value: latestTMPayload['altitude'] ?? "Unknown"),
      _Property(property: "Pressure", value: latestTMPayload['pressure'] ?? "Unknown"),
      _Property(property: "Temperature", value: latestTMPayload['temperature'] ?? "Unknown"),
      _Property(property: "Yaw", value: latestTMPayload['yaw'] ?? "Unknown"),
      _Property(property: "Pitch", value: latestTMPayload['yaw'] ?? "Unknown"),
      _Property(property: "Roll", value: latestTMPayload['yaw'] ?? "Unknown"),
    ];

    return LayoutBuilder(
      builder: (context, constraints) {
        final double totalWidth = constraints.maxWidth;
        final double itemWidth = totalWidth / columns - 16;

        return SingleChildScrollView(
          child: Column(
            children: [
              SizedBox(
                width: double.infinity,
                child: Card(
                  margin: const EdgeInsets.only(bottom: 5),
                  child: Padding(
                    padding: const EdgeInsets.only(left: 5, top: 5),
                    child: Wrap(
                      spacing: 20,
                      runSpacing: 0,
                      children: properties
                          .map((prop) => SizedBox(width: itemWidth, child: prop))
                          .toList(),
                    ),
                  ),
                ),
              ),
              SizedBox(
                width: double.infinity,
                height: 220,
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: SingleChildScrollView(
                      controller: _controller,
                      scrollDirection: Axis.vertical,
                      child: Text(
                        logs,
                        style: const TextStyle(fontSize: 11.0),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  void _setValues() {
    logs += "${widget.latestEvent}\n\n";
    if (logs.length > 10000) {
      logs = logs.substring(5000);
    }
    if (_controller.hasClients) {
      _controller.animateTo(
        _controller.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }

    if (widget.latestEvent.isTm()) {
      setState(() {
        latestTMDatetime = widget.latestEvent.datetime;
        latestTMPayload = widget.latestEvent.payload ?? {};
      });
    }
  }
}
class _Property extends StatelessWidget {
  final String property;
  final String value;

  const _Property({Key? key, required this.property, required this.value}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          property,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
        ),
        Text(
          value,
          style: const TextStyle(fontSize: 13),
        ),
        const SizedBox(height: 6),
      ],
    );
  }
}

