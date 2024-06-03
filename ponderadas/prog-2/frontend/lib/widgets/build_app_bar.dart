// ignore_for_file: unused_element, prefer_const_constructors_in_immutables

import 'package:flutter/material.dart';
import 'package:frontend/constants/colors.dart';

AppBar buildAppBar(srcImage) {
  return AppBar(
      backgroundColor: tdBGColor,
      elevation: 0,
      title: Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          SizedBox(
            height: 40,
            width: 40,
            child: ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: Image.network(srcImage),
            ),
          ),
        ],
      ));
}
