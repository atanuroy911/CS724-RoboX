import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'settings_page.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';



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
            // Display the spoken text in a separate RichText widget
            Container(
              width: containerWidth,
              decoration: BoxDecoration(
              border: Border.all(color: Colors.grey),
              ),
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: SingleChildScrollView(
                  child: RichText(text: _displayedTextSpan),
                ),
              ),
            ),
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
          spokenText += result.recognizedWords + ' ';

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
    final url = 'http://$ipAddress:$port/$path'; // Replace with your Flask server URL
    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: '{"user_query": "$spokenText"}',
    );

    if (response.statusCode == 200) {
      print('Server response: ${response.body}');
    } else {
      print('Failed to send data to server. Status code: ${response.statusCode}');
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

class MicrophoneButton extends StatefulWidget {
  final VoidCallback onPressed;
  final VoidCallback onReleased;
  final VoidCallback onLongPressed;

  MicrophoneButton({
    required this.onPressed,
    required this.onReleased,
    required this.onLongPressed,
  });

  @override
  _MicrophoneButtonState createState() => _MicrophoneButtonState();
}

class _MicrophoneButtonState extends State<MicrophoneButton> {
  bool _isLongPress = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: widget.onPressed,
      onTapUp: (details) {
        if (_isLongPress) {
          widget.onReleased();
          _isLongPress = false;
        }
      },
      onLongPress: () {
        _isLongPress = true;
        widget.onLongPressed();
      },
      onLongPressEnd: (details) {
        if (_isLongPress) {
          widget.onReleased();
          _isLongPress = false;
        }
      },
      child: Container(
        padding: EdgeInsets.all(8.0),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.blue,
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.mic, size: 44.0, color: Colors.white)],
        ),
      ),
    );
  }
}
