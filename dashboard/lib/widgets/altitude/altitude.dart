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
  final Map<String, List<FlSpot>> _seriesData = {};
  double _time = 0;

  @override
  Widget build(BuildContext context) {
    if (_seriesData.isEmpty || _seriesData.values.every((list) => list.isEmpty)) {
      return const Center(child: Text(""));
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildLegend(),
        const SizedBox(height: 8),
        Expanded(
          child: LineChart(
            LineChartData(
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
              lineBarsData: _seriesData.entries.map((entry) {
                return LineChartBarData(
                  spots: entry.value,
                  isCurved: true,
                  color: _colorForKey(entry.key),
                  barWidth: 2,
                  dotData: const FlDotData(show: false),
                  belowBarData: BarAreaData(show: false),
                );
              }).toList(),
            ),
          ),
        ),
      ],
    );
  }

  @override
  void didUpdateWidget(covariant Altitude oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.latestEvent != oldWidget.latestEvent &&
        widget.latestEvent.isTm()) {
      final payload = widget.latestEvent.payload;

      setState(() {
        payload?.forEach((key, value) {
          final doubleValue = double.tryParse(value.toString());
          if (doubleValue != null) {
            _seriesData.putIfAbsent(key, () => []);
            _seriesData[key]!.add(FlSpot(_time, doubleValue));
            if (_seriesData[key]!.length > 300) {
              _seriesData[key]!.removeAt(0);
            }
          }
        });
        _time += 2;
      });
    }
  }

  Color _colorForKey(String key) {
    final colors = [
      Colors.blue,
      Colors.red,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.brown,
      Colors.pink,
      Colors.teal,
    ];
    return colors[key.hashCode % colors.length];
  }

  Widget _buildLegend() {
    return Wrap(
      spacing: 12,
      runSpacing: 8,
      children: _seriesData.keys.map((key) {
        return Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 12,
              height: 12,
              color: _colorForKey(key),
            ),
            const SizedBox(width: 4),
            Text(key, style: const TextStyle(fontSize: 12)),
          ],
        );
      }).toList(),
    );
  }
}
