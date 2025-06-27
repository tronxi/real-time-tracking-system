import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:dashboard/models/event.dart';

class Altitude extends StatefulWidget {
  final Event latestEvent;

  const Altitude({super.key, required this.latestEvent});

  @override
  State<Altitude> createState() => _AltitudeState();
}

class _AltitudeState extends State<Altitude> {
  final List<FlSpot> _altitudePoints = [];
  double _time = 0;

  @override
  Widget build(BuildContext context) {
    if (_altitudePoints.isEmpty) {
      return const Center(child: Text(""));
    }
    return SizedBox(
      height: 250,
      child: LineChart(
        LineChartData(
          minY: 500,
          maxY: 600,
          lineTouchData: const LineTouchData(enabled: true),
          gridData: const FlGridData(show: true),
          borderData: FlBorderData(show: true),
          titlesData: FlTitlesData(
            bottomTitles: AxisTitles(
              axisNameWidget: const Text('Time (s)'),
              sideTitles: SideTitles(
                interval: 1,
                getTitlesWidget: (v, _) => Text('${v.toInt()}s'),
              ),
            ),
            leftTitles: AxisTitles(
              axisNameWidget: const Text('Altitude (m)'),
              sideTitles: SideTitles(
                interval: 2,
                getTitlesWidget: (v, _) => Text(v.toStringAsFixed(0)),
              ),
            ),
          ),
          lineBarsData: [
            LineChartBarData(
              spots: _altitudePoints,
              isCurved: true,
              color: Colors.blue,
              barWidth: 2,
              dotData: const FlDotData(show: false),
              belowBarData: BarAreaData(show: true),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void didUpdateWidget(covariant Altitude oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.latestEvent != oldWidget.latestEvent &&
        widget.latestEvent.isAltitude()) {
      final payload = widget.latestEvent.payload;
      final altitudeStr = payload?['altitude'];
      final altitude = double.tryParse(altitudeStr ?? '');

      if (altitude != null) {
        setState(() {
          _altitudePoints.add(FlSpot(_time, altitude));
          _time += 2;

          if (_altitudePoints.length > 300) {
            _altitudePoints.removeAt(0);
          }
        });
      }
    }
  }
}
