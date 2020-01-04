import 'package:flutter/material.dart';
import 'customer.dart';

class ReceiptData extends StatefulWidget {
    // property
    final Customer customer;

    // constructor
    ReceiptData({Key key, @required this.customer}) : super(key: key);

    @override
    _ReceiptDataState createState() => _ReceiptDataState(customer: customer);
}

class _ReceiptDataState extends State<ReceiptData> {
    // property
    Customer customer;

    // constructor
    _ReceiptDataState({@required this.customer}) : super();

    @override
    Widget build(BuildContext context) {
        return Scaffold(
            appBar: AppBar(
                title: Text('Receipt Data'),
            ),
            body: Center(
                child: Padding(
                    padding: EdgeInsets.all(20),
                    child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: <Widget>[
                            Text(
                                'Inserted Customer : '
                            ),
                            Text(
                                'Name: ' + customer.name
                            ),
                            Text(
                                'Address: ' + customer.address
                            ),
                        ],
                    ),
                )
            ),
        );
    }
}
