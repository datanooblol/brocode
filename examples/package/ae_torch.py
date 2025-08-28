#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple AutoEncoder implementation using PyTorch.

The module defines three classes:

* :class:`Encoder` – maps the input to a latent representation.
* :class:`Decoder` – reconstructs the input from the latent vector.
* :class:`AutoEncoder` – combines the encoder and decoder into a single
  :class:`torch.nn.Module`.

The network is intentionally lightweight and suitable for educational
purposes or quick prototyping.  It can be extended by inheriting from the
base classes or by replacing the internal layers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


class Encoder(nn.Module):
    """
    Encoder network that compresses the input into a latent vector.

    The architecture consists of a single linear layer followed by a
    ReLU activation.  The dimensionality of the latent space is
    configurable via the ``latent_dim`` argument.

    Args:
        input_dim: Dimensionality of the input features.
        latent_dim: Dimensionality of the latent representation.
    """

    def __init__(self, input_dim: int, latent_dim: int) -> None:
        super().__init__()
        if input_dim <= 0:
            raise ValueError("input_dim must be a positive integer")
        if latent_dim <= 0:
            raise ValueError("latent_dim must be a positive integer")

        self.linear = nn.Linear(input_dim, latent_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the encoder.

        Args:
            x: Input tensor of shape ``(batch_size, input_dim)``.

        Returns:
            Latent representation tensor of shape
            ``(batch_size, latent_dim)``.
        """
        if x.ndim != 2 or x.size(1) != self.linear.in_features:
            raise ValueError(
                f"Expected input of shape (batch_size, {self.linear.in_features}), "
                f"got {x.shape}"
            )
        return F.relu(self.linear(x))


class Decoder(nn.Module):
    """
    Decoder network that reconstructs the input from a latent vector.

    The architecture mirrors the encoder: a single linear layer followed
    by a Sigmoid activation to keep the output in the range [0, 1].

    Args:
        latent_dim: Dimensionality of the latent representation.
        output_dim: Dimensionality of the reconstructed output.
    """

    def __init__(self, latent_dim: int, output_dim: int) -> None:
        super().__init__()
        if latent_dim <= 0:
            raise ValueError("latent_dim must be a positive integer")
        if output_dim <= 0:
            raise ValueError("output_dim must be a positive integer")

        self.linear = nn.Linear(latent_dim, output_dim)

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the decoder.

        Args:
            z: Latent tensor of shape ``(batch_size, latent_dim)``.

        Returns:
            Reconstructed tensor of shape ``(batch_size, output_dim)``.
        """
        if z.ndim != 2 or z.size(1) != self.linear.in_features:
            raise ValueError(
                f"Expected latent input of shape (batch_size, {self.linear.in_features}), "
                f"got {z.shape}"
            )
        return torch.sigmoid(self.linear(z))


class AutoEncoder(nn.Module):
    """
    AutoEncoder that combines an :class:`Encoder` and a :class:`Decoder`.

    The network can be used for dimensionality reduction, denoising,
    or as a pre‑training step for other models.

    Args:
        input_dim: Dimensionality of the input features.
        latent_dim: Dimensionality of the latent representation.
    """

    def __init__(self, input_dim: int, latent_dim: int) -> None:
        super().__init__()
        self.encoder = Encoder(input_dim, latent_dim)
        self.decoder = Decoder(latent_dim, input_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass of the autoencoder.

        Args:
            x: Input tensor of shape ``(batch_size, input_dim)``.

        Returns:
            Reconstructed tensor of shape ``(batch_size, input_dim)``.
        """
        z = self.encoder(x)
        return self.decoder(z)

    def encode(self, x: torch.Tensor) -> torch.Tensor:
        """
        Encode the input into the latent space.

        Args:
            x: Input tensor of shape ``(batch_size, input_dim)``.

        Returns:
            Latent representation tensor of shape
            ``(batch_size, latent_dim)``.
        """
        return self.encoder(x)

    def decode(self, z: torch.Tensor) -> torch.Tensor:
        """
        Decode a latent vector back into the input space.

        Args:
            z: Latent tensor of shape ``(batch_size, latent_dim)``.

        Returns:
            Reconstructed tensor of shape ``(batch_size, input_dim)``.
        """
        return self.decoder(z)


# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #
def _example() -> None:
    """
    Demonstrates how to instantiate and train the AutoEncoder on dummy data.
    """
    # Hyper‑parameters
    input_dim = 784  # e.g., flattened 28x28 images
    latent_dim = 32
    batch_size = 64
    epochs = 5
    learning_rate = 1e-3

    # Dummy dataset: random noise
    data = torch.randn(1000, input_dim)

    # DataLoader
    dataset = torch.utils.data.TensorDataset(data)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Model, loss, optimizer
    model = AutoEncoder(input_dim, latent_dim)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # Training loop
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for batch, in loader:
            optimizer.zero_grad()
            recon = model(batch)
            loss = criterion(recon, batch)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * batch.size(0)

        epoch_loss /= len(loader.dataset)
        print(f"Epoch {epoch + 1}/{epochs} – Loss: {epoch_loss:.4f}")

    # Inference example
    model.eval()
    with torch.no_grad():
        sample = data[:5]
        latent = model.encode(sample)
        recon = model.decode(latent)
        print("Original shape:", sample.shape)
        print("Latent shape:", latent.shape)
        print("Reconstructed shape:", recon.shape)


if __name__ == "__main__":
    _example()