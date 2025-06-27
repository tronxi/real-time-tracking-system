import 'dart:ui_web' as ui;

void registerViewFactory(String viewType, dynamic Function(int) viewFactory) {
  ui.platformViewRegistry.registerViewFactory(viewType, viewFactory);
}
