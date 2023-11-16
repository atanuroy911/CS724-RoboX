import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'settings_page.dart';
import 'remote_button.dart';
import 'microphone_button.dart';
import 'spoken_text_display.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:shared_preferences/shared_preferences.dart';
import 'server_communication.dart';


class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final stt.SpeechToText _speech = stt.SpeechToText();
  List<TextSpan> _spokenTextSpans = [];
  late TextSpan _displayedTextSpan = TextSpan(); // New variable to store the displayed rich text

  late SharedPreferences _prefs;

  late String ipAddress = '';
  late String port = '';
  final String path = 'prompt';

  @override
  void initState() {
    super.initState();
    _displayedTextSpan = TextSpan();
    _loadSavedValues(); // Load saved values here
  }

  Future<void> _loadSavedValues() async {
    _prefs = await SharedPreferences.getInstance();
    setState(() {
      ipAddress = _prefs.getString('ipAddress') ?? '';
      port = _prefs.getInt('port')?.toString() ?? ''; // Use toString() here
      if (kDebugMode) {
        print('SHUORER $ipAddress, $port');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    double containerWidth = MediaQuery.of(context).size.width * 0.95;

    return Scaffold(
      appBar: AppBar(
        title: Text('Robo X Companion - Home'),
        actions: [
          IconButton(
            icon: Icon(Icons.settings),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => SettingsPage()),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                RemoteButton(icon: Icons.arrow_upward, text: 'Up'),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                RemoteButton(icon: Icons.arrow_back, text: 'Left'),
                RemoteButton(icon: Icons.check, text: 'OK'),
                RemoteButton(icon: Icons.arrow_forward, text: 'Right'),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                RemoteButton(icon: Icons.arrow_downward, text: 'Down'),
              ],
            ),
            SizedBox(height: 20),
            MicrophoneButton(
              onPressed: _startListening,
              onReleased: _stopListening,
              onLongPressed: _startListeningLongPress,
            ),
            SizedBox(height: 20),
            // Display the spoken text using the SpokenTextDisplay widget
            SpokenTextDisplay(displayedTextSpan: _displayedTextSpan, containerWidth: containerWidth),
          ],
        ),
      ),
    );
  }

  void _startListening() async {
    if (await _speech.initialize()) {
      String spokenText = ''; // Variable to accumulate spoken text
      bool isListening = true; // Flag to track whether speech recognition is ongoing

      _speech.listen(
        onResult: (result) {
          // Concatenate the recognized words to the accumulated spoken text
          spokenText = result.recognizedWords + ' ';

          // Update the displayed text with the accumulated spoken text
          setState(() {
            _spokenTextSpans = _getSpokenTextSpans(spokenText);
            _displayedTextSpan = TextSpan(style: DefaultTextStyle.of(context).style, children: _spokenTextSpans);
          });
        },
        onSoundLevelChange: (level) {
          // Optionally, you can use this callback to track sound levels during speech recognition
        },
      );

      // Add a delay or use a timer to simulate the end of speech recognition
      await Future.delayed(Duration(seconds: 5));

      // Stop speech recognition after a simulated delay
      if (isListening) {
        _speech.stop();
        isListening = false;

        // Speech recognition is complete, send the accumulated spoken text to the Flask server
        await _sendSpokenTextToServer(spokenText);
      }
    }
  }

  Future<void> _sendSpokenTextToServer(String spokenText) async {
    try {
      await ServerCommunication.sendToServer(ipAddress, port, path, spokenText);
    } catch (e) {
      print('Error sending data to server: $e');
    }
  }

  void _startListeningLongPress() async {
    _startListening();
  }

  void _stopListening() {
    _speech.stop();
  }

  List<TextSpan> _getSpokenTextSpans(String text) {
    // Define your styles here
    TextStyle defaultStyle = TextStyle(color: Colors.black, fontSize: 16.0);
    TextStyle keywordStyle = TextStyle(color: Colors.blue, fontWeight: FontWeight.bold, fontSize: 16.0);

    // Split the text into keywords (for example, you can split by space)
    List<String> words = text.split(' ');

    // Create TextSpans with different styles for each word
    List<TextSpan> spans = [];
    for (String word in words) {
      spans.add(
        TextSpan(
          text: '$word ',
          style: word.toLowerCase() == 'robocop' ? keywordStyle : defaultStyle,
        ),
      );
    }

    return spans;
  }
}

