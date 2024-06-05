// ignore_for_file: prefer_const_constructors

import 'package:awesome_notifications/awesome_notifications.dart';
import 'package:flutter/material.dart';
// import 'package:frontend/screens/user.dart';
import 'screens/login.dart';

// import 'screens/home.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  AwesomeNotifications().initialize(
    null,
    [
      NotificationChannel(
        channelKey: "basic_chanel",
        channelName: "Image Notification",
        channelDescription: "Notification channel for images changing",
        defaultColor: Colors.white,
        ledColor: Colors.blue,
        importance: NotificationImportance.High,
      ),
    ],
    debug: true,
  );
  requestNotificationPermissions();
  runApp(const MyApp());
}

Future<void> requestNotificationPermissions() async {
  bool isAllowed = await AwesomeNotifications().isNotificationAllowed();
  if (!isAllowed) {
    await AwesomeNotifications().requestPermissionToSendNotifications();
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "ToDo App",
      home: LoginPage(),
    );
  }
}
