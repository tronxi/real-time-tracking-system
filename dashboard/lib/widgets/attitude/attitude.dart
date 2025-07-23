import 'package:dashboard/models/event.dart';
import 'package:flutter/material.dart';
import 'package:three_js/three_js.dart' as three;
import 'package:three_js_math/three_js_math.dart' as tmath;

class Attitude extends StatefulWidget {
  final Event latestEvent;

  const Attitude({super.key, required this.latestEvent});

  @override
  State<Attitude> createState() => _AttitudeState();
}

class _AttitudeState extends State<Attitude> {
  late three.ThreeJS threeJs;
  three.Object3D? model;

  @override
  void initState() {
    super.initState();
    threeJs = three.ThreeJS(
      setup: _setupScene,
      onSetupComplete: () => setState(() {}),
      settings: three.Settings(useOpenGL: true),
    );
  }

  Future<void> _setupScene() async {
    threeJs.scene = three.Scene();
    threeJs.camera =
        three.PerspectiveCamera(60, threeJs.width / threeJs.height, 0.1, 1000);
    threeJs.camera.position.setValues(0, 0, 5);
    final directionalLight = three.DirectionalLight(0xffffff, 1);
    directionalLight.position.setValues(5, 5, 5);
    threeJs.scene.add(directionalLight);

    final ambientLight = three.AmbientLight(0xffffff, 0.4);
    threeJs.scene.add(ambientLight);

    final loader = three.GLTFLoader(flipY: false).setPath('assets/');
    final result = await loader.fromAsset('cube.glb');
    model = result!.scene.children.first;
    threeJs.scene.add(result.scene);

    threeJs.addAnimationEvent((dt) {
      if (model != null) {
        final payload = widget.latestEvent.payload ?? {};
        final newYaw = double.tryParse(payload['yaw']?.toString() ?? '') ?? 0.0;
        final newPitch =
            double.tryParse(payload['pitch']?.toString() ?? '') ?? 0.0;
        final newRoll =
            double.tryParse(payload['roll']?.toString() ?? '') ?? 0.0;
        // model!.rotation.set(
        //   tmath.MathUtils.degToRad(newPitch),
        //   tmath.MathUtils.degToRad(newYaw),
        //   tmath.MathUtils.degToRad(newRoll),
        // );
        model!.rotation.x = tmath.MathUtils.degToRad(newPitch);
        model!.rotation.y = tmath.MathUtils.degToRad(newRoll);
        model!.rotation.z = tmath.MathUtils.degToRad(newYaw);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return threeJs.build();
  }
}
