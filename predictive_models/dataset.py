import numpy as np
import pandas as pd
from sklearn.datasets import make_regression, load_diabetes

class DatasetGenerator:
    @staticmethod
    def generate_synthetic_data(n_samples=1000, n_features=10, noise=0.1, random_state=42):
        """生成合成回归数据集"""
        X, y = make_regression(n_samples=n_samples, n_features=n_features, noise=noise, random_state=random_state)
        
        # 转换为DataFrame以便于处理
        columns = [f'feature_{i}' for i in range(n_features)]
        X_df = pd.DataFrame(X, columns=columns)
        y_df = pd.Series(y, name='target')
        
        return X_df, y_df
    
    @staticmethod
    def load_boston():
        """加载波士顿房价数据集（替代方案，因为原数据集已被移除）"""
        print("Boston dataset is no longer available due to ethical issues. Using California housing dataset instead.")
        from sklearn.datasets import fetch_california_housing
        california = fetch_california_housing()
        X_df = pd.DataFrame(california.data, columns=california.feature_names)
        y_df = pd.Series(california.target, name='MEDV')
        return X_df, y_df
    
    @staticmethod
    def load_diabetes():
        """加载糖尿病数据集"""
        diabetes = load_diabetes()
        X_df = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        y_df = pd.Series(diabetes.target, name='target')
        return X_df, y_df
    
    @staticmethod
    def load_custom_data(file_path):
        """加载自定义CSV数据"""
        try:
            df = pd.read_csv(file_path)
            # 假设最后一列是目标变量
            X_df = df.iloc[:, :-1]
            y_df = df.iloc[:, -1]
            return X_df, y_df
        except Exception as e:
            raise ValueError(f"Error loading custom data: {e}")
    
    @staticmethod
    def save_data(X, y, file_path):
        """保存数据到CSV文件"""
        df = pd.concat([X, pd.Series(y, name='target')], axis=1)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")

# 示例用法
if __name__ == "__main__":
    # 生成合成数据
    X_synth, y_synth = DatasetGenerator.generate_synthetic_data()
    print("Synthetic data generated:")
    print(f"X shape: {X_synth.shape}, y shape: {y_synth.shape}")
    print(X_synth.head())
    print(y_synth.head())
    
    # 加载糖尿病数据
    X_diabetes, y_diabetes = DatasetGenerator.load_diabetes()
    print("\nDiabetes data loaded:")
    print(f"X shape: {X_diabetes.shape}, y shape: {y_diabetes.shape}")
    print(X_diabetes.head())
    print(y_diabetes.head())
    
    # 保存合成数据到文件
    DatasetGenerator.save_data(X_synth, y_synth, 'synthetic_data.csv')