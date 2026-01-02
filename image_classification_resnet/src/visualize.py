import torch
import torchvision
import torchvision.transforms as transforms
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import os
from model import resnet18

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 数据预处理
transforms_test = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
])

# 加载CIFAR-10测试集
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transforms_test)
testloader = torch.utils.data.DataLoader(testset, batch_size=100, shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 创建保存结果的目录
os.makedirs('./results', exist_ok=True)

# 加载模型
def load_model():
    model = resnet18(num_classes=10).to(device)
    checkpoint = torch.load('./checkpoints/resnet18_final.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    train_losses = checkpoint.get('train_losses', [])
    train_accs = checkpoint.get('train_accs', [])
    test_losses = checkpoint.get('test_losses', [])
    test_accs = checkpoint.get('test_accs', [])
    
    return model, train_losses, train_accs, test_losses, test_accs

# 绘制训练曲线
def plot_training_curves(train_losses, train_accs, test_losses, test_accs):
    epochs = range(1, len(train_losses) + 1)
    
    plt.figure(figsize=(12, 5))
    
    # 绘制损失曲线
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_losses, 'b-', label='Training Loss')
    plt.plot(epochs, test_losses, 'r-', label='Test Loss')
    plt.title('Loss vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True)
    
    # 绘制准确率曲线
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accs, 'b-', label='Training Accuracy')
    plt.plot(epochs, test_accs, 'r-', label='Test Accuracy')
    plt.title('Accuracy vs. Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('./results/training_curves.png', dpi=300, bbox_inches='tight')
    print('Training curves saved to ./results/training_curves.png')

# 计算混淆矩阵
def calculate_confusion_matrix(model):
    all_preds = []
    all_targets = []
    
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())
    
    cm = confusion_matrix(all_targets, all_preds)
    return cm, all_preds, all_targets

# 绘制混淆矩阵
def plot_confusion_matrix(cm):
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('./results/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print('Confusion matrix saved to ./results/confusion_matrix.png')

# 展示错误分类的样本
def show_misclassified_samples(model, all_preds, all_targets):
    # 获取错误分类的索引
    misclassified_idx = np.where(np.array(all_preds) != np.array(all_targets))[0]
    
    # 随机选择16个错误分类的样本
    if len(misclassified_idx) >= 16:
        selected_idx = np.random.choice(misclassified_idx, 16, replace=False)
    else:
        selected_idx = misclassified_idx
    
    # 加载原始测试集（不进行归一化，用于可视化）
    transforms_visualize = transforms.Compose([
        transforms.ToTensor(),
    ])
    
    testset_visualize = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transforms_visualize)
    
    plt.figure(figsize=(12, 12))
    
    for i, idx in enumerate(selected_idx):
        img, true_label = testset_visualize[idx]
        pred_label = all_preds[idx]
        
        plt.subplot(4, 4, i+1)
        plt.imshow(np.transpose(img.numpy(), (1, 2, 0)))
        plt.title(f'True: {classes[true_label]}\nPred: {classes[pred_label]}')
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('./results/misclassified_samples.png', dpi=300, bbox_inches='tight')
    print('Misclassified samples saved to ./results/misclassified_samples.png')

# 计算分类报告
def print_classification_report(cm):
    class_acc = cm.diagonal() / cm.sum(axis=1) * 100
    
    print('Classification Report by Class:')
    print('-' * 40)
    for i, cls in enumerate(classes):
        print(f'{cls:<10}: {class_acc[i]:.2f}%')
    print('-' * 40)
    print(f'Overall Acc: {np.mean(class_acc):.2f}%')
    
    # 保存分类报告到文件
    with open('./results/classification_report.txt', 'w') as f:
        f.write('Classification Report by Class:\n')
        f.write('-' * 40 + '\n')
        for i, cls in enumerate(classes):
            f.write(f'{cls:<10}: {class_acc[i]:.2f}%\n')
        f.write('-' * 40 + '\n')
        f.write(f'Overall Acc: {np.mean(class_acc):.2f}%\n')
    
    print('Classification report saved to ./results/classification_report.txt')

# 主函数
def main():
    print('Loading model...')
    model, train_losses, train_accs, test_losses, test_accs = load_model()
    
    print('\nPlotting training curves...')
    plot_training_curves(train_losses, train_accs, test_losses, test_accs)
    
    print('\nCalculating confusion matrix...')
    cm, all_preds, all_targets = calculate_confusion_matrix(model)
    
    print('\nPlotting confusion matrix...')
    plot_confusion_matrix(cm)
    
    print('\nShowing misclassified samples...')
    show_misclassified_samples(model, all_preds, all_targets)
    
    print('\nGenerating classification report...')
    print_classification_report(cm)
    
    print('\nAll visualizations have been saved to ./results/ directory!')

if __name__ == '__main__':
    main()