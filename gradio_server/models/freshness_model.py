import torch
import torch.nn as nn
import torchvision.models as models

class MultiOutputModel(nn.Module):
    def __init__(self, num_classes_type):
        super(MultiOutputModel, self).__init__()
        
        # Load a pretrained ResNet model
        self.resnet = models.resnet50(pretrained=True)
        
        # Freeze ResNet layers if needed
        for param in self.resnet.parameters():
            param.requires_grad = False
        
        # Get the in_features from the fully connected layer of ResNet
        in_features = self.resnet.fc.in_features
        
        # Modify the fully connected layer for type classification
        self.resnet.fc = nn.Linear(in_features, 512)

        self.type_head = nn.Sequential(
            nn.Linear(512, 512),  # Adding another fully connected layer
            nn.ReLU(),            # Activation function for the new layer
            nn.Dropout(0.3),       # Optional dropout for regularization
            nn.Linear(512, num_classes_type)  # Output layer
        )

        self.freshness_head = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(256, 128),    # Adding a new layer for more complexity
            nn.ReLU(),              # Activation for the new layer
            nn.Linear(128, 1)       # Final output layer
        )

    def forward(self, x):
        x = self.resnet(x)
        # Type classification
        type_output = self.type_head(x)
        # Freshness classification
        freshness_output = self.freshness_head(x)
        
        return type_output, freshness_output