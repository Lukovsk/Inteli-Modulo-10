import "dart:convert";
import "dart:io";

import "package:frontend/model/todo.dart";

import "../globals.dart" as globals;
import "package:http/http.dart" as http;

var baseurl = globals.baseUrl;

Future<List<ToDo>> getTodos() async {
  final response = await http.get(
    Uri.parse("$baseurl/todo/user:${globals.userId}"),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer ${globals.accessToken}',
    },
  );
  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(response.body);
    return data.map((d) => ToDo.fromJson(d)).toList();
  } else {
    return ToDo.todoList();
  }
}

Future<bool> addTodo(String content) async {
  final response = await http.post(Uri.parse("$baseurl/todo/"),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer ${globals.accessToken}',
      },
      body: jsonEncode(<String, dynamic>{
        "content": content,
        "user_id": globals.userId,
      }));

  return response.statusCode == 200;
}

Future<bool> removeTodo(int id) async {
  final response = await http.delete(
    Uri.parse("$baseurl/todo/$id"),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer ${globals.accessToken}',
    },
  );

  return response.statusCode == 200;
}

Future<bool> checkTodo(int id) async {
  final response = await http.put(
    Uri.parse("$baseurl/todo/check/$id"),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Bearer ${globals.accessToken}',
    },
  );

  return response.statusCode == 200;
}
