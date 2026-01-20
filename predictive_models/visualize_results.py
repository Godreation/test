import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

sns.set(style="whitegrid")

class ResultVisualizer:
    def __init__(self):
        plt.rcParams.update({'font.size': 12})
    
    def plot_model_comparison(self, metrics, save_path=None):
        """绘制模型性能对比图"""
        models = list(metrics.keys())
        mse_values = [metrics[model]['MSE'] for model in models]
        r2_values = [metrics[model]['R2'] for model in models]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 绘制MSE对比
        bars1 = ax1.bar(models, mse_values, color='skyblue')
        ax1.set_title('Model Comparison - Mean Squared Error')
        ax1.set_xlabel('Models')
        ax1.set_ylabel('MSE')
        ax1.tick_params(axis='x', rotation=45)
        
        # 在柱子上显示数值
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height, f'{height:.4f}',
                    ha='center', va='bottom')
        
        # 绘制R2对比
        bars2 = ax2.bar(models, r2_values, color='lightgreen')
        ax2.set_title('Model Comparison - R2 Score')
        ax2.set_xlabel('Models')
        ax2.set_ylabel('R2')
        ax2.tick_params(axis='x', rotation=45)
        
        # 在柱子上显示数值
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height, f'{height:.4f}',
                    ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Model comparison plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_actual_vs_predicted(self, metrics, model_name, save_path=None):
        """绘制实际值与预测值对比图"""
        y_test = metrics[model_name]['y_test']
        y_pred = metrics[model_name]['y_pred']
        
        plt.figure(figsize=(10, 6))
        
        # 绘制散点图
        plt.scatter(y_test, y_pred, alpha=0.6, color='blue', label='Predicted vs Actual')
        
        # 绘制理想线
        min_val = min(min(y_test), min(y_pred))
        max_val = max(max(y_test), max(y_pred))
        plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='Ideal Line')
        
        plt.title(f'{model_name} - Actual vs Predicted Values')
        plt.xlabel('Actual Values')
        plt.ylabel('Predicted Values')
        plt.legend()
        plt.grid(True)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Actual vs Predicted plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_residuals(self, metrics, model_name, save_path=None):
        """绘制残差图"""
        y_test = metrics[model_name]['y_test']
        y_pred = metrics[model_name]['y_pred']
        residuals = y_test - y_pred
        
        plt.figure(figsize=(10, 6))
        
        # 绘制残差分布直方图
        plt.hist(residuals, bins=30, alpha=0.7, color='purple', edgecolor='black')
        plt.axvline(x=0, color='red', linestyle='--', label='Zero Residual')
        
        plt.title(f'{model_name} - Residual Distribution')
        plt.xlabel('Residuals')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, axis='y')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Residual plot saved to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def plot_feature_importance(self, model, X_train, save_path=None):
        """绘制特征重要性图"""
        if hasattr(model, 'feature_importances_'):
            feature_importance = model.feature_importances_
            feature_names = X_train.columns
            
            # 排序
            sorted_idx = np.argsort(feature_importance)
            sorted_features = feature_names[sorted_idx]
            sorted_importance = feature_importance[sorted_idx]
            
            plt.figure(figsize=(10, 8))
            
            # 绘制水平条形图
            plt.barh(sorted_features, sorted_importance, color='orange')
            plt.title('Feature Importance')
            plt.xlabel('Importance Score')
            plt.ylabel('Features')
            plt.grid(True, axis='x')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Feature importance plot saved to {save_path}")
            else:
                plt.show()
            
            plt.close()
        else:
            print("Model does not support feature importance!")
    
    def plot_all_models_actual_vs_predicted(self, metrics, save_dir=None):
        """绘制所有模型的实际值与预测值对比图"""
        for model_name in metrics.keys():
            if save_dir:
                save_path = f"{save_dir}/{model_name.replace(' ', '_')}_actual_vs_predicted.png"
            else:
                save_path = None
            
            self.plot_actual_vs_predicted(metrics, model_name, save_path)
    
    def generate_all_plots(self, metrics, trained_models, X_train, save_dir='plots'):
        """生成所有可视化图表"""
        import os
        
        # 创建保存目录
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # 1. 模型性能对比图
        self.plot_model_comparison(metrics, save_path=f"{save_dir}/model_comparison.png")
        
        # 2. 每个模型的实际值vs预测值
        for model_name in metrics.keys():
            self.plot_actual_vs_predicted(metrics, model_name, 
                                        save_path=f"{save_dir}/{model_name.replace(' ', '_')}_actual_vs_predicted.png")
            
            # 3. 每个模型的残差图
            self.plot_residuals(metrics, model_name, 
                              save_path=f"{save_dir}/{model_name.replace(' ', '_')}_residuals.png")
        
        # 4. 特征重要性图（仅对支持的模型）
        for model_name, model in trained_models.items():
            if hasattr(model, 'feature_importances_'):
                self.plot_feature_importance(model, X_train, 
                                           save_path=f"{save_dir}/{model_name.replace(' ', '_')}_feature_importance.png")
    
    def plot_from_results_file(self, results_file, save_path=None):
        """从保存的评估结果文件绘制图表"""
        try:
            df = pd.read_csv(results_file)
            
            # 按数据分组
            for data_name, group in df.groupby('Data'):
                plt.figure(figsize=(15, 6))
                
                # 绘制MSE对比
                plt.subplot(1, 2, 1)
                bars1 = plt.bar(group['Model'], group['MSE'], color='skyblue')
                plt.title(f'{data_name} - Mean Squared Error')
                plt.xlabel('Models')
                plt.ylabel('MSE')
                plt.xticks(rotation=45)
                
                for bar in bars1:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.4f}',
                            ha='center', va='bottom')
                
                # 绘制R2对比
                plt.subplot(1, 2, 2)
                bars2 = plt.bar(group['Model'], group['R2'], color='lightgreen')
                plt.title(f'{data_name} - R2 Score')
                plt.xlabel('Models')
                plt.ylabel('R2')
                plt.xticks(rotation=45)
                
                for bar in bars2:
                    height = bar.get_height()
                    plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.4f}',
                            ha='center', va='bottom')
                
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(f"{save_path}_{data_name.replace(' ', '_')}.png", dpi=300, bbox_inches='tight')
                    print(f"Plot saved to {save_path}_{data_name.replace(' ', '_')}.png")
                else:
                    plt.show()
                
                plt.close()
        except Exception as e:
            print(f"Error plotting from results file: {e}")