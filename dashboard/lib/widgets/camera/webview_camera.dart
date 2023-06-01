import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class DeviceCamera extends StatefulWidget {
  final String url;
  const DeviceCamera({Key? key, required this.url}) : super(key: key);

  @override
  State<DeviceCamera> createState() => _DeviceCameraState();
}

class _DeviceCameraState extends State<DeviceCamera> {
  late WebViewController _webViewController;

  @override
  void initState() {
    _webViewController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setBackgroundColor(const Color(0x00000000))
      ..loadRequest(
          Uri.parse(widget.url));
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SizedBox(
        width: 400,
        height: 200,
        child: WebViewWidget(controller: _webViewController));
  }
}
