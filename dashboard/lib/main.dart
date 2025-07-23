import 'package:dashboard/bloc/events_bloc.dart';
import 'package:dashboard/models/event.dart';
import 'package:dashboard/shared/responsive_query.dart';
import 'package:dashboard/widgets/altitude/altitude.dart';
import 'package:dashboard/widgets/attitude/attitude.dart';
import 'package:dashboard/widgets/camera/camera.dart';
import 'package:dashboard/widgets/maps/map.dart';
import 'package:dashboard/widgets/metrics/metrics.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:split_view/split_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Real Time Tracking System Dashboard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.blue, brightness: Brightness.dark),
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
    return BlocProvider<TrackingDeviceEventBloc>(
        create: (BuildContext context) => TrackingDeviceEventBloc(),
        child: const _HomeBuilder());
  }
}

class _HomeBuilder extends StatelessWidget {
  const _HomeBuilder({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<TrackingDeviceEventBloc, Event>(
        builder: (context, state) {
      return Scaffold(
          body: ResponsiveQuery.isDesktop(context)
              ? _DashboardView(latestEvent: state)
              : _DashboardViewMobile(latestEvent: state));
    });
  }
}

class _DashboardViewMobile extends StatelessWidget {
  final Event latestEvent;

  const _DashboardViewMobile({Key? key, required this.latestEvent})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          Metrics(latestEvent: latestEvent),
          const SizedBox(height: 40),
          SizedBox(height: 300, child: Attitude(latestEvent: latestEvent)),
          const SizedBox(height: 40),
          Altitude(latestEvent: latestEvent),
          const SizedBox(height: 40),
          SizedBox(height: 300, child: CustomMap(latestEvent: latestEvent)),
          const SizedBox(height: 40),
          const Camera(
              url: 'https://tronxi.ddns.net/players/players/hlsjs.html'),
        ],
      ),
    );
  }
}

class _DashboardView extends StatelessWidget {
  final Event latestEvent;

  const _DashboardView({Key? key, required this.latestEvent}) : super(key: key);

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
      children: [
        _TopView(latestEvent: latestEvent),
        _BottomView(latestEvent: latestEvent)
      ],
    );
  }
}

class _TopView extends StatefulWidget {
  final Event latestEvent;

  const _TopView({Key? key, required this.latestEvent}) : super(key: key);

  @override
  State<_TopView> createState() => _TopViewState();
}

class _TopViewState extends State<_TopView> {
  late SplitViewController _controller;

  @override
  void initState() {
    _controller = SplitViewController(weights: [0.5, 0.5]);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SplitView(
      controller: _controller,
      viewMode: SplitViewMode.Horizontal,
      indicator: const SplitIndicator(viewMode: SplitViewMode.Horizontal),
      activeIndicator: const SplitIndicator(
        viewMode: SplitViewMode.Horizontal,
        isActive: true,
      ),
      gripSize: 5,
      children: [
        Metrics(latestEvent: widget.latestEvent),
        const Camera(url: 'https://tronxi.ddns.net/players/players/hlsjs.html')
      ],
    );
  }
}

class _BottomView extends StatefulWidget {
  final Event latestEvent;

  const _BottomView({Key? key, required this.latestEvent}) : super(key: key);

  @override
  State<_BottomView> createState() => _BottomViewState();
}

class _BottomViewState extends State<_BottomView> {
  late SplitViewController _controller;

  @override
  void initState() {
    _controller = SplitViewController(weights: [0.2, 0.6, 0.2]);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SplitView(
      viewMode: SplitViewMode.Horizontal,
      controller: _controller,
      indicator: const SplitIndicator(viewMode: SplitViewMode.Horizontal),
      activeIndicator: const SplitIndicator(
        viewMode: SplitViewMode.Horizontal,
        isActive: true,
      ),
      gripSize: 5,
      children: [
        Attitude(latestEvent: widget.latestEvent),
        Altitude(latestEvent: widget.latestEvent),
        CustomMap(latestEvent: widget.latestEvent)
      ],
    );
  }
}
