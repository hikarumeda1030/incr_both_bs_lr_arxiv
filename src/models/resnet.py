import torch
import torch.nn as nn
from torchvision.models.resnet import ResNet, BasicBlock, Bottleneck

__all__ = ['ResNet', 'resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']


class ResNet(ResNet):
    def __init__(self, block, layers, num_classes=100):
        super().__init__(block, layers, num_classes=num_classes)

        # Adjust initial convolution and pooling layers
        self.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.maxpool = nn.Identity()  # Remove MaxPooling

    def _forward_impl(self, x):
        # Adjust standard ResNet forward processing
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        # Skip MaxPool
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x


def resnet18(num_classes=100):
    """Build the ResNet-18 model"""
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes=num_classes)


def resnet34(num_classes=100):
    """Build the ResNet-34 model"""
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes)


def resnet50(num_classes=100):
    """Build the ResNet-50 model"""
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes=num_classes)


def resnet101(num_classes=100):
    """Build the ResNet-101 model"""
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes=num_classes)


def resnet152(num_classes=100):
    """Build the ResNet-152 model"""
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes=num_classes)
