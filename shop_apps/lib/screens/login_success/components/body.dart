import 'package:flutter/material.dart';
import 'package:shop_apps/components/default_button.dart';
import 'package:shop_apps/screens/home/home_screen.dart';
import 'package:shop_apps/size_config.dart';

import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class Body extends StatelessWidget {

  _getjson() async { 
    var res = await http.get(
          Uri.parse("http://192.168.1.45:5000/get_data_mobile"),
           headers: {HttpHeaders.contentTypeHeader: "application/json"},
    );
    final item = json.decode(res.body);
    print(item);

    return "OK";
}
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(height: SizeConfig.screenHeight * 0.04),
        Image.asset(
          "assets/images/success.png",
          height: SizeConfig.screenHeight * 0.4, //40%
        ),
        SizedBox(height: SizeConfig.screenHeight * 0.08),
        Text(
          "Login Success",
          style: TextStyle(
            fontSize: getProportionateScreenWidth(30),
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        Spacer(),
        SizedBox(
          width: SizeConfig.screenWidth * 0.6,
          child: DefaultButton(
            text: "Back to home",
            press: () {
              // Navigator.pushNamed(context, HomeScreen.routeName);
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => HomeScreen()),
              );
            },
          ),
        ),
        Spacer(),
        // Text(_getjson()),
      ],
    );
  }
}
