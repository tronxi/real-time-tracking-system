import 'package:json_annotation/json_annotation.dart';
import 'package:latlong2/latlong.dart';

part 'event.g.dart';

@JsonSerializable()
class Event {
  final String type;
  final String datetime;
  final Map<String, String>? payload;

  Event.empty()
      : type = "",
        datetime = "",
        payload = null;

  const Event(
      {required this.type, required this.datetime, required this.payload});

  bool isTm() => type == "TM";

  LatLng? latLng() {
    if(!isTm()) return null;
    double lat = double.parse(payload!['lat'] ?? "0");
    double long = double.parse(payload!['long'] ?? "0");
    return LatLng(lat, long);
  }

  factory Event.fromJson(Map<String, dynamic> json) => _$EventFromJson(json);

  Map<String, dynamic> toJson() => _$EventToJson(this);

  @override
  String toString() {
    return '{type: $type, datetime: $datetime, payload: $payload}';
  }
}
