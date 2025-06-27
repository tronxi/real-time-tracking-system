import 'package:flutter/material.dart';
import 'package:flutter_3d_controller/flutter_3d_controller.dart';
import 'dart:async';

class Attitude extends StatefulWidget {
  const Attitude({super.key});

  @override
  State<Attitude> createState() => _AttitudeState();
}

class _AttitudeState extends State<Attitude> {
  final Flutter3DController _controller = Flutter3DController();

  double yaw = 0;
  double pitch = 0;
  double roll = 0;
  Timer? _rotationTimer;
  bool _isModelLoaded = false;

  void _startRotationLoop() {
    _rotationTimer = Timer.periodic(const Duration(milliseconds: 100), (_) {
      setState(() {
        yaw = (yaw + 1) % 360;
        pitch = (pitch + 0.5) % 360;
        roll = (roll + 0.3) % 360;

        if (_isModelLoaded) {
          _controller.setCameraOrbit(
            yaw,
            pitch,
            2.0,
          );
        }
      });
    });
  }

  @override
  void dispose() {
    _rotationTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Flutter3DViewer(
        controller: _controller,
        src: 'assets/cube.glb',
        enableTouch: true,
        progressBarColor: Colors.blue,
        onLoad: (String modelAddress) {
          _isModelLoaded = true;
          // _startRotationLoop();
        },
        onError: (String error) {
          debugPrint('3D model failed to load: $error');
        },
      ),
    );
  }
}
