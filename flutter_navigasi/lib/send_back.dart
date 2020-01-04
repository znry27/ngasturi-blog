import 'package:flutter/material.dart';
import 'customer.dart';

class SendDataBack extends StatefulWidget {
    SendDataBack({Key key}) : super(key: key);

    @override
    _SendDataBackState createState() => _SendDataBackState();
}

class _SendDataBackState extends State<SendDataBack> {
    TextEditingController nameController = TextEditingController();
    TextEditingController addressController = TextEditingController();

    bool isValid(){
        if(nameController.text.isEmpty){
            return false;
        }

        if(addressController.text.isEmpty){
            return false;
        }

        return true;
    }

    sendData() {
        if(isValid()){
            // buat object customer dari input user
            Customer customer = Customer(nameController.text, addressController.text);
            // kirim object customer ke halaman sebelumnya
            Navigator.pop(context, customer);
        }else{
            return showDialog(
                context: context,
                builder: (context){
                    return AlertDialog(
                        content: Text('Please fill all field.'),
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
    }

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Send Data Back'),
                actions: <Widget>[
                    FlatButton(
                        onPressed: (){
                            sendData();
                        },
                        child: Text('Back'),
                    )
                ],
            ),
            body: Center(
                child: Padding(
                    padding: EdgeInsets.all(20),
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                            Text(
                                'Name'
                            ),
                            TextField(
                                controller: nameController,
                            ),
                            Padding(
                                padding: EdgeInsets.only(top: 20),
                            ),
                            Text(
                                'Address'
                            ),
                            TextField(
                                controller: addressController,
                            )
                        ],
                    ),
                )
            ),
        );
    }
}
