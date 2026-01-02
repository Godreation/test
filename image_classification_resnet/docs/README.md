# 基于PyTorch的残差CNN图像分类项目

## 项目结构

```
image_classification_resnet/
├── env/              # 环境配置和依赖
├── src/              # 项目源代码
│   ├── model.py      # ResNet模型定义
│   ├── train.py      # 训练脚本
│   ├── visualize.py  # 结果可视化脚本
│   └── requirements.txt  # 依赖列表
└── docs/             # 开发记录和文档
```

## 项目说明

本项目使用PyTorch框架构建了一个基于残差网络（ResNet）的图像分类模型，用于对CIFAR-10数据集进行分类。

### 主要功能

1. **残差网络模型**：实现了ResNet-18和ResNet-34模型
2. **数据增强**：使用随机裁剪、水平翻转等数据增强技术
3. **模型训练**：支持SGD优化器、学习率调度器
4. **结果可视化**：
   - 训练曲线（损失和准确率）
   - 混淆矩阵
   - 错误分类样本展示
   - 分类报告

## 环境配置

### 安装依赖

```bash
# 在src目录下执行
pip install -r requirements.txt
```

### 启用Windows长路径支持（如果需要）

如果遇到长路径错误，请按照以下步骤启用Windows长路径支持：

1. 打开注册表编辑器（regedit）
2. 导航到：`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem`
3. 将`LongPathsEnabled`键值设置为`1`
4. 重启电脑

## 使用说明

### 1. 训练模型

```bash
# 在src目录下执行
python train.py
```

训练参数说明：
- 数据集：CIFAR-10
- 批次大小：128
- 学习率：0.1（每20个epoch衰减为原来的1/10）
- 训练轮次：50
- 模型保存：每10个epoch保存一次模型

### 2. 可视化结果

```bash
# 在src目录下执行
python visualize.py
```

可视化内容：
- 训练损失和准确率曲线
- 混淆矩阵
- 16个错误分类的样本
- 分类报告（按类别）

## 模型结构

### ResNet-18

- 输入：3×32×32 RGB图像
- 输出：10个类别
- 层数：18层（包含卷积层、全连接层）
- 残差块：BasicBlock

### ResNet-34

- 输入：3×32×32 RGB图像
- 输出：10个类别
- 层数：34层
- 残差块：BasicBlock

## 预期结果

在CIFAR-10数据集上，ResNet-18模型预期可以达到约90%以上的测试准确率。

## 文件说明

- `model.py`：定义了ResNet模型结构
- `train.py`：模型训练和验证脚本
- `visualize.py`：结果可视化和报告生成脚本
- `requirements.txt`：项目依赖列表

## 扩展建议

1. 尝试使用更大的ResNet模型（如ResNet-50、ResNet-101）
2. 使用其他数据集（如CIFAR-100、ImageNet）
3. 添加更多数据增强技术
4. 尝试不同的优化器（如Adam、AdamW）
5. 实现模型剪枝和量化

## 开发记录

- 2026-01-02：创建项目结构和基本代码
- 2026-01-02：实现ResNet模型和训练脚本
- 2026-01-02：添加结果可视化功能
