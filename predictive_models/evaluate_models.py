import pandas as pd
from models import PredictiveModels
from dataset import DatasetGenerator

class ModelEvaluator:
    def __init__(self):
        self.models = PredictiveModels()
        self.dataset_generator = DatasetGenerator()
    
    def evaluate_on_synthetic_data(self, n_samples=1000, n_features=10, noise=0.1):
        """在合成数据上评估模型"""
        print("Generating synthetic data...")
        X, y = self.dataset_generator.generate_synthetic_data(n_samples=n_samples, n_features=n_features, noise=noise)
        print(f"Generated data with shape: X={X.shape}, y={y.shape}")
        
        return self._evaluate(X, y, "Synthetic Data")
    
    def evaluate_on_boston(self):
        """在波士顿房价数据上评估模型"""
        print("Loading Boston dataset...")
        X, y = self.dataset_generator.load_boston()
        print(f"Loaded Boston data with shape: X={X.shape}, y={y.shape}")
        
        return self._evaluate(X, y, "Boston Housing Data")
    
    def evaluate_on_diabetes(self):
        """在糖尿病数据上评估模型"""
        print("Loading Diabetes dataset...")
        X, y = self.dataset_generator.load_diabetes()
        print(f"Loaded Diabetes data with shape: X={X.shape}, y={y.shape}")
        
        return self._evaluate(X, y, "Diabetes Data")
    
    def evaluate_on_custom_data(self, file_path):
        """在自定义数据上评估模型"""
        print(f"Loading custom data from {file_path}...")
        X, y = self.dataset_generator.load_custom_data(file_path)
        print(f"Loaded custom data with shape: X={X.shape}, y={y.shape}")
        
        return self._evaluate(X, y, "Custom Data")
    
    def _evaluate(self, X, y, data_name):
        """内部评估方法"""
        print(f"\nTraining models on {data_name}...")
        X_train, X_test, y_train, y_test = self.models.train(X, y)
        
        print(f"\n{'='*50}")
        print(f"Model Evaluation Results on {data_name}")
        print(f"{'='*50}")
        
        metrics = self.models.get_metrics()
        results = []
        
        for model_name, metric in metrics.items():
            print(f"\n{model_name}:")
            print(f"  MSE: {metric['MSE']:.4f}")
            print(f"  R2 Score: {metric['R2']:.4f}")
            
            results.append({
                'Model': model_name,
                'Data': data_name,
                'MSE': metric['MSE'],
                'R2': metric['R2']
            })
        
        # 找到最佳模型
        best_model_name, best_model_metrics = self.models.get_best_model()
        print(f"\n{'='*50}")
        print(f"Best Model based on R2 Score: {best_model_name}")
        print(f"MSE: {best_model_metrics['MSE']:.4f}")
        print(f"R2 Score: {best_model_metrics['R2']:.4f}")
        print(f"{'='*50}")
        
        # 保存评估结果
        results_df = pd.DataFrame(results)
        results_df.to_csv('model_evaluation_results.csv', index=False)
        print("\nEvaluation results saved to model_evaluation_results.csv")
        
        return metrics, best_model_name, results_df
    
    def compare_models(self, metrics):
        """比较不同模型的性能"""
        print("\nModel Comparison:")
        print("-" * 30)
        
        # 按R2分数排序
        sorted_models = sorted(metrics.items(), key=lambda x: x[1]['R2'], reverse=True)
        
        for i, (model_name, metric) in enumerate(sorted_models, 1):
            print(f"{i}. {model_name}: R2 = {metric['R2']:.4f}, MSE = {metric['MSE']:.4f}")

# 示例用法
if __name__ == "__main__":
    evaluator = ModelEvaluator()
    
    # 在合成数据上评估
    metrics, best_model, results_df = evaluator.evaluate_on_synthetic_data()
    
    # 在糖尿病数据上评估
    # metrics, best_model, results_df = evaluator.evaluate_on_diabetes()
    
    # 比较模型
    evaluator.compare_models(metrics)