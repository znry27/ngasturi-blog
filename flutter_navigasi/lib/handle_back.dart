import 'package:flutter/material.dart';

class HandleBack extends StatelessWidget {
    Future<bool> onBackButton(context) async {
        // tampilkan dialog saat user menekan tombol back
        // jika ditekan ok maka akan kembali ke halaman sebelumnya
        return showDialog(
            context: context,
            builder: (context){
                return AlertDialog(
                    title: Text('Back'),
                    content: Text('Are you sure want to back to previous page ?'),
                    actions: <Widget>[
                        FlatButton(
                            onPressed: () {
                                // tutup modal dan halaman ini
                                Navigator.of(context).pop(true);
                            },
                            child: Text('OK'),
                        ),
                        FlatButton(
                            onPressed: () {
                                // tutup modal saja
                                Navigator.of(context).pop(false);
                            },
                            child: Text('NO'),
                        )
                    ],
                );
            }
        );
    }

    @override
    Widget build(BuildContext context) {
        return WillPopScope(
            onWillPop: (){
                // panggil method onBackButton saat user menekan tombol back
                return onBackButton(context);
            },
            child: Scaffold(
                appBar: AppBar(
                    title: Text('Handle Back'),
                ),
                body: Center(
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: <Widget>[
                            Text('Try press back button')
                        ],
                    ),
                ),
            ),
        );
    }
}