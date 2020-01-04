import 'package:flutter/material.dart';
import 'simple.dart';
import 'without_history.dart';
import 'handle_back.dart';
import 'collect_data.dart';
import 'send_back.dart';
import 'customer.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
    // This widget is the root of your application.
    @override
    Widget build(BuildContext context) {
        return MaterialApp(
            theme: ThemeData(
                primarySwatch: Colors.blue,
            ),
            home: MyHomePage(),
        );
    }
}

class MyHomePage extends StatefulWidget {
    MyHomePage({Key key}) : super(key: key);

    @override
    _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

    waitForData() async {
        // pada dasarnya method Navigator.push return Future
        // jadi kita bisa menggunakan await untuk mendapatkan data sebenarnya
        // bisa juga menggunakan method then()
        Customer customer = await Navigator.push(context, MaterialPageRoute(builder: (context) => SendDataBack()));

        String content = '';

        // cek data yang diterima null atau tidak
        // jika user menekan tombol back data akan bernilai null
        if(customer != null){
            content = 'You insert Name : ${customer.name} and Address : ${customer.address}';
        }else{
            content = 'Please insert Name and Address';
        }
        return showDialog(
            context: context,
            builder: (context){
                return AlertDialog(
                    content: Text(content),
                    actions: <Widget>[
                        FlatButton(
                            onPressed: () {
                                Navigator.pop(context);
                            },
                            child: Text('OK'),
                        ),
                    ],
                );
            }
        );
    }
    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Tutorial Navigasi'),
            ),
            body: Center(
                child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                        FlatButton(
                            onPressed: () {
                                // pindah ke halaman simple
                                Navigator.push(context, MaterialPageRoute(builder: (context) => Simple()));
                            },
                            child: Text(
                                'Basic Navigation',
                                style: TextStyle(
                                    color: Colors.white
                                ),
                            ),
                            color: Colors.green,
                        ),
                        FlatButton(
                            onPressed: () {
                                // pindah ke halaman WithoutHistory
                                // tapi tidak menyimpan halaman saat ini
                                Navigator.pushReplacement(context, MaterialPageRoute(builder: (context) => WithoutHistory()));
                            },
                            child: Text(
                                'Navigation Without History',
                                style: TextStyle(
                                    color: Colors.white
                                ),
                            ),
                            color: Colors.green,
                        ),
                        FlatButton(
                            onPressed: () {
                                Navigator.push(context, MaterialPageRoute(builder: (context) => HandleBack()));
                            },
                            child: Text(
                                'Handle Back',
                                style: TextStyle(
                                    color: Colors.white
                                ),
                            ),
                            color: Colors.green,
                        ),
                        FlatButton(
                            onPressed: () {
                                Navigator.push(context, MaterialPageRoute(builder: (context) => CollectData()));
                            },
                            child: Text(
                                'Send Data',
                                style: TextStyle(
                                    color: Colors.white
                                ),
                            ),
                            color: Colors.green,
                        ),
                        FlatButton(
                            onPressed: () {
                                waitForData();
                            },
                            child: Text(
                                'Receive Data',
                                style: TextStyle(
                                    color: Colors.white
                                ),
                            ),
                            color: Colors.green,
                        ),
                    ],
                ),
            ),
        );
    }
}
