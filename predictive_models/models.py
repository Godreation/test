import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class PredictiveModels:
    def __init__(self):
        self.models = {
            'Linear Regression': LinearRegression(),
            'Decision Tree': DecisionTreeRegressor(random_state=42),
            'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'Support Vector Regression': SVR(kernel='rbf'),
            'K-Nearest Neighbors': KNeighborsRegressor(n_neighbors=5)
        }
        self.trained_models = {}
        self.metrics = {}
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """训练所有模型"""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            self.trained_models[name] = model
            
            # 预测测试集
            y_pred = model.predict(X_test)
            
            # 计算评估指标
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            self.metrics[name] = {
                'MSE': mse,
                'R2': r2,
                'y_test': y_test,
                'y_pred': y_pred
            }
        
        return X_train, X_test, y_train, y_test
    
    def predict(self, X, model_name):
        """使用指定模型进行预测"""
        if model_name in self.trained_models:
            return self.trained_models[model_name].predict(X)
        else:
            raise ValueError(f"Model {model_name} not trained yet!")
    
    def get_metrics(self):
        """获取所有模型的评估指标"""
        return self.metrics
    
    def get_best_model(self, metric='R2'):
        """获取表现最好的模型"""
        if not self.metrics:
            raise ValueError("No models trained yet!")
        
        if metric == 'R2':
            best_model = max(self.metrics, key=lambda x: self.metrics[x][metric])
        elif metric == 'MSE':
            best_model = min(self.metrics, key=lambda x: self.metrics[x][metric])
        else:
            raise ValueError(f"Metric {metric} not supported!")
        
        return best_model, self.metrics[best_model]