import 'package:flutter/material.dart';
import 'package:shop_apps/components/product_card.dart';
import 'package:shop_apps/models/Product.dart';

import '../../../size_config.dart';
import 'section_title.dart';
import 'package:http/http.dart' as http;

import 'package:flutter/material.dart';
import 'package:shop_apps/components/product_card.dart';
import 'package:shop_apps/models/Product.dart';

import '../../../size_config.dart';
import 'section_title.dart';

class PopularProducts extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Product>>(
      future: getdata(),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return Container(child: 
          Text("no error"));
        }
        print(snapshot.data!);
        return Column(
          children: [
            Padding(
              padding: EdgeInsets.symmetric(
                  horizontal: getProportionateScreenWidth(20)),
              child: SectionTitle(title: "Popular Products", press: () {}),
            ),
            SizedBox(height: getProportionateScreenWidth(20)),
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  ...List.generate(
                    snapshot.data!.length,
                    (index) {
                      if (snapshot.data![index].isPopular) {
                        return ProductCard(product: snapshot.data![index]);
                      }

                      return const SizedBox
                          .shrink(); // here by default width and height is 0
                    },
                  ),
                  SizedBox(width: getProportionateScreenWidth(20)),
                ],
              ),
            )
          ],
        );
      },
    );
  }
}

// class PopularProducts extends StatelessWidget {
//   @override
//   Widget build(BuildContext context) {
//     return Column(children: [
//       Center(
//         child: FutureBuilder<List<Product>>(
//           future: fetchProducts(http.Client()),
//           builder: (context, snapshot) {
//             if (snapshot.hasData) {
//               return Text("${snapshot.data!}");
//             } else if (snapshot.hasError) {
//               return Text("error");
//             }
//             return CircularProgressIndicator();
//           },
//         ),
//       ),
//     ]);
//   }
// }
