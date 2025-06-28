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

  bool isPosition() => type == "POSITION";

  bool isAltitude() => type == "ALTITUDE";


  LatLng? latLng() {
    if(!isPosition()) return null;
    double lat = double.parse(payload!['lat']!);
    double long = double.parse(payload!['long']!);
    return LatLng(lat, long);
  }

  factory Event.fromJson(Map<String, dynamic> json) => _$EventFromJson(json);

  Map<String, dynamic> toJson() => _$EventToJson(this);

  @override
  String toString() {
    return '{type: $type, datetime: $datetime, payload: $payload}';
  }
}
