import 'package:flutter/material.dart';

class Simple extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Simple Page'),
            ),
            body: Center(
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                        Text('Simple Page. Please press back button')
                    ],
                ),
            ),
        );
    }
}