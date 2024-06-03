// ignore_for_file: unused_element, prefer_const_constructors_in_immutables

import 'package:flutter/material.dart';
import 'package:frontend/api/todo.dart';
import 'package:frontend/screens/login.dart';
import 'package:frontend/screens/user.dart';
import 'package:frontend/widgets/bottom_bar.dart';
import '../constants/colors.dart';
import '../model/todo.dart';
import '../widgets/build_app_bar.dart';
import '../widgets/todo_item.dart';

class Home extends StatefulWidget {
  Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  List<ToDo> todosList = [];
  List<ToDo> _foundTodo = [];
  final _todoController = TextEditingController();

  int _currentIndex = 0;

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

  @override
  void initState() {
    super.initState();
    fetchTodos();
    _foundTodo = todosList;
  }

  @override
  Widget build(BuildContext context) {
    const src =
        'https://tlfrtkzvkxvuczdoozhu.supabase.co/storage/v1/object/public/images/image.jpg';
    return Scaffold(
      backgroundColor: tdBGColor,
      appBar: buildAppBar(src),
      body: Stack(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 20,
              vertical: 15,
            ),
            child: _buildToDos(todosList),
          ),
          Align(
            alignment: Alignment.bottomCenter,
            child: _buildAddTodo(),
          )
        ],
      ),
      bottomNavigationBar:
          CustomBottomNavigationBar(currentIndex: _currentIndex, onTap: _onTap),
    );
  }

  Column _buildToDos(todosList) {
    return Column(
      children: [
        _searchBox(),
        Expanded(
          child: ListView(
            children: [
              Container(
                margin: const EdgeInsets.only(
                  top: 50,
                  bottom: 20,
                ),
                child: const Text(
                  "All ToDos",
                  style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
              for (ToDo todoo in _foundTodo.reversed)
                TodoItem(
                  todo: todoo,
                  onTodoChanged: _handleTodoChange,
                  onDeleteItem: _handleDeleteTodo,
                )
            ],
          ),
        ),
      ],
    );
  }

  void _handleTodoChange(ToDo todo) async {
    if (await checkTodo(todo.id)) {
      fetchTodos();
    } else {
      fetchTodos();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Erro em atualizar tarefa!'),
        ),
      );
    }
  }

  void _handleDeleteTodo(int id) async {
    if (await removeTodo(id)) {
      fetchTodos();
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Erro em remover tarefa!'),
        ),
      );
    }
  }

  void fetchTodos() async {
    final todos = await getTodos();
    setState(() {
      todosList = todos;
      _foundTodo = todos;
    });
  }

  void _addTodoItem(String todo) async {
    if (await addTodo(todo)) {
      fetchTodos();
      _todoController.clear();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Tarefa registrada com sucesso!'),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Erro em registrar tarefa!'),
        ),
      );
    }
  }

  void _runFilter(String enteredKeyword) {
    List<ToDo> results = [];
    if (enteredKeyword.isEmpty) {
      results = todosList;
    } else {
      results = todosList
          .where((item) => item.todoText!
              .toLowerCase()
              .contains(enteredKeyword.toLowerCase()))
          .toList();
    }

    setState(() {
      _foundTodo = results;
    });
  }

  Row _buildAddTodo() {
    return Row(
      children: [
        _buildAddTodoInput(),
        _buildAddTodoButton(),
      ],
    );
  }

  Expanded _buildAddTodoInput() {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.only(
          bottom: 20,
          right: 20,
          left: 20,
        ),
        padding: const EdgeInsets.symmetric(
          horizontal: 20,
          vertical: 5,
        ),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: const [
            BoxShadow(
              color: Colors.grey,
              offset: Offset(0.0, 0.0),
              blurRadius: 10.0,
              spreadRadius: 0.0,
            ),
          ],
          borderRadius: BorderRadius.circular(10),
        ),
        child: TextField(
          controller: _todoController,
          decoration: const InputDecoration(
            hintText: "Add a new todo item",
            border: InputBorder.none,
          ),
        ),
      ),
    );
  }

  Container _buildAddTodoButton() {
    return Container(
      margin: const EdgeInsets.only(
        bottom: 20,
        right: 20,
      ),
      child: ElevatedButton(
        onPressed: () {
          _addTodoItem(_todoController.text);
        },
        style: ElevatedButton.styleFrom(
          backgroundColor: tdBlue,
          minimumSize: const Size(60, 30),
          elevation: 10,
        ),
        child: const Text(
          "+",
          style: TextStyle(
            fontSize: 40,
            color: Colors.white,
          ),
        ),
      ),
    );
  }

  Container _searchBox() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 15),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
      ),
      child: TextField(
        onChanged: (value) => _runFilter(value),
        decoration: const InputDecoration(
          contentPadding: EdgeInsets.all(0),
          prefixIcon: Icon(
            Icons.search,
            color: tdBlack,
            size: 20,
          ),
          prefixIconConstraints: BoxConstraints(
            maxHeight: 20,
            minWidth: 25,
          ),
          border: InputBorder.none,
          hintText: "Search",
          hintStyle: TextStyle(color: tdGrey),
        ),
      ),
    );
  }
}
