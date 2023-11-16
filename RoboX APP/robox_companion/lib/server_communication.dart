import 'package:http/http.dart' as http;

class ServerCommunication {
  static Future<void> sendToServer(String ipAddress, String port, String path, String spokenText) async {
    final url = 'http://$ipAddress:$port/$path';

    try {
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
    } catch (e) {
      print('Error sending data to server: $e');
    }
  }
}
