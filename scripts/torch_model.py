import torch 
from torch import nn 

class model(nn.Module) : 
    def __init__(self) : 
        super().__init__()
        self.S = nn.Sequential(
            nn.Conv2d(1, 16 , (3,3)) , 
            nn.ReLU() , 
            nn.MaxPool2d((2,2)) , 
            nn.Conv2d(16 , 16 , (3,3)) , 
            nn.ReLU() , 
            nn.Flatten() , 
            nn.Linear(181104 , 128 ), 
            nn.Dropout(.2),
            nn.Linear(128 ,1) , 
            nn.Sigmoid()
            
        )
    def forward(self , inputs ) : 
        return self.S(inputs ) 