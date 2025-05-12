from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import zipfile
import os

# ==========================
#      FASTAPI SETUP
# ==========================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/train")
async def train_endpoint(file: UploadFile = File(...)):
    print("Received zip file for split learning simulation.")
    # Extract zip to 'recieved_data' folder
    extract_dir = os.path.abspath("recieved_data")
    os.makedirs(extract_dir, exist_ok=True)
    zip_path = os.path.join(extract_dir, "upload.zip")
    with open(zip_path, "wb") as f:
        f.write(await file.read())
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Extracted zip to {extract_dir}. Ignoring contents, running FMNIST simulation.")
    comm_overhead = run_split_learning_simulation()
    return {"comm_overhead_mb": comm_overhead}

# ==========================
#   SPLIT LEARNING SIM
# ==========================
def run_split_learning_simulation():
    batch_size = 64
    epochs = 1  # Keep short for demo
    learning_rate = 0.01
    random_seed = 0
    torch.manual_seed(random_seed)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')
    # Data loading (FMNIST)
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    train_set = torchvision.datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
    total_train = len(train_set)
    client1_len = total_train // 2
    client2_len = total_train - client1_len
    client1_set, client2_set = torch.utils.data.random_split(train_set, [client1_len, client2_len], generator=torch.Generator().manual_seed(random_seed))
    client1_loader = torch.utils.data.DataLoader(client1_set, batch_size=batch_size, shuffle=True)
    client2_loader = torch.utils.data.DataLoader(client2_set, batch_size=batch_size, shuffle=True)
    # Model split (first split only)
    class Client1(nn.Module):
        def __init__(self):
            super().__init__()
            self.block1 = nn.Sequential(
                nn.Conv2d(1, 6, 5), nn.ReLU(), nn.MaxPool2d(2, 2)
            )
        def forward(self, x):
            return self.block1(x)
    class Server1(nn.Module):
        def __init__(self):
            super().__init__()
            self.block2 = nn.Sequential(
                nn.Conv2d(6, 16, 5), nn.ReLU(), nn.MaxPool2d(2, 2)
            )
            self.block3 = nn.Sequential(
                nn.Linear(256, 120), nn.ReLU(),
                nn.Linear(120, 84), nn.ReLU(),
                nn.Linear(84, 10)
            )
        def forward(self, x):
            x = self.block2(x)
            x = x.view(x.size(0), -1)
            x = self.block3(x)
            return x
    client1_model = Client1().to(device)
    client2_model = Client1().to(device)
    server_model = Server1().to(device)
    client1_optimizer = optim.SGD(client1_model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=5e-4)
    client2_optimizer = optim.SGD(client2_model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=5e-4)
    server_optimizer = optim.SGD(server_model.parameters(), lr=learning_rate, momentum=0.9, weight_decay=5e-4)
    loss_criterion = nn.CrossEntropyLoss()
    total_activations_sent = 0
    total_gradients_sent = 0
    for epoch in range(1, epochs + 1):
        client1_model.train()
        client2_model.train()
        server_model.train()
        for (batch1, batch2) in zip(client1_loader, client2_loader):
            for client_model, client_optimizer, (inputs, labels) in [
                (client1_model, client1_optimizer, batch1),
                (client2_model, client2_optimizer, batch2)
            ]:
                inputs, labels = inputs.to(device), labels.to(device)
                client_optimizer.zero_grad()
                server_optimizer.zero_grad()
                split_activations = client_model(inputs)
                split_activations = split_activations.detach().requires_grad_()
                total_activations_sent += split_activations.numel()
                outputs = server_model(split_activations)
                loss = loss_criterion(outputs, labels)
                loss.backward()
                split_grads = split_activations.grad
                total_gradients_sent += split_grads.numel()
                split_activations.backward(split_grads)
                client_optimizer.step()
                server_optimizer.step()
    elements_sent = total_activations_sent + total_gradients_sent
    bytes_sent = elements_sent * 4  # float32 = 4 bytes
    mb_sent = bytes_sent / (1024**2)
    print(f"Total communication overhead: {mb_sent:.2f} MB")
    return round(mb_sent, 2) 