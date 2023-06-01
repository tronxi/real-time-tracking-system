import 'package:flutter/material.dart';

class ResponsiveQuery {
  static bool isDesktop(BuildContext context) {
    return MediaQuery.of(context).size.width >= 1024;
  }
}