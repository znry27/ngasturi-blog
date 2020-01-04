import 'package:flutter/material.dart';

class WithoutHistory extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Navigation Without History'),
            ),
            body: Center(
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                        Text('After press back aplication will be closed')
                    ],
                ),
            ),
        );
    }
}