import torch
from torch.utils.data import DataLoader, TensorDataset
from tqdm import tqdm
import time
import pandas as pd

def fit(model, train_dl, train_ds, model_children, regular_param, optimizer, RHO, l1):
    print('Training')
    model.train()
    running_loss = 0.0
    counter = 0
    for i, data in tqdm(enumerate(train_dl), total=int(len(train_ds) / train_dl.batch_size)):
        counter += 1
        x, _ = data
        optimizer.zero_grad()
        reconstructions = model(x)
        loss = model.loss(model_children=model_children, true_data=x, reconstructed_data=reconstructions,reg_param=regular_param)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

def validate(model, test_dl, test_ds, model_children,reg_param):
    print('Validating')
    model.eval()
    running_loss = 0.0
    counter = 0
    with torch.no_grad():
        for i, data in tqdm(enumerate(test_dl), total=int(len(test_ds) / test_dl.batch_size)):
            counter += 1
            x, _ = data
            reconstructions = model(x)
            loss = model.loss(model_children=model_children, true_data=x, reconstructed_data=reconstructions, reg_param=reg_param)
            running_loss += loss.item()

    epoch_loss = running_loss / counter
    print(f" Val Loss: {loss:.6f}")
    # save the reconstructed images every 5 epochs
    return epoch_loss

def train(model,variables, train_data, test_data, parent_path, config):
    learning_rate = config["lr"]
    reg_param = config["reg_param"]
    RHO = config["RHO"]
    l1 = config["l1"]
    epochs = config["epochs"]
    latent_space_size = config["latent_space_size"]
    
    model_children = list(model.children())

    # Constructs a tensor object of the data and wraps them in a TensorDataset object.
    train_ds = TensorDataset(torch.tensor(train_data.values, dtype=torch.float),
                             torch.tensor(train_data.values, dtype=torch.float))
    valid_ds = TensorDataset(torch.tensor(test_data.values, dtype=torch.float),
                             torch.tensor(test_data.values, dtype=torch.float))

    bs = 512

    # Converts the TensorDataset into a DataLoader object and combines into one DataLoaders object (a basic wrapper
    # around several DataLoader objects).
    train_dl = DataLoader(train_ds, batch_size=bs, shuffle=True)
    valid_dl = DataLoader(valid_ds, batch_size=bs * 2)

    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # train and validate the autoencoder neural network
    train_loss = []
    val_loss = []
    start = time.time()
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1} of {epochs}")
        train_epoch_loss = fit(model=model, train_dl=train_dl, train_ds=train_ds, model_children=model_children,
                               optimizer=optimizer, RHO=RHO, regular_param=reg_param, l1=l1)
        val_epoch_loss = validate(model=model, test_dl=valid_dl, test_ds=valid_ds, model_children=model_children,reg_param=reg_param)
        train_loss.append(train_epoch_loss)
        val_loss.append(val_epoch_loss)
    end = time.time()

    print(f"{(end - start) / 60:.3} minutes")
    pd.DataFrame(train_loss).to_csv(parent_path+"loss_train_data.csv")
    pd.DataFrame(val_loss).to_csv(parent_path+"loss_val_data.csv")

    data = torch.tensor(test_data.values, dtype=torch.float)

    pred = model(data)
    pred = pred.detach().numpy()
    data = data.detach().numpy()

    return data, pred