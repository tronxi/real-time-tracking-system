import 'package:dashboard/models/event.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:stomp_dart_client/stomp.dart';
import 'package:stomp_dart_client/stomp_config.dart';
import 'package:stomp_dart_client/stomp_frame.dart';
import 'dart:convert';

abstract class TrackingDeviceEvent {}

class NewEventBloc extends TrackingDeviceEvent {
  final String message;
  NewEventBloc({required this.message});
}

class TrackingDeviceEventBloc extends Bloc<TrackingDeviceEvent, Event> {
  late StompClient client;
  TrackingDeviceEventBloc() : super(Event.empty()) {
    client = StompClient(
        config: StompConfig(
      url: 'wss://tronxi.ddns.net/dashboard_backend/ws',
      onConnect: _onConnect,
      onWebSocketError: (dynamic error) => print(error.toString()),
    ));
    client.activate();
    on<NewEventBloc>((event, emit) => emit(_onNewEvent(event)));
  }

  Event _onNewEvent(NewEventBloc newEventBloc) {
    final eventJson = json.decode(newEventBloc.message);
    Event event = Event.fromJson(eventJson);
    return event;
  }

  void _onConnect(StompFrame frame) {
    client.subscribe(
      destination: '/topic/events',
      callback: (frame) => add(NewEventBloc(message: frame.body!)),
    );
  }
}
