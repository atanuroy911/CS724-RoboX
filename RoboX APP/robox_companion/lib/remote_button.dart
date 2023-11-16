import 'package:flutter/material.dart';

class RemoteButton extends StatelessWidget {
  final IconData icon;
  final String text;

  RemoteButton({required this.icon, required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: ElevatedButton(
        onPressed: () {
          print('Pressed $text button');
        },
        child: Icon(icon),
      ),
    );
  }
}
