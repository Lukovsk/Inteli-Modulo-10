// ignore_for_file: unused_element

import 'package:flutter/material.dart';
import '../constants/colors.dart';
import '../model/todo.dart';
import '../widgets/todo_item.dart';

class Home extends StatefulWidget {
  Home({super.key});

  @override
  State<Home> createState() => _HomeState();
}

class _HomeState extends State<Home> {
  final todosList = ToDo.todoList();
  List<ToDo> _foundTodo = [];
  final _todoController = TextEditingController();

  @override
  void initState() {
    _foundTodo = todosList;
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    const src = 'https://avatars.githubusercontent.com/u/99260684?v=4';
    return Scaffold(
      backgroundColor: tdBGColor,
      appBar: _buildAppBar(src),
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

  void _handleTodoChange(ToDo todo) {
    setState(() {
      todo.check = !todo.check;
    });
  }

  void _handleDeleteTodo(int id) {
    setState(() {
      todosList.removeWhere((element) => element.id == id);
    });
  }

  void _addTodoItem(String todo) {
    setState(() {
      todosList.add(ToDo(
          id: (todosList.isNotEmpty ? todosList.last.id + 1 : 0),
          todoText: todo));
    });
    _todoController.clear();
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

AppBar _buildAppBar(srcImage) {
  return AppBar(
      backgroundColor: tdBGColor,
      elevation: 0,
      title: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Icon(
            Icons.menu,
            color: tdBlack,
            size: 30,
          ),
          // ignor  e: sized_box_for_whitespace
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
