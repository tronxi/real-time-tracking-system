import 'dart:async';
import 'dart:io';
import 'dart:math' as math;

import 'package:dashboard/models/event.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_compass/flutter_compass.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_cancellable_tile_provider/flutter_map_cancellable_tile_provider.dart';
import 'package:geolocator/geolocator.dart';
import 'package:latlong2/latlong.dart';

class CustomMap extends StatefulWidget {
  final Event latestEvent;

  const CustomMap({Key? key, required this.latestEvent}) : super(key: key);

  @override
  State<CustomMap> createState() => _CustomMapState();
}

class _CustomMapState extends State<CustomMap> {
  late final double _defaultZoom;
  late final List<Marker> _markers;
  late final List<Marker> _rocketMarkers;
  late LatLng _current;
  late double _currentHeading;
  late LatLng? _latestRocketPosition;
  late bool _moveToRocket;
  final MapController _mapController = MapController();

  @override
  void initState() {
    _moveToRocket = true;
    _defaultZoom = 18;
    _markers = [];
    _rocketMarkers = [];
    _currentHeading = 0;
    _latestRocketPosition = null;
    _current = const LatLng(40.416775, -3.703790);
    _determinePosition().then((value) {
      _current = LatLng(value.latitude, value.longitude);
      _markers.add(_createCompassMarker());
      _initCompass();
      _followPosition();
    });

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    if (_moveToRocket && _latestRocketPosition != null) {
      _moveToCurrentRocketPosition();
      setState(() {
        _moveToRocket = false;
      });
    }
    if (widget.latestEvent.isTm()) {
      setState(() {
        _latestRocketPosition = widget.latestEvent.latLng();
        _rocketMarkers.clear();
        _rocketMarkers.add(_createRocketMarker());
      });
    }
    return Stack(
      children: [
        FlutterMap(
          mapController: _mapController,
          options: MapOptions(
            initialCenter: _current,
            maxZoom: 18.2,
            initialZoom: _defaultZoom,
            minZoom: 0,
          ),
          children: [
            TileLayer(
              tileProvider: CancellableNetworkTileProvider(),
              urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            ),
            MarkerLayer(markers: _markers),
            MarkerLayer(markers: _rocketMarkers),
          ],
        ),
        Positioned(
          bottom: 16.0,
          right: 16.0,
          child: IconButton(
            onPressed: _moveToCurrentRocketPosition,
            icon: const Icon(Icons.rocket),
          ),
        ),
        Positioned(
          bottom: 16.0,
          right: 80.0,
          child: IconButton(
            onPressed: _moveToCurrentUserPosition,
            icon: const Icon(Icons.location_searching),
          ),
        ),
      ],
    );

  }

  void _moveToCurrentRocketPosition() {
    if (_latestRocketPosition != null) {
      _mapController.move(_latestRocketPosition!, _defaultZoom);
    }
  }

  void _moveToCurrentUserPosition() {
    _mapController.move(_current, _defaultZoom);
    }

  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return Future.error('Location services are disabled.');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.denied) {
        return Future.error('Location permissions are denied');
      }
    }

    if (permission == LocationPermission.deniedForever) {
      return Future.error(
          'Location permissions are permanently denied, we cannot request permissions.');
    }
    return await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.best);
  }

  Marker _createCompassMarker() {
    return Marker(
      width: 80,
      height: 80,
      point: _current,
      rotate: true,
      child: Transform.rotate(
        angle: (_currentHeading * (math.pi / 180)),
        child: const Icon(
          Icons.keyboard_arrow_up,
          color: Colors.blueAccent,
          size: 80,
        ),
      ),
    );
  }

  Marker _createRocketMarker() {
    return Marker(
      width: 40,
      height: 40,
      point: widget.latestEvent.latLng()!,
      rotate: true,
      child: Transform.rotate(
        angle: (_currentHeading * (math.pi / 180)),
        child: const Icon(
          Icons.rocket,
          color: Colors.redAccent,
          size: 40,
        ),
      ),
    );
  }

  void _initCompass() {
    if (kIsWeb) return;
    if (Platform.isAndroid || Platform.isIOS) {
      FlutterCompass.events?.listen((event) {
        setState(() {
          _currentHeading = event.heading ?? 0;
        });
      });
    }
  }

  void _followPosition() {
    Geolocator.getPositionStream(
            locationSettings:
                const LocationSettings(accuracy: LocationAccuracy.high))
        .listen((event) => setState(() {
              _current = LatLng(event.latitude, event.longitude);
            }));
  }
}
