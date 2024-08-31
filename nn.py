import torch
import torchvision



if __name__=='__main__':
    model = torch.hub.load('pytorch/vision', 'mobilenet_v2', pretrained=True)
    print(model.classifier)