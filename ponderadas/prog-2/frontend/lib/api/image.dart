import "dart:convert";
import "dart:developer";
import "dart:io";

import "../globals.dart" as globals;
import "package:http/http.dart" as http;

var baseurl = globals.imageServiceUrl;

Future<String> getImageUrl() async {
  final response = await http.get(
    Uri.parse("$baseurl/${globals.userId}"),
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
  );

  if (response.statusCode == 200) {
    final String imageUrl = json.decode(response.body);
    return imageUrl;
  } else {
    return "https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/025.png";
  }
}

Future<bool> sendImage(File file) async {
  var request = http.MultipartRequest(
      "POST", Uri.parse("$baseurl/upload/${globals.userId}"));

  request.files.add(await http.MultipartFile.fromPath("file", file.path));

  final response = await request.send();

  return response.statusCode == 200;
}
  