import 'package:flutter/material.dart';
import 'package:dashboard/widgets/camera/webview_camera.dart'
if (dart.library.html) 'package:dashboard/widgets/camera/iframe_camera.dart'
as camera;

class Camera extends StatelessWidget {
  final String url;

  const Camera({Key? key, required this.url}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return camera.DeviceCamera(url: url);
  }
}
