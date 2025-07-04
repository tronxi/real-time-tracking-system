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
  late Map<String, String> latestLocationPayload;
  late Map<String, String> latestAltitudePayload;
  late String logs;
  late String latestAltitudeDatetime;
  late String latestGPSDatetime;

  @override
  void initState() {
    super.initState();
    logs = "";
    latestAltitudeDatetime = "Unknown";
    latestGPSDatetime = "Unknown";
    latestLocationPayload = {};
    latestAltitudePayload = {};
  }

  @override
  Widget build(BuildContext context) {
    _setValues();

    final isDesktop = ResponsiveQuery.isDesktop(context);
    final int columns = isDesktop ? 3 : 1;

    final properties = [
      _Property(property: "Lat", value: latestLocationPayload['lat'] ?? "Unknown"),
      _Property(property: "Long", value: latestLocationPayload['long'] ?? "Unknown"),
      _Property(property: "GPS Altitude", value: latestLocationPayload['altitude'] ?? "Unknown"),
      _Property(property: "Speed", value: latestLocationPayload['speed'] ?? "Unknown"),
      _Property(property: "Last GPS Connection", value: latestGPSDatetime),
      _Property(property: "Last Altitude Connection", value: latestAltitudeDatetime),
      _Property(property: "CPU Temp", value: latestAltitudePayload['cpuTemperature'] ?? "Unknown"),
      _Property(property: "Altitude", value: latestAltitudePayload['altitude'] ?? "Unknown"),
      _Property(property: "Pressure", value: latestAltitudePayload['pressure'] ?? "Unknown"),
      _Property(property: "Temperature", value: latestAltitudePayload['temperature'] ?? "Unknown"),
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

    if (widget.latestEvent.isPosition()) {
      setState(() {
        latestGPSDatetime = widget.latestEvent.datetime;
        latestLocationPayload = widget.latestEvent.payload ?? {};
      });
    } else if (widget.latestEvent.isAltitude()) {
      setState(() {
        latestAltitudeDatetime = widget.latestEvent.datetime;
        latestAltitudePayload = widget.latestEvent.payload ?? {};
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

