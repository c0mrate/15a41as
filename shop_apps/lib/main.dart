import 'package:flutter/material.dart';
import 'package:shop_apps/screens/splash/splash_screen.dart';
import 'package:shop_apps/theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Shop Apps Demo",
      theme: theme(),
      home: SplashScreen(),
      // initialRoute: SplashScreen.routeName,
      // routes: routes,
    );
  }
}