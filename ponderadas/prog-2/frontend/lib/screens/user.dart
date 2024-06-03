// ignore_for_file: prefer_const_constructors

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:frontend/constants/colors.dart';
import 'package:frontend/screens/home.dart';
import 'package:frontend/widgets/bottom_bar.dart';
import 'package:frontend/widgets/build_app_bar.dart';
import 'package:image_picker/image_picker.dart';

class User extends StatefulWidget {
  const User({super.key});

  @override
  State<User> createState() => _UserState();
}

class _UserState extends State<User> {
  int _currentIndex = 1;

  void _onTap(int index) {
    setState(() {
      _currentIndex = index;
    });

    switch (index) {
      case 0:
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => Home()),
        );
        break;
      case 1:
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => User()),
        );
        break;
      default:
        break;
    }
  }

  Future<File> getImage() async {
    final ImagePicker _picker = ImagePicker();

    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);

    File file = File(image!.path);

    return file;
  }

  void onSendNewImage() async {
    File file = await getImage();
  }

  @override
  Widget build(BuildContext context) {
    const src =
        'https://tlfrtkzvkxvuczdoozhu.supabase.co/storage/v1/object/public/images/image.jpg';
    return Scaffold(
      appBar: buildAppBar(src),
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Padding(
                padding: const EdgeInsets.all(16),
                child: SizedBox(
                  height: 200,
                  width: 200,
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(200),
                    child: Image.network(src),
                  ),
                ),
              ),
              Container(
                width: 330,
                height: 200,
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    ElevatedButton(
                      onPressed: onSendNewImage,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: tdBlue,
                        minimumSize: const Size(60, 60),
                        elevation: 10,
                      ),
                      child: Text(
                        "Editar imagem",
                        style: TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                        ),
                      ),
                    ),
                    ElevatedButton(
                      onPressed: () {},
                      style: ElevatedButton.styleFrom(
                        backgroundColor: tdBlue,
                        minimumSize: const Size(60, 60),
                        elevation: 10,
                      ),
                      child: Text(
                        "Remover background",
                        style: TextStyle(
                          fontSize: 20,
                          color: Colors.white,
                        ),
                      ),
                    )
                  ],
                ),
              )
            ],
          ),
        ),
      ),
      bottomNavigationBar:
          CustomBottomNavigationBar(currentIndex: _currentIndex, onTap: _onTap),
    );
  }
}
