class ToDo {
  int id;
  String? todoText;
  bool check;

  ToDo({
    required this.id,
    required this.todoText,
    this.check = false,
  });

  factory ToDo.fromJson(Map<String, dynamic> json) {
    return ToDo(
      id: json["id"],
      todoText: json["content"],
      check: json["check"],
    );
  }

  static List<ToDo> todoList() {
    return [
      ToDo(id: 0, todoText: "Hi 1", check: true),
      ToDo(id: 1, todoText: "Hi 2", check: true),
      ToDo(id: 2, todoText: "Hi 3"),
      ToDo(id: 3, todoText: "Hi 4"),
      ToDo(id: 4, todoText: "Hi 5"),
    ];
  }
}
