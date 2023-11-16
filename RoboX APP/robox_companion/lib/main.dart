import 'package:flutter/material.dart';
import 'home_page.dart';
import 'package:provider/provider.dart';

import 'app_state.dart'; // Import the file where you defined AppState

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => AppState(),
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Robo X Companion',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}
