// camera_widget.dart

import 'package:flutter/material.dart';
import 'package:flutter_mjpeg/flutter_mjpeg.dart';

class CameraWidget extends StatelessWidget {
  final String videoUrl;

  CameraWidget({required this.videoUrl});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Mjpeg(
        isLive: true,
        stream: videoUrl,
      ),
    );
  }
}
