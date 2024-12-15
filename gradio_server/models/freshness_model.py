import torch
import torch.nn as nn
import torchvision.models as models

class MultiOutputModel(nn.Module):
    def __init__(self, num_classes_type):
        super(MultiOutputModel, self).__init__()
        
        # Load a pretrained MobileNetV2 model
        self.mobilenet = models.mobilenet_v2(pretrained=True)
        
        # Freeze MobileNetV2 layers if needed
        for param in self.mobilenet.features.parameters():
            param.requires_grad = False

        # Get the in_features from the classifier layer of MobileNetV2
        in_features = self.mobilenet.last_channel
        
        # Replace the classifier to produce a shared feature space
        self.mobilenet.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3)  # Optional regularization
        )
        
        # Head for type classification
        self.type_head = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes_type)
        )

        # Head for freshness classification
        self.freshness_head = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        # Extract features using MobileNetV2
        x = self.mobilenet(x)
        
        # Type classification
        type_output = self.type_head(x)
        # Freshness classification
        freshness_output = self.freshness_head(x)
        
        return type_output, freshness_output
