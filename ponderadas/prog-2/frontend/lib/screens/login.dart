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
                          "Esqueceu a senha?",
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

                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 25),
                  child: Row(
                    children: [
                      Expanded(
                        child: Divider(
                          thickness: 0.5,
                          color: tdGrey,
                        ),
                      ),
                      Padding(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        child: Text(
                          "Ou continue com",
                          style: TextStyle(color: tdBlack),
                        ),
                      ),
                      Expanded(
                        child: Divider(
                          thickness: 0.5,
                          color: tdGrey,
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 30),

                const Padding(
                  padding: EdgeInsets.symmetric(horizontal: 25),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SquareTile(
                          imageUrl:
                              "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1200px-GitHub_Invertocat_Logo.svg.png"),
                      SizedBox(
                        width: 40,
                      ),
                      SquareTile(
                          imageUrl:
                              "https://t.ctcdn.com.br/lvns56iaSMyHvyTur4JeYS_NYeY=/i606944.png")
                    ],
                  ),
                )

                // not a member?
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
