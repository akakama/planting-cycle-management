"""
MobileNetV3 病虫害识别模型微调训练脚本
使用真实病虫害数据集对模型进行微调训练
"""
import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from torchvision.models import mobilenet_v3_small
from PIL import Image
from pathlib import Path
import time
from tqdm import tqdm
import json

class PlantDiseaseDataset(Dataset):
    """病虫害数据集"""

    def __init__(self, data_dir, transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform
        self.images = []
        self.labels = []

        # 类别映射
        self.class_names = [
            "小麦白粉病",
            "稻瘟病",
            "玉米大斑病",
            "蚜虫",
            "红蜘蛛",
            "白粉虱"
        ]

        # 加载所有图像
        for class_id, class_name in enumerate(self.class_names):
            class_dir = self.data_dir / class_name
            if class_dir.exists():
                for img_path in class_dir.glob("*.*"):
                    if img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                        self.images.append(str(img_path))
                        self.labels.append(class_id)

        print(f"加载数据: {len(self.images)} 张图像")

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image_path = self.images[idx]
        label = self.labels[idx]

        # 加载图像
        image = Image.open(image_path).convert('RGB')

        # 应用变换
        if self.transform:
            image = self.transform(image)

        return image, label


class ModelTrainer:
    """模型训练器"""

    def __init__(self, data_dir="data", model_path="models/mobilenetv3.pth",
                 output_path="models/mobilenetv3_finetuned.pth"):
        self.data_dir = Path(data_dir)
        self.model_path = model_path
        self.output_path = output_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        print(f"使用设备: {self.device}")

        # 类别名称
        self.class_names = [
            "小麦白粉病",
            "稻瘟病",
            "玉米大斑病",
            "蚜虫",
            "红蜘蛛",
            "白粉虱"
        ]

        # 训练历史
        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": []
        }

    def create_data_loaders(self, batch_size=32):
        """创建数据加载器"""
        # 数据增强和预处理
        train_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        val_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        # 创建数据集
        train_dataset = PlantDiseaseDataset(
            self.data_dir / "train",
            transform=train_transform
        )

        val_dataset = PlantDiseaseDataset(
            self.data_dir / "val",
            transform=val_transform
        )

        # 创建数据加载器
        train_loader = DataLoader(
            train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=4,
            pin_memory=True
        )

        val_loader = DataLoader(
            val_dataset,
            batch_size=batch_size,
            shuffle=False,
            num_workers=4,
            pin_memory=True
        )

        return train_loader, val_loader

    def load_model(self):
        """加载预训练模型"""
        print("\n加载预训练模型...")

        # 尝试加载已有模型
        if os.path.exists(self.model_path):
            model = torch.load(self.model_path, map_location=self.device)
            print(f"✓ 从 {self.model_path} 加载模型")
        else:
            # 创建新模型
            model = mobilenet_v3_small(pretrained=False)

            # 修改分类器
            in_features = model.classifier[0].in_features
            model.classifier = nn.Sequential(
                nn.Linear(in_features, 1024),
                nn.Hardswish(),
                nn.Dropout(0.2),
                nn.Linear(1024, 6)
            )
            print("✓ 创建新模型")

        model = model.to(self.device)
        return model

    def train_epoch(self, model, train_loader, criterion, optimizer):
        """训练一个epoch"""
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        pbar = tqdm(train_loader, desc="训练中")
        for images, labels in pbar:
            images = images.to(self.device)
            labels = labels.to(self.device)

            # 前向传播
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)

            # 反向传播
            loss.backward()
            optimizer.step()

            # 统计
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            # 更新进度条
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })

        epoch_loss = running_loss / len(train_loader)
        epoch_acc = 100. * correct / total

        return epoch_loss, epoch_acc

    def validate(self, model, val_loader, criterion):
        """验证模型"""
        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():
            pbar = tqdm(val_loader, desc="验证中")
            for images, labels in pbar:
                images = images.to(self.device)
                labels = labels.to(self.device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                running_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        epoch_loss = running_loss / len(val_loader)
        epoch_acc = 100. * correct / total

        return epoch_loss, epoch_acc

    def train(self, epochs=50, batch_size=32, learning_rate=0.001, freeze_backbone=True):
        """训练模型"""
        print("="*60)
        print("开始模型训练")
        print("="*60)

        # 创建数据加载器
        train_loader, val_loader = self.create_data_loaders(batch_size)

        # 加载模型
        model = self.load_model()

        # 冻结骨干网络（可选）
        if freeze_backbone:
            print("\n冻结骨干网络参数...")
            for param in model.features.parameters():
                param.requires_grad = False
            print("✓ 骨干网络已冻结，只训练分类器")

        # 定义损失函数和优化器
        criterion = nn.CrossEntropyLoss()

        # 使用不同的学习率
        if freeze_backbone:
            optimizer = optim.Adam(
                filter(lambda p: p.requires_grad, model.parameters()),
                lr=learning_rate
            )
        else:
            optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        # 学习率调度器
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

        # 训练循环
        best_val_acc = 0.0

        print(f"\n训练参数:")
        print(f"  Epochs: {epochs}")
        print(f"  Batch Size: {batch_size}")
        print(f"  Learning Rate: {learning_rate}")
        print(f"  Freeze Backbone: {freeze_backbone}")
        print(f"  Train Samples: {len(train_loader.dataset)}")
        print(f"  Val Samples: {len(val_loader.dataset)}")

        for epoch in range(epochs):
            print(f"\nEpoch {epoch+1}/{epochs}")
            print("-"*60)

            # 训练
            train_loss, train_acc = self.train_epoch(
                model, train_loader, criterion, optimizer
            )

            # 验证
            val_loss, val_acc = self.validate(model, val_loader, criterion)

            # 更新学习率
            scheduler.step()

            # 记录历史
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)

            # 打印结果
            print(f"训练 - Loss: {train_loss:.4f}, Acc: {train_acc:.2f}%")
            print(f"验证 - Loss: {val_loss:.4f}, Acc: {val_acc:.2f}%")

            # 保存最佳模型
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model, self.output_path)
                print(f"✓ 保存最佳模型 (验证准确率: {val_acc:.2f}%)")

        print("\n" + "="*60)
        print("训练完成")
        print("="*60)
        print(f"最佳验证准确率: {best_val_acc:.2f}%")
        print(f"模型已保存到: {self.output_path}")

        # 保存训练历史
        self.save_history()

    def save_history(self):
        """保存训练历史"""
        history_path = Path(self.output_path).parent / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.history, f, indent=2)
        print(f"训练历史已保存到: {history_path}")

    def evaluate_test(self):
        """在测试集上评估模型"""
        print("\n在测试集上评估模型...")

        # 加载最佳模型
        model = torch.load(self.output_path, map_location=self.device)
        model.eval()

        # 创建测试数据加载器
        test_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        test_dataset = PlantDiseaseDataset(
            self.data_dir / "test",
            transform=test_transform
        )

        test_loader = DataLoader(
            test_dataset,
            batch_size=32,
            shuffle=False
        )

        # 评估
        correct = 0
        total = 0
        class_correct = [0] * 6
        class_total = [0] * 6

        with torch.no_grad():
            for images, labels in test_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)

                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

                # 每个类别的准确率
                for i in range(len(labels)):
                    label = labels[i]
                    class_total[label] += 1
                    if predicted[i] == label:
                        class_correct[label] += 1

        # 打印结果
        print("\n测试集评估结果:")
        print("="*60)
        print(f"总体准确率: {100.*correct/total:.2f}%")
        print("\n各类别准确率:")
        for i, class_name in enumerate(self.class_names):
            if class_total[i] > 0:
                acc = 100. * class_correct[i] / class_total[i]
                print(f"  {class_name}: {acc:.2f}% ({class_correct[i]}/{class_total[i]})")


def main():
    """主函数"""
    print("="*60)
    print("MobileNetV3 病虫害识别模型微调训练")
    print("="*60)

    # 创建训练器
    trainer = ModelTrainer(
        data_dir="data",
        model_path="models/mobilenetv3.pth",
        output_path="models/mobilenetv3_finetuned.pth"
    )

    # 训练模型
    trainer.train(
        epochs=50,
        batch_size=32,
        learning_rate=0.001,
        freeze_backbone=True  # 先冻结骨干网络训练
    )

    # 评估测试集
    trainer.evaluate_test()


if __name__ == "__main__":
    main()
