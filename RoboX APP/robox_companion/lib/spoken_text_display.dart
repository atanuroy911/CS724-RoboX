import 'package:flutter/material.dart';

class SpokenTextDisplay extends StatelessWidget {
  final TextSpan displayedTextSpan;
  final double containerWidth;

  SpokenTextDisplay({required this.displayedTextSpan, required this.containerWidth});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: containerWidth,
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
      ),
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: SingleChildScrollView(
          child: RichText(text: displayedTextSpan),
        ),
      ),
    );
  }
}
