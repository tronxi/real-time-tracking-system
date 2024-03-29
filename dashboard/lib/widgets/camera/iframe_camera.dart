import 'dart:html';
import 'dart:ui' as ui;

import 'package:flutter/material.dart';

class DeviceCamera extends StatefulWidget {
  final String url;
  const DeviceCamera({Key? key, required this.url}) : super(key: key);

  @override
  State<DeviceCamera> createState() => _DeviceCameraState();
}

class _DeviceCameraState extends State<DeviceCamera> {
  late IFrameElement _iframeElement;
  @override
  void initState() {
    _iframeElement = IFrameElement()
      ..src = widget.url
      ..id = 'iframe'
      ..style.border = 'none';
    ui.platformViewRegistry.registerViewFactory(
      'iframeElement',
      (int viewId) => _iframeElement,
    );
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return const SizedBox(
      height: 230,
      child: HtmlElementView(
        // key: UniqueKey(),
        viewType: 'iframeElement',
      ),
    );
  }
}
