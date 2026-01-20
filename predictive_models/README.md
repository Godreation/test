# Predictive Models Project

This project implements several classic predictive models using Python, along with evaluation and visualization capabilities.

## Project Structure

```
predictive_models/
├── venv/                # Virtual environment
├── models.py            # Predictive models implementation
├── dataset.py           # Dataset generation and loading
├── evaluate_models.py   # Model evaluation
├── visualize_results.py # Result visualization
├── model_evaluation_results.csv # Evaluation results
└── README.md            # This file
```

## Virtual Environment Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install numpy pandas scikit-learn matplotlib seaborn jupyter
   ```

## Supported Models

This project implements the following predictive models:

- **Linear Regression**
- **Decision Tree Regression**
- **Random Forest Regression**
- **Support Vector Regression (SVR)**
- **K-Nearest Neighbors Regression**

## Dataset Support

The project supports multiple datasets for model evaluation:

1. **Synthetic Data**: Generated programmatically with customizable parameters
2. **Boston Housing Data**: Historical housing prices in Boston
3. **Diabetes Data**: Diabetes progression dataset
4. **Custom Data**: Load your own CSV data

## Usage

### 1. Generate/Load Dataset

```python
from dataset import DatasetGenerator

# Generate synthetic data
X, y = DatasetGenerator.generate_synthetic_data(n_samples=1000, n_features=10)

# Load built-in dataset
X, y = DatasetGenerator.load_diabetes()

# Load custom CSV data
X, y = DatasetGenerator.load_custom_data('your_data.csv')
```

### 2. Train and Evaluate Models

```python
from evaluate_models import ModelEvaluator

# Initialize evaluator
evaluator = ModelEvaluator()

# Evaluate on synthetic data
metrics, best_model, results_df = evaluator.evaluate_on_synthetic_data()

# Evaluate on diabetes data
metrics, best_model, results_df = evaluator.evaluate_on_diabetes()
```

### 3. Visualize Results

```python
from visualize_results import ResultVisualizer
from models import PredictiveModels
from dataset import DatasetGenerator

# Train models
models = PredictiveModels()
X, y = DatasetGenerator.generate_synthetic_data()
X_train, X_test, y_train, y_test = models.train(X, y)

# Generate visualizations
visualizer = ResultVisualizer()
metrics = models.get_metrics()

# Plot model comparison
visualizer.plot_model_comparison(metrics)

# Plot actual vs predicted for a specific model
visualizer.plot_actual_vs_predicted(metrics, 'Random Forest')

# Plot residuals for a specific model
visualizer.plot_residuals(metrics, 'Linear Regression')

# Generate all plots at once
trained_models = models.trained_models
visualizer.generate_all_plots(metrics, trained_models, X_train)
```

## Example Workflow

```python
from evaluate_models import ModelEvaluator
from visualize_results import ResultVisualizer

# Step 1: Evaluate models
evaluator = ModelEvaluator()
metrics, best_model, results_df = evaluator.evaluate_on_synthetic_data()

# Step 2: Visualize results
visualizer = ResultVisualizer()
visualizer.generate_all_plots(
    metrics=metrics,
    trained_models=evaluator.models.trained_models,
    X_train=evaluator.models._X_train  # Access X_train from the trained models
)
```

## Evaluation Metrics

The project computes the following evaluation metrics for each model:

- **Mean Squared Error (MSE)**: Measures the average squared difference between predictions and actual values
- **R² Score**: Indicates how well the model explains the variance in the data (0-1, higher is better)

## Visualization Types

1. **Model Comparison**: Bar charts comparing MSE and R² scores across all models
2. **Actual vs Predicted**: Scatter plots showing how well predictions match actual values
3. **Residual Distribution**: Histograms of prediction errors
4. **Feature Importance**: Horizontal bar charts showing which features contribute most to predictions (for tree-based models)

## Results Storage

- Evaluation results are saved to `model_evaluation_results.csv`
- Visualization plots can be saved to the `plots/` directory by specifying the `save_dir` parameter

## Customization

### Custom Dataset Format

Your custom CSV file should have:
- Features in columns 1 to n-1
- Target variable in the last column
- No missing values (or handle them before loading)

### Model Parameters

You can customize model parameters in the `models.py` file by modifying the `__init__` method of the `PredictiveModels` class.

## Requirements

- Python 3.7+
- numpy
- pandas
- scikit-learn
- matplotlib
- seaborn
- jupyter (optional, for interactive development)

## License

This project is open source and available under the MIT License.

## Notes

- The Boston Housing dataset may require additional installation steps due to licensing restrictions
- For large datasets, consider adjusting the `n_samples` parameter to reduce computation time
- Model performance may vary significantly depending on the dataset characteristics
- Always validate models on unseen data to avoid overfitting

## Contributing

Feel free to contribute to this project by adding new models, improving existing code, or enhancing visualization capabilities.
