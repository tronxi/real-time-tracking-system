import 'package:dashboard/models/event.dart';
import 'package:flutter/material.dart';
import 'package:flutter_3d_controller/flutter_3d_controller.dart';
import 'dart:async';

class Attitude extends StatefulWidget {
  final Event latestEvent;

  const Attitude({super.key, required this.latestEvent});

  @override
  State<Attitude> createState() => _AttitudeState();
}

class _AttitudeState extends State<Attitude> {
  final Flutter3DController _controller = Flutter3DController();
  late Map<String, String> latestTMPayload;

  double yaw = 0;
  double pitch = 0;
  double roll = 0;
  Timer? _rotationTimer;
  bool _isModelLoaded = false;

  @override
  void initState() {
    super.initState();
    latestTMPayload = {};
  }

  @override
  void dispose() {
    _rotationTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    _setValues();
    return Center(
      child: Flutter3DViewer(
        controller: _controller,
        src: 'assets/cube.glb',
        enableTouch: true,
        progressBarColor: Colors.blue,
        onLoad: (String modelAddress) {
          _isModelLoaded = true;
        },
        onError: (String error) {
          debugPrint('3D model failed to load: $error');
        },
      ),
    );
  }

  void _setValues() {
    if (widget.latestEvent.isTm()) {
      latestTMPayload = widget.latestEvent.payload ?? {};
      final newYaw = double.tryParse(latestTMPayload['yaw']?.toString() ?? '') ?? 0.0;

      if (_isModelLoaded) {
        yaw = newYaw;
        pitch = 0;
        roll = 0;
        _controller.setCameraOrbit(
          newYaw,
          0,
          0
        );
      }
    }
  }
}
