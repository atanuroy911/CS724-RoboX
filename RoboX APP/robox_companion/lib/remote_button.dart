import 'package:flutter/material.dart';
import 'package:robox_companion/server_communication.dart';
import 'package:shared_preferences/shared_preferences.dart';

class RemoteButton extends StatelessWidget {
  final IconData icon;
  final String text;

  RemoteButton({required this.icon, required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: ElevatedButton(
        onPressed: () async {
          // Retrieve IP and port from SharedPreferences
          SharedPreferences prefs = await SharedPreferences.getInstance();
          String ipAddress = prefs.getString('ipAddress') ?? '';
          String port = prefs.getInt('port')?.toString() ?? '';

          // Check if IP and port are available
          if (ipAddress.isEmpty || port.isEmpty) {
            print('IP address or port is not available. Please set it in the Settings.');
            return;
          }

          // Call the sendToServer function from ServerCommunication
          await ServerCommunication.sendToServer(ipAddress, port, 'control', text);

          print('Pressed $text button');
        },
        child: Icon(icon),
      ),
    );
  }
}
