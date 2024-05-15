// ignore_for_file: avoid_print, prefer_typing_uninitialized_variables, prefer_const_constructors

import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../globals.dart' as globals;

var baseurl = globals.baseUrl;

Future<bool> login(String email, String password) async {
  final Map<String, String> data = {
    "email": email,
    "password": password,
  };

  final jsonData = jsonEncode(data);

  var response = await http.post(Uri.parse("$baseurl/user/login"),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonData);

  if (response.statusCode == 200) {
    final body = jsonDecode(response.body);
    _storeAccessToken(body["acess_token"], body["user_id"]);
    return true;
  } else {
    return false;
  }
}

Future<bool> signUp(String name, String email, String password) async {
  final Map<String, String> data = {
    "email": email,
    "name": name,
    "password": password
  };

  var response = await http.post(Uri.parse("$baseurl/user/signup"),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(data));

  if (response.statusCode == 200) {
    return true;
  } else {
    return false;
  }
}

void _storeAccessToken(String token, int userId) async {
  final storage = FlutterSecureStorage();
  globals.accessToken = token;
  globals.userId = userId;
  await storage.write(key: "access_token", value: token);
  await storage.write(key: "userId", value: userId.toString());
}
