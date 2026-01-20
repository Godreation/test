from models import PredictiveModels
from dataset import DatasetGenerator
from visualize_results import ResultVisualizer

# 生成合成数据
dataset_gen = DatasetGenerator()
X, y = dataset_gen.generate_synthetic_data(n_samples=500, n_features=8, noise=0.2)

# 训练模型
models = PredictiveModels()
X_train, X_test, y_train, y_test = models.train(X, y)
metrics = models.get_metrics()
trained_models = models.trained_models

# 初始化可视化器
visualizer = ResultVisualizer()

print("Generating visualization plots...")

# 生成所有图表
visualizer.generate_all_plots(metrics, trained_models, X_train, save_dir='test_plots')

print("All plots generated successfully!")
print("Plots saved in 'test_plots' directory.")

# 测试从结果文件绘制图表
print("\nTesting plot generation from results file...")
visualizer.plot_from_results_file('model_evaluation_results.csv', save_path='test_results_plot')

print("\nVisualization test completed successfully!")