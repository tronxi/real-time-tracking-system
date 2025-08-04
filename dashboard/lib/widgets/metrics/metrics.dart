import 'package:dashboard/models/event.dart';
import 'package:dashboard/shared/responsive_query.dart';
import 'package:flutter/material.dart';
import 'package:flutter_cupertino_datetime_picker/flutter_cupertino_datetime_picker.dart';
import 'package:web/web.dart' as web;
import 'package:flutter_dotenv/flutter_dotenv.dart';

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
    final isDesktop = ResponsiveQuery.isDesktop(context);
    final int columns = isDesktop ? 3 : 1;

    final properties = [
      _Property(property: "Lat", value: latestTMPayload['lat'] ?? "Unknown"),
      _Property(property: "Long", value: latestTMPayload['long'] ?? "Unknown"),
      _Property(
          property: "GPS Altitude",
          value: latestTMPayload['gps_altitude'] ?? "Unknown"),
      _Property(
          property: "Speed", value: latestTMPayload['speed'] ?? "Unknown"),
      _Property(property: "Last Connection", value: latestTMDatetime),
      _Property(
          property: "CPU Temp",
          value: latestTMPayload['cpuTemperature'] ?? "Unknown"),
      _Property(
          property: "Altitude",
          value: latestTMPayload['altitude'] ?? "Unknown"),
      _Property(
          property: "Pressure",
          value: latestTMPayload['pressure'] ?? "Unknown"),
      _Property(
          property: "Temperature",
          value: latestTMPayload['temperature'] ?? "Unknown"),
      _Property(
          property: "Pitch", value: latestTMPayload['pitch'] ?? "Unknown"),
      _Property(property: "Roll", value: latestTMPayload['roll'] ?? "Unknown"),
      _Property(property: "Yaw", value: latestTMPayload['yaw'] ?? "Unknown"),
    ];

    return LayoutBuilder(
      builder: (context, constraints) {
        final double totalWidth = constraints.maxWidth;
        final double itemWidth = totalWidth / columns - 16;

        return Stack(children: [
          SingleChildScrollView(
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
                            .map((prop) =>
                                SizedBox(width: itemWidth, child: prop))
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
          ),
          Positioned(
            top: 10,
            right: 10,
            child: ElevatedButton.icon(
              onPressed: () => _showDownloadDialog(context),
              icon: const Icon(Icons.download),
              label: const Text("Download"),
              style: ElevatedButton.styleFrom(
                padding:
                    const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
              ),
            ),
          ),
        ]);
      },
    );
  }

  Future<void> _showDownloadDialog(BuildContext context) async {
    DateTime? fromDate;
    DateTime? toDate;

    await showDialog(
      context: context,
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setState) {
            return AlertDialog(
              title: const Text("Select Date Range"),
              content: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  ElevatedButton(
                    onPressed: () {
                      DatePicker.showDatePicker(
                        context,
                        pickerTheme: const DateTimePickerTheme(
                          backgroundColor: Colors.black,
                          itemTextStyle:
                              TextStyle(color: Colors.blue, fontSize: 18),
                          cancel: Text("Cancel",
                              style: TextStyle(color: Colors.red)),
                          confirm:
                              Text("OK", style: TextStyle(color: Colors.blue)),
                        ),
                        dateFormat: 'yyyy-MM-dd HH:mm:ss',
                        initialDateTime:
                            DateTime.now().subtract(const Duration(days: 1)),
                        minDateTime: DateTime(2020),
                        maxDateTime: DateTime(2100),
                        onConfirm: (dt, _) => setState(() => fromDate = dt),
                      );
                    },
                    child: Text(fromDate == null
                        ? "Pick Start Date"
                        : "From: ${fromDate!.toIso8601String()}"),
                  ),
                  const SizedBox(height: 10),
                  ElevatedButton(
                    onPressed: () {
                      DatePicker.showDatePicker(
                        context,
                        pickerTheme: const DateTimePickerTheme(
                          backgroundColor: Colors.black,
                          itemTextStyle:
                              TextStyle(color: Colors.blue, fontSize: 18),
                          cancel: Text("Cancel",
                              style: TextStyle(color: Colors.red)),
                          confirm:
                              Text("OK", style: TextStyle(color: Colors.blue)),
                        ),
                        dateFormat: 'yyyy-MM-dd HH:mm:ss',
                        initialDateTime: DateTime.now(),
                        minDateTime: DateTime(2020),
                        maxDateTime: DateTime(2100),
                        onConfirm: (dt, _) => setState(() => toDate = dt),
                      );
                    },
                    child: Text(toDate == null
                        ? "Pick End Date"
                        : "To: ${toDate!.toIso8601String()}"),
                  ),
                ],
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text("Cancel"),
                ),
                ElevatedButton(
                  onPressed: fromDate != null && toDate != null
                      ? () {
                          _downloadJsonlFromUrl(fromDate!, toDate!);
                          Navigator.pop(ctx);
                        }
                      : null,
                  child: const Text("Download"),
                ),
              ],
            );
          },
        );
      },
    );
  }

  void _downloadJsonlFromUrl(DateTime from, DateTime to) {
    final fromStr = from.toIso8601String();
    final toStr = to.toIso8601String();
    final url =
    '${dotenv.env['DOWNLOAD_URL']!}/events/range/download?from=$fromStr&to=$toStr';

    final anchor = web.document.createElement('a') as web.HTMLAnchorElement;
    anchor.href = url;
    anchor.download = 'events_$fromStr\_$toStr.jsonl';
    anchor.style.display = 'none';
    web.document.body!.appendChild(anchor);
    anchor.click();
    anchor.remove();
  }

  @override
  void didUpdateWidget(covariant Metrics oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.latestEvent != oldWidget.latestEvent) {
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
}

class _Property extends StatelessWidget {
  final String property;
  final String value;

  const _Property({Key? key, required this.property, required this.value})
      : super(key: key);

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
