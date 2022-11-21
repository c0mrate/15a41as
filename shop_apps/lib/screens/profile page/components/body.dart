import 'package:flutter/material.dart';
import 'package:shop_apps/screens/home/home_screen.dart';

import 'profile_menu.dart';
import 'profile_pic.dart';

class Body extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: EdgeInsets.symmetric(vertical: 20),
      child: Column(
        children: [
          ProfilePic(),
          SizedBox(height: 20),
          ProfileMenu(
            text: "Name: Burin Hongprapat",
            icon: "assets/icons/User Icon.svg",
            
          ),
          ProfileMenu(
            text: "Email: gg677938@email.com",
            icon: "assets/icons/Mail.svg",
            
          ),
          ProfileMenu(
            text: "SAVE",
            icon: "assets/icons/Success.svg",
            press: () => {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => HomeScreen(),
                ),
              ),
            },
          ),
        ],
      ),
    );
  }
}