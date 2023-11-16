import 'package:flutter/material.dart';


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
