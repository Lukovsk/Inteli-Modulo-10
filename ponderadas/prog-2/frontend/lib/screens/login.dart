// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables

import 'package:flutter/material.dart';
import 'package:frontend/screens/home.dart';
import '../components/login_text_field.dart';
import '../components/sign_in_button.dart';
import '../components/square_tile.dart';
import '../constants/colors.dart';
import "../api/login.dart";

class LoginPage extends StatelessWidget {
  LoginPage({super.key});

  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        backgroundColor: tdBGColor,
        body: SafeArea(
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 50),
                // logo
                const Icon(
                  Icons.lock,
                  size: 100,
                ),

                const SizedBox(height: 50),

                // welcome back
                const Text(
                  "Bem vindo de volta!",
                  style: TextStyle(
                    color: tdGrey,
                    fontSize: 16,
                  ),
                ),

                const SizedBox(height: 25),

                // email
                LoginTextField(
                  controller: emailController,
                  hintText: "Email",
                  obscureText: false,
                ),

                const SizedBox(height: 25),
                // password
                LoginTextField(
                  controller: passwordController,
                  hintText: "Senha",
                  obscureText: true,
                ),

                const SizedBox(height: 10),
                // forgot password
                GestureDetector(
                  onTap: () {
                    _registerUser(context);
                  },
                  child: Padding(
                    padding: EdgeInsets.symmetric(horizontal: 25.0),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        Text(
                          "Não tem uma conta?",
                          style: TextStyle(color: tdGrey),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 25),

                // signin
                SignInButton(
                  onTap: () {
                    signUserIn(context);
                  },
                ),

                const SizedBox(height: 25),

                // github
              ],
            ),
          ),
        ));
  }

  void signUserIn(context) async {
    if (await login(emailController.text, passwordController.text)) {
      Navigator.push(context, MaterialPageRoute(builder: (context) => Home()));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Falha no login!'),
        ),
      );
    }
  }

  void signUserUp(context, String name, String email, String password) async {
    if (await signUp(name, email, password)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Usuário registrado com sucesso!'),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Falha no registro!'),
        ),
      );
    }
  }

  void _registerUser(mainContext) {
    showDialog(
      context: mainContext,
      builder: (context) {
        String name = '';
        String email = '';
        String password = '';

        return AlertDialog(
          title: const Text('Registrar-se'),
          content: Container(
            margin: EdgeInsets.symmetric(horizontal: 10, vertical: 25),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextField(
                  decoration: InputDecoration(labelText: 'Nome'),
                  onChanged: (value) {
                    name = value;
                  },
                ),
                TextField(
                  decoration: InputDecoration(labelText: 'Email'),
                  onChanged: (value) {
                    email = value;
                  },
                ),
                TextField(
                  decoration: InputDecoration(labelText: 'Senha'),
                  onChanged: (value) {
                    password = value;
                  },
                ),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () {
                signUserUp(mainContext, name, email, password);
                Navigator.pop(context);
              },
              child: const Text('Sign Up'),
            ),
          ],
        );
      },
    );
  }
}
