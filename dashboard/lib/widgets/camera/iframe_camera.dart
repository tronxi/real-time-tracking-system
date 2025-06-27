import 'package:web/web.dart' as web;
import 'package:flutter/material.dart';
import 'web_view_registry.dart';

class DeviceCamera extends StatefulWidget {
  final String url;

  const DeviceCamera({Key? key, required this.url}) : super(key: key);

  @override
  State<DeviceCamera> createState() => _DeviceCameraState();
}

class _DeviceCameraState extends State<DeviceCamera> {
  late web.HTMLIFrameElement _iframeElement;

  @override
  void initState() {
    _iframeElement =
        web.document.createElement('iframe') as web.HTMLIFrameElement
          ..src = widget.url
          ..id = 'iframe'
          ..style.border = 'none'
          ..style.height = '100%'
          ..style.width = '100%';
    registerViewFactory('iframeElement', (int viewId) => _iframeElement);
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
