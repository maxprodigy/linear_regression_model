# Linear Regression Model 
# Nigeria GDP Per Capita Predictor

A machine learning project that predicts Nigeria's GDP Per Capita using Linear Regression and Random Forest models, deployed with FastAPI and a Flutter mobile application.

## Project Components

1. **Machine Learning Models**
   - Linear Regression Model
   - Random Forest Model
   - Data source: World Bank Nigeria Statistics (2000-2020) [Link](https://www.kaggle.com/datasets/mutindafestus/world-statistics-dataset-from-world-bank)
   - Extracted Nigerian Dataset With Python [Link](https://docs.google.com/spreadsheets/d/1XbH2jp8tDylk2nGXRoy7xrtd0Es0BUkLvYvuNHRn2BM/edit?usp=sharing)
   - Features: Year
   - Target: GDP Per Capita (USD)

2. **API Endpoint**
   - URL: https://nigeria-gdp-linear-regression-model.onrender.com/docs
   - Swagger UI Documentation Available
   - Accepts POST requests with:
     ```json
     {
       "year": 2024,
       "model_type": "linear"
     }
     ```
   - Returns predictions in format:
     ```json
     {
       "year": 2024,
       "predicted_gdp": 3231.69
     }
     ```

3. **Mobile Application**
   - Built with Flutter
   - Features:
     - Year input (2024-2050)
     - Model selection (Linear/Random Forest)
     - Real-time predictions
     - Error handling and validation

## Running the Mobile App

1. Prerequisites:
   - Flutter SDK installed
   - Android Studio/VS Code with Flutter extensions
   - An Android/iOS emulator or physical device

2. Installation:
   ```bash
   # Clone the repository
   git clone https://github.com/maxprodigy/linear_regression_model.git
   cd linear_regression_model.git
   # Install dependencies
   flutter pub get

   # Run the app
   flutter run
   ```

3. Using the App:
   - Enter a year between 2024 and 2050
   - Select prediction model (Linear or Random Forest)
   - Click "Predict" to get GDP forecast
   - View results in the prediction area

## Demo Video

[Link to YouTube Demo](https://youtu.be/ER-fepmiVhM)

## API Usage

Test the API directly through Swagger UI:
1. Visit https://nigeria-gdp-linear-regression-model.onrender.com/docs
2. Navigate to POST /predict endpoint
3. Click "Try it out"
4. Input test values:
   ```json
   {
     "year": 2025,
     "model_type": "linear"
   }
   ```
5. Click "Execute"

## Error Handling

The application handles various error cases:
- Invalid year input
- Network errors
- Server errors
- Missing values
- Out of range predictions

## Contributors
- Peter Johnson
