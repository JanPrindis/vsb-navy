import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim

# Generování logistické mapy
def generate_values(start: float, num: int):
    a_values = np.linspace(start, 4.0, num)
    values = []

    for a in a_values:
        x = 0.5

        # Iterace pro stabilizaci
        for _ in range(1000):
            x = a * x * (1 - x)

        # Hlavní iterace pro generování hodnot
        for _ in range(1000):
            x = a * x * (1 - x)
            values.append((a, x))

    return values


def generate_dataset(n_samples=10000):
    a_vals = np.random.uniform(2.5, 4.0, n_samples)
    x_vals = np.random.uniform(0, 1, n_samples)
    y_vals = a_vals * x_vals * (1 - x_vals)  # x_{n+1}
    X = np.stack([a_vals, x_vals], axis=1).astype(np.float32)
    y = y_vals.astype(np.float32)
    return torch.tensor(X), torch.tensor(y)


# Model pro predikci
class LogisticMapModel(nn.Module):
    def __init__(self):
        super(LogisticMapModel, self).__init__()
        self.layer1 = nn.Linear(2, 32)
        self.layer2 = nn.Linear(32, 32)
        self.output = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = torch.relu(self.layer2(x))
        return self.output(x)


def train_model(X, y, epochs=20):
    model = LogisticMapModel()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        output = model(X)
        loss = criterion(output.flatten(), y)
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 5 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

    return model


# První okno: Vykreslení trénovacích dat a predikcí
def plot_training_and_predictions(model, start=2.5, num=1000, N=1000):
    # Generování skutečného bifurkačního diagramu
    values = generate_values(start, num)
    a_values, x_values = zip(*values)
    a_values = np.array(a_values)
    x_values = np.array(x_values)

    # Náhodně vybrat N bodů pro predikci
    indices = np.random.choice(len(a_values), size=N, replace=False)
    a_values_sampled = a_values[indices]
    x_values_sampled = x_values[indices]

    # Predikce modelu
    X = torch.tensor(np.stack([a_values_sampled, x_values_sampled], axis=1), dtype=torch.float32)
    y_pred = model(X).detach().numpy().flatten()

    # Vykreslení: první okno (trénovací dataset a predikce)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Trénovací dataset (levý graf)
    axes[0].scatter(a_values, x_values, c='black', s=1, alpha=0.25, label="Trénovací data")
    axes[0].set_title("Trénovací dataset")
    axes[0].set_xlabel("a")
    axes[0].set_ylabel("x")

    # Predikce modelu (pravý graf)
    axes[1].scatter(a_values_sampled, y_pred, c='blue', s=1, label="Predikce modelu")
    axes[1].set_title("Predikce modelu")
    axes[1].set_xlabel("a")
    axes[1].set_ylabel("Predikce")

    plt.tight_layout()
    plt.show()


# Druhé okno: Vykreslení predikcí na novém bifurkačním diagramu
def plot_bifurcation_with_predictions(model, start=2.5, num=1000, N=1000):
    # Generování nového bifurkačního diagramu
    values = generate_values(start, num)
    a_values, x_values = zip(*values)
    a_values = np.array(a_values)
    x_values = np.array(x_values)

    # Náhodně vybrat N bodů pro predikci
    indices = np.random.choice(len(a_values), size=N, replace=False)
    a_values_sampled = a_values[indices]
    x_values_sampled = x_values[indices]

    # Predikce modelu
    X = torch.tensor(np.stack([a_values_sampled, x_values_sampled], axis=1), dtype=torch.float32)
    y_pred = model(X).detach().numpy().flatten()

    # Určení správných predikcí (rozdíl mezi skutečnými a predikovanými hodnotami je menší než tolerance)
    tolerance = 0.01
    correct_predictions = np.abs(a_values_sampled * x_values_sampled * (1 - x_values_sampled) - y_pred) < tolerance

    # Výpočet úspěšnosti
    correct_count = np.sum(correct_predictions)
    accuracy = (correct_count / N) * 100

    # Vykreslení nového bifurkačního diagramu s predikcemi
    plt.figure(figsize=(10, 6))

    # Skutečný bifurkační diagram
    plt.scatter(a_values, x_values, c='black', s=1, alpha=0.25, label="Skutečná data")

    # Korektní predikce (zelená)
    plt.scatter(a_values_sampled[correct_predictions], x_values_sampled[correct_predictions], c='green', s=5,
                label="Správně predikováno", alpha=0.75)

    # Nesprávně predikované body (červená)
    plt.scatter(a_values_sampled[~correct_predictions], x_values_sampled[~correct_predictions], c='red', s=5,
                label="Chybně predikováno", alpha=0.75)

    # Titulek s úspěšností
    plt.title(f"Bifurkační diagram s predikcemi\nPredikční úspěšnost: {accuracy:.2f}%", fontsize=14)
    plt.xlabel("a")
    plt.ylabel("x")
    plt.legend()

    plt.show()


# Generování datasetu a trénování modelu
X, y = generate_dataset()
model = train_model(X, y, epochs=10000)

# První okno: Trénovací data a predikce
plot_training_and_predictions(model, N=1000)

# Druhé okno: Nový bifurkační diagram s predikcemi
plot_bifurcation_with_predictions(model, N=1000)
