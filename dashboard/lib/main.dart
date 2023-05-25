import 'package:dashboard/widgets/camera/camera.dart';
import 'package:dashboard/widgets/maps/map.dart';
import 'package:dashboard/widgets/metrics/metrics.dart';
import 'package:flutter/material.dart';
import 'package:split_view/split_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Rocket',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const Scaffold(
        body: Home(),
      ),
    );
  }
}

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SplitView(
      viewMode: SplitViewMode.Vertical,
      indicator: const SplitIndicator(viewMode: SplitViewMode.Vertical),
      activeIndicator: const SplitIndicator(
        viewMode: SplitViewMode.Vertical,
        isActive: true,
      ),
      gripSize: 5,
      children: const [_TopView(), _BottomView()],
    );
  }
}

class _TopView extends StatelessWidget {
  const _TopView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SplitView(
      viewMode: SplitViewMode.Horizontal,
      indicator: const SplitIndicator(viewMode: SplitViewMode.Horizontal),
      activeIndicator: const SplitIndicator(
        viewMode: SplitViewMode.Horizontal,
        isActive: true,
      ),
      gripSize: 5,
      children: [
        Metrics(),
        const Camera(url: 'https://tronxi.ddns.net/players/players/hlsjs.html')
      ],
    );
  }
}

class _BottomView extends StatelessWidget {
  const _BottomView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return const CustomMap();
  }
}
