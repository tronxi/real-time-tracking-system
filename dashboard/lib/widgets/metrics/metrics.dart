import 'package:flutter/material.dart';

class Metrics extends StatelessWidget {
  final ScrollController _controller = ScrollController();
  Metrics({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white70,
      padding: const EdgeInsets.all(10),
      child: Stack(children: [
        const Wrap(
          direction: Axis.vertical,
          alignment: WrapAlignment.start,
          runAlignment: WrapAlignment.start,
          runSpacing: 20,
          children: [
            _Property(property: "Lat", value: "23"),
            _Property(property: "Long", value: "23"),
            _Property(property: "Altura", value: "100"),
            _Property(property: "Velocidad", value: "20"),
            _Property(property: "Estado", value: "Conectado"),
            SizedBox(
              width: 600,
              height: 200,
              child: Card(
                  child: Padding(
                padding: EdgeInsets.all(8.0),
                child: SingleChildScrollView(
                  scrollDirection: Axis.vertical,
                  child: Text(
                    "...........\n...........\n...........\n...........\n...........\nLogs del cohete\n...........\n...........\n...........\n...........\n...........\n...........\n",
                    style: TextStyle(fontSize: 16.0),
                  ),
                ),
              )),
            )
          ],
        ),
        Positioned(
            bottom: 10,
            right: 10,
            child: CircleAvatar(
              radius: 30,
              backgroundColor: Colors.redAccent,
              child: SizedBox(
                width: 60,
                height: 60,
                child: IconButton(
                  icon: const Icon(
                    Icons.rocket_launch,
                    color: Colors.white,
                  ),
                  onPressed: () {},
                ),
              ),
            ))
      ]),
    );
  }
}

class _Property extends StatelessWidget {
  final String property;
  final String value;
  const _Property({Key? key, required this.property, required this.value})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Text(
          "$property: ",
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
        ),
        Text(value, style: const TextStyle(fontSize: 20))
      ],
    );
  }
}
