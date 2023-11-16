import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

import 'home_page.dart';

class SettingsPage extends StatefulWidget {
  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final TextEditingController _ipController = TextEditingController();
  final TextEditingController _portController = TextEditingController();
  final TextEditingController _pathController = TextEditingController();
  final TextEditingController _logController = TextEditingController();

  late SharedPreferences _prefs;

  @override
  void initState() {
    super.initState();
    _loadSavedValues();
  }

  Future<void> _loadSavedValues() async {
    _prefs = await SharedPreferences.getInstance();
    setState(() {
      _ipController.text = _prefs.getString('ipAddress') ?? '';
      _portController.text = _prefs.getInt('port').toString() ?? '';
      _pathController.text = _prefs.getString('path') ?? '';
    });
  }

  void _saveValues() {
    _prefs.setString('ipAddress', _ipController.text);
    _prefs.setInt('port', int.tryParse(_portController.text) ?? 80);
    _prefs.setString('path', _pathController.text);
  }

  void _log(String message, [Color? color]) {
    final logMessage = '$message\n';

    final span = TextSpan(text: logMessage, style: TextStyle(color: color));

    setState(() {
      _logController.text += logMessage;
      _logController.value = TextEditingValue(
        text: _logController.text,
        selection: TextSelection.collapsed(offset: _logController.text.length),
      );
    });
  }

  bool validateIPAddress(String ip) {
    final ipv4Regex = RegExp(r'^(\d{1,3}\.){3}\d{1,3}$');
    final ipv6Regex = RegExp(r'^([\da-f]{1,4}:){7}[\da-f]{1,4}$');

    if (ipv4Regex.hasMatch(ip)) {
      final parts = ip.split('.');
      for (var part in parts) {
        if (int.parse(part) > 255) {
          return false;
        }
      }
      return true;
    }

    if (ipv6Regex.hasMatch(ip)) {
      final parts = ip.split(':');
      for (var part in parts) {
        if (part.length > 4) {
          return false;
        }
      }
      return true;
    }

    return false;
  }

  Future<void> _checkConnection() async {
    final String ipAddress = _ipController.text;
    final int port = int.tryParse(_portController.text) ?? 80;
    final String path = _pathController.text;

    if (!validateIPAddress(ipAddress)) {
      _log('Invalid IP address');
      return;
    }

    _log('Requesting to $ipAddress:$port/$path');

    try {
      final response = await http
          .get(Uri.parse('http://$ipAddress:$port/$path'))
          .timeout(Duration(seconds: 5));

      if (response.statusCode == 200) {
        _log('Connection successful', Colors.green); // Colored text for success
        _log('Response:');
        _log(formatJson(response.body)); // Beautifully formatted JSON
        await _promptToSaveValues();
      } else {
        _log('Connection unsuccessful', Colors.red); // Colored text for failure
        _log('Response: ${response.body}');
      }
    } catch (error) {
      _log('Connection failed: $error', Colors.red); // Colored text for failure
    }
  }

  // Function to format JSON response beautifully
  String formatJson(String jsonStr) {
    try {
      final dynamic jsonObj = json.decode(jsonStr);
      final JsonEncoder encoder = JsonEncoder.withIndent('  ');
      return encoder.convert(jsonObj);
    } catch (e) {
      return jsonStr; // Return the original string if unable to format
    }
  }

  Future<void> _promptToSaveValues() async {
    final String savedIp = _prefs.getString('ipAddress') ?? '';
    final int savedPort = _prefs.getInt('port') ?? 0;

    final String newIp = _ipController.text;
    final int newPort = int.tryParse(_portController.text) ?? 0;

    if (newIp == savedIp && newPort == savedPort) {
      // IP and Port are the same, no need to prompt to save.
      return;
    }

    final shouldSave = await showDialog<bool>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Save Connection Settings?'),
          content: Text('Do you want to save the current connection settings?'),
          actions: [
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(true);
              },
              child: Text('Yes'),
            ),
            TextButton(
              onPressed: () {
                Navigator.of(context).pop(false);
              },
              child: Text('No'),
            ),
          ],
        );
      },
    );

    if (shouldSave ?? false) {
      _saveValues();
      // Use Navigator.pushReplacement to reload the HomePage with new values
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => HomePage()),
      );
    }
  }

  void _clearLog() {
    setState(() {
      _logController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Robo X Companion - Settings'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _ipController,
              decoration: InputDecoration(labelText: 'IP Address'),
            ),
            TextField(
              controller: _portController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Port'),
            ),
            TextField(
              controller: _pathController,
              decoration: InputDecoration(labelText: 'Path'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                _clearLog();
                await _checkConnection();
              },
              child: Text('Check Connection'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _saveValues,
              child: Text('Save Settings'),
            ),
            SizedBox(height: 20),
            Text('Log:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            SizedBox(height: 10),
            Expanded(
              child: Container(
                width: MediaQuery.of(context).size.width * 0.95,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: SingleChildScrollView(
                    child: RichText(
                      text: TextSpan(
                        style: DefaultTextStyle.of(context).style,
                        children: <TextSpan>[
                          for (var log in _logController.text.split('\n'))
                            TextSpan(
                              text: '$log\n',
                              style: log.contains('successful')
                                  ? TextStyle(color: Colors.green, fontSize: 16.0)
                                  : log.contains('unsuccessful') || log.contains('failed')
                                  ? TextStyle(color: Colors.red, fontSize: 16.0)
                                  : TextStyle(color: Colors.black, fontSize: 16.0),
                            ),
                        ],
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
