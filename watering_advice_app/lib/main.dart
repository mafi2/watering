import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(WateringAdviceApp());

class WateringAdviceApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Watering Advice',
      theme: ThemeData(primarySwatch: Colors.green),
      home: AdvicePage(),
    );
  }
}

class AdvicePage extends StatefulWidget {
  @override
  _AdvicePageState createState() => _AdvicePageState();
}

class _AdvicePageState extends State<AdvicePage> {
  List<dynamic>? data;
  String? error;

  Future<void> fetchAdvice() async {
  final url = Uri.parse(
    'https://raw.githubusercontent.com/mafi2/watering/refs/heads/main/data/weather_data.json',
  );

  try {
    final res = await http.get(url);
    if (res.statusCode == 200) {
      setState(() {
        data = json.decode(res.body) as List<dynamic>;
        error = null;
      });
    } else {
      setState(() {
        error = "Failed to load data (${res.statusCode})";
        data = null;
      });
    }
  } catch (e) {
    setState(() {
      error = "Error: $e";
      data = null;
    });
  }
}


  @override
  void initState() {
    super.initState();
    fetchAdvice();
  }

  @override
  Widget build(BuildContext context) {
    final prettyJson = data != null
        ? const JsonEncoder.withIndent('  ').convert(data)
        : null;

    return Scaffold(
      appBar: AppBar(title: Text("Today's Watering Advice")),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: error != null
              ? Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(error!, style: TextStyle(color: Colors.red)),
                    SizedBox(height: 10),
                    ElevatedButton(
                      onPressed: fetchAdvice,
                      child: Text("Retry"),
                    ),
                  ],
                )
              : SingleChildScrollView(
                  child: SelectableText(
                    prettyJson ?? "Loading...",
                    style: TextStyle(fontSize: 16, fontFamily: 'monospace'),
                  ),
                ),
        ),
      ),
    );
  }
}
