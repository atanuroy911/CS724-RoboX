import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AppState extends ChangeNotifier {
  late SharedPreferences _prefs;

  String ipAddress = '';
  String port = '';

  Future<void> loadSavedValues() async {
    _prefs = await SharedPreferences.getInstance();
    ipAddress = _prefs.getString('ipAddress') ?? '';
    port = _prefs.getInt('port')?.toString() ?? '';
    notifyListeners();
  }

// Add methods to update shared preferences values if needed
}
