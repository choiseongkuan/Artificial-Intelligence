from torch.autograd import Variable
import torch
import torch.nn as nn
import torch.utils.data as Data
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import time

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# device = torch.device('cpu')
print(device)

# 定义超参数
EPOCH = 10
BATCH_SIZE = 10
LR = 0.001

# 加载数据集
transform = transforms.Compose([
    transforms.Resize((128, 128)),  # 把像素重新调整成128*128
    transforms.ToTensor(),  # 把图片转换为张量
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # 对图像进行标准化处理，使得图像数据分布更加平稳，有利于提升模型精度
])

train_dataset = datasets.ImageFolder('./data/train', transform=transform)  # 加载图像文件（训练集）
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)  # 预处理图像，将训练集分成一个个batch

test_dataset = datasets.ImageFolder('./data/test', transform=transform)  # 加载图像文件（测试集）
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)  # 预处理图像，将测试集分成一个个batch


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()  # 构建卷积神经网络
        self.conv1 = nn.Sequential(  # 输入大小(3, 128, 128)
            nn.Conv2d(  # 卷积层
                in_channels=3,  # 输入通道数（彩色图片为3）
                out_channels=16,  # 卷积核的数量即输出的通道数
                kernel_size=5,  # 卷积核的大小
                stride=1,  # 卷积的步长
                padding=2,  # 图像周围填充0的数量(为保持原先的宽和高，可根据(kernel_size-1)/2设定该值)
            ),
            nn.ReLU(),  # 激活函数
            nn.MaxPool2d(kernel_size=2),  # 最大池化
        )  # 输出大小（16，64，64）
        self.conv2 = nn.Sequential(  # 输入大小（16，64，64）
            nn.Conv2d(16, 32, 5, 1, 2),  # 卷积层
            nn.ReLU(),  # 激活函数
            nn.MaxPool2d(2),  # 最大池化
        )  # 输出大小（16，32，32）
        self.out = nn.Linear(32 * 32 * 32, 5)   # 全连接层

    def forward(self, x):  # 前向传播
        x = self.conv1(x)  # 通过第一个卷积层得到特征图
        x = self.conv2(x)  # 通过第二个卷积层得到特征图
        x = x.view(x.size(0), -1)  # 拉平为一维向量
        y = self.out(x)  # 通过全连接层进行线性变化得到最终结果
        return y, x    # 返回输出输入


cnn = CNN().to(device)  # 初始化卷积神经网络

optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)  # 用Adam优化器优化参数
loss_func = nn.CrossEntropyLoss()  # 交叉熵损失函数

t1 = time.time()
loss_ls = []
accuracy_ls = []
for epoch in range(EPOCH):  # 迭代过程
    for step, (b_x, b_y) in enumerate(train_loader):  # 训练
        b_x = b_x.to(device)
        b_y = b_y.to(device)
        output = cnn(b_x)[0]  # 计算cnn输出
        loss = loss_func(output, b_y)  # 计算损失
        optimizer.zero_grad()  # 清空梯度
        loss.backward()   # 反向传播
        optimizer.step()  # 参数更新

        # 记录损失和计算准确率
        correct = 0  # 初始化预测正确的数目
        total = 0  # 初始化样本总数
        for (images, labels) in test_loader:  # 测试
            images = images.to(device)
            labels = labels.to(device)
            outputs = cnn(images)[0]  # 计算cnn输出
            _, predicted = torch.max(outputs.data, 1)  # 获取预测结果
            total += labels.size(0)  # 获取样本总数
            correct += (predicted == labels).sum()  # 计算预测正确的个数
            loss_record = loss.data.cpu().numpy()  # 获取损失
            accuracy_record = 100 * correct / total  # 计算准确率
            print(f"loss: {loss.data.cpu().numpy()} accuracy: {100 * correct / total}%")
            loss_ls.append(float(loss_record))  # 记录损失
            accuracy_ls.append(int(accuracy_record))  # 记录准确率
            # running_loss = 0.0
t2 = time.time()
print(t2-t1)
plt.plot(loss_ls)
plt.show()
plt.plot(accuracy_ls)
plt.show()
