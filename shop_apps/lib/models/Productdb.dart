import 'dart:convert';

Productdb productdbFromJson(String str) => Productdb.fromJson(json.decode(str));

String productdbToJson(Productdb data) => json.encode(data.toJson());

class Productdb {
  Productdb({
    required this.data,
  });

  List<Datum> data;

  factory Productdb.fromJson(Map<String, dynamic> json) => Productdb(
        data: List<Datum>.from(json["data"].map((x) => Datum.fromJson(x))),
      );

  Map<String, dynamic> toJson() => {
        "data": List<dynamic>.from(data.map((x) => x.toJson())),
      };
}

class Datum {
  Datum({
    required this.detail,
    required this.id,
    required this.image,
    required this.price,
    required this.title,
  });

  String detail;
  int id;
  String image;
  double price;
  String title;

  factory Datum.fromJson(Map<String, dynamic> json) => Datum(
        detail: json["detail"],
        id: json["id"],
        image: json["image"],
        price: json["price"].toDouble(),
        title: json["title"],
      );

  Map<String, dynamic> toJson() => {
        "detail": detail,
        "id": id,
        "image": image,
        "price": price,
        "title": title,
      };
}