import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Nigeria GDP Predictor',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const GDPPredictorScreen(),
    );
  }
}

class GDPPredictorScreen extends StatefulWidget {
  const GDPPredictorScreen({super.key});

  @override
  State<GDPPredictorScreen> createState() => _GDPPredictorScreenState();
}

class _GDPPredictorScreenState extends State<GDPPredictorScreen> {
  final _yearController = TextEditingController();
  String _prediction = '';
  bool _isLoading = false;
  String _selectedModel = 'linear';
  String _error = '';

  Future<void> _getPrediction() async {
    if (_yearController.text.isEmpty) {
      setState(() {
        _error = 'Please enter a year';
      });
      return;
    }

    final year = int.tryParse(_yearController.text);
    if (year == null || year < 2024 || year > 2050) {
      setState(() {
        _error = 'Please enter a valid year between 2024 and 2050';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _error = '';
    });

    try {
      final response = await http.post(
        Uri.parse(
            'https://nigeria-gdp-linear-regression-model.onrender.com/predict'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'year': year, 'model_type': _selectedModel}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _prediction = '\$${data['predicted_gdp'].toStringAsFixed(2)}';
          _error = '';
        });
      } else {
        setState(() {
          _error = 'Failed to get prediction';
        });
      }
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.green,
        title: const Text(
          'Nigerian GDP Per Capita Predictor',
          style: TextStyle(color: Colors.white, fontSize: 20),
        ),
        centerTitle: true,
      ),
      body: Container(
        color: Colors.white,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              TextField(
                controller: _yearController,
                decoration: InputDecoration(
                  labelText: 'Enter Year (2024-2050)',
                  border: const OutlineInputBorder(),
                  hintText: 'e.g., 2025',
                  filled: true,
                  fillColor: Colors.white,
                  labelStyle: TextStyle(color: Colors.green[700]),
                  focusedBorder: OutlineInputBorder(
                    borderSide:
                        BorderSide(color: Colors.green[700]!, width: 2.0),
                  ),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.symmetric(horizontal: 12),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: DropdownButton<String>(
                  value: _selectedModel,
                  isExpanded: true,
                  underline: Container(),
                  items: const [
                    DropdownMenuItem(
                      value: 'linear',
                      child: Text('Linear Model'),
                    ),
                    DropdownMenuItem(
                      value: 'rf',
                      child: Text('Random Forest Model'),
                    ),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() {
                        _selectedModel = value;
                      });
                    }
                  },
                ),
              ),
              const SizedBox(height: 20),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green,
                    padding: const EdgeInsets.all(16),
                  ),
                  onPressed: _isLoading ? null : _getPrediction,
                  child: _isLoading
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text(
                          'Predict',
                          style: TextStyle(fontSize: 18, color: Colors.white),
                        ),
                ),
              ),
              const SizedBox(height: 30),
              // Display Area
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: _error.isEmpty
                      ? Colors.green.withOpacity(0.1)
                      : Colors.red.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(
                    color: _error.isEmpty ? Colors.green : Colors.red,
                    width: 1,
                  ),
                ),
                child: Column(
                  children: [
                    Text(
                      'Prediction Results',
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: _error.isEmpty ? Colors.green[700] : Colors.red,
                      ),
                    ),
                    const SizedBox(height: 10),
                    if (_prediction.isNotEmpty && _error.isEmpty)
                      Text(
                        'Predicted GDP Per Capita: $_prediction',
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.green[700],
                        ),
                      ),
                    if (_error.isNotEmpty)
                      Text(
                        _error,
                        style: const TextStyle(
                          color: Colors.red,
                          fontSize: 16,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    if (_prediction.isEmpty && _error.isEmpty)
                      Text(
                        'Enter a year and select a model to see prediction',
                        style: TextStyle(
                          color: Colors.grey[600],
                          fontSize: 16,
                        ),
                        textAlign: TextAlign.center,
                      ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _yearController.dispose();
    super.dispose();
  }
}
