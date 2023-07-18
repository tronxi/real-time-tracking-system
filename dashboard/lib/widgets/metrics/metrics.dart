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
  late Map<String, String> latestHeartbeatPayload;
  late String logs;
  late String latestDatetime;

  @override
  void initState() {
    logs = "";
    latestDatetime = "Unknown";
    latestLocationPayload = <String, String>{};
    latestHeartbeatPayload = <String, String>{};
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    _setValues();
    return Container(
      color: Colors.white70,
      padding: const EdgeInsets.all(10),
      child: Stack(children: [
        Wrap(
          direction: Axis.vertical,
          alignment: WrapAlignment.start,
          runAlignment: WrapAlignment.start,
          runSpacing: 20,
          children: [
            _Property(
                property: "Lat",
                value: latestLocationPayload['lat'] ?? "Unknown"),
            _Property(
                property: "Long",
                value: latestLocationPayload['long'] ?? "Unknown"),
            _Property(
                property: "Altura",
                value: latestLocationPayload['altitude'] ?? "Unknown"),
            _Property(
                property: "Velocidad",
                value: latestLocationPayload['speed'] ?? "Unknown"),
            _Property(property: "Ultima conexión", value: latestDatetime),
            _Property(
                property: "Cpu Temperature",
                value: latestHeartbeatPayload['cpuTemperature'] ?? "Unknown"),
            SizedBox(
              width: ResponsiveQuery.isDesktop(context) ? 640 : 380,
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
              )),
            )
          ],
        ),
        Positioned(
            bottom: 10,
            right: 10,
            child: CircleAvatar(
              radius: 20,
              backgroundColor: Colors.redAccent,
              child: SizedBox(
                width: 40,
                height: 40,
                child: IconButton(
                  icon: const Icon(
                    Icons.rocket_launch,
                    color: Colors.white,
                  ),
                  onPressed: () {},
                ),
              ),
            ))
      ]),
    );
  }

  void _setValues() {
    logs += "${widget.latestEvent}\n\n";
    if (logs.length > 10000) {
      logs = logs.substring(5000, logs.length - 1);
      _controller.jumpTo(_controller.position.maxScrollExtent);
    }
    if (_controller.positions.isNotEmpty) {
      _controller.animateTo(
        _controller.position.maxScrollExtent,
        duration: const Duration(seconds: 1),
        curve: Curves.fastOutSlowIn,
      );
    }
    if (widget.latestEvent.isPosition()) {
      setState(() {
        latestLocationPayload = widget.latestEvent.payload!;
      });
    } else if (widget.latestEvent.isHeartBeat()) {
      setState(() {
        latestDatetime = widget.latestEvent.datetime;
        latestHeartbeatPayload = widget.latestEvent.payload!;
      });
    }
  }
}

class _Property extends StatelessWidget {
  final String property;
  final String value;
  const _Property({Key? key, required this.property, required this.value})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          "$property: ",
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
        ),
        Text(value, style: const TextStyle(fontSize: 18))
      ],
    );
  }
}
