import 'package:flutter/material.dart';
import 'package:frontend/screens/home.dart';
import '../constants/colors.dart';

class LoginPage extends StatelessWidget {
  LoginPage({super.key});

  final usernameController = TextEditingController();
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

                // username
                LoginTextField(
                  controller: usernameController,
                  hintText: "Username",
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
                const Padding(
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

  void signUserIn(context) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => Home()));
  }
}

class SquareTile extends StatelessWidget {
  final String imageUrl;

  const SquareTile({super.key, required this.imageUrl});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
          border: Border.all(color: Colors.grey),
          borderRadius: BorderRadius.circular(20),
          color: Colors.white),
      child: Image.network(
        imageUrl,
        height: 72,
      ),
    );
  }
}

class SignInButton extends StatelessWidget {
  final Function()? onTap;

  const SignInButton({super.key, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        decoration: BoxDecoration(
          color: tdBlack,
          borderRadius: BorderRadius.circular(8),
        ),
        padding: const EdgeInsets.all(25),
        margin: const EdgeInsets.symmetric(horizontal: 25),
        child: const Center(
          child: Text(
            "Sign In",
            style: TextStyle(
              fontSize: 16,
              color: Colors.white,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
      ),
    );
  }
}

class LoginTextField extends StatelessWidget {
  final controller;
  final String hintText;
  final bool obscureText;

  const LoginTextField({
    super.key,
    required this.controller,
    required this.hintText,
    required this.obscureText,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(
        horizontal: 25,
      ),
      child: TextField(
        controller: controller,
        obscureText: obscureText,
        decoration: InputDecoration(
            enabledBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: tdBlack),
            ),
            focusedBorder: const OutlineInputBorder(
              borderSide: BorderSide(color: tdBlue),
            ),
            fillColor: Colors.white,
            filled: true,
            hintText: hintText,
            hintStyle: TextStyle(color: Colors.grey[500])),
      ),
    );
  }
}
