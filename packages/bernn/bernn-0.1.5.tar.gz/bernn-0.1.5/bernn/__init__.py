"""BERNN: Batch Effect Removal Neural Networks for Tandem Mass Spectrometry.

This package provides tools for removing batch effects from mass spectrometry data
using deep learning approaches.
"""

import os

# Read version from VERSION file
with open(os.path.join(os.path.dirname(__file__), '..', 'VERSION'), 'r') as f:
    __version__ = f.read().strip()

__author__ = "Simon Pelletier"
__license__ = "MIT"

# Core training modules
from .dl.train import (
    TrainAE,
    TrainAEClassifierHoldout,
    TrainAEThenClassifierHoldout,
)

# Model definitions
from .dl.models.pytorch import (
    AutoEncoder2,
    SHAPAutoEncoder2,
    KANAutoencoder2,
    SHAPKANAutoencoder2,
)

# KAN modules
from .dl.train.pytorch.ekan import KANLinear, KAN

__all__ = [
    # Training
    "TrainAE",
    "TrainAEClassifierHoldout",
    "TrainAEThenClassifierHoldout",
    
    # Models
    "AutoEncoder2",
    "SHAPAutoEncoder2",
    "KANAutoencoder2",
    "SHAPKANAutoencoder2",
    
    # KAN
    "KANLinear",
    "KAN"
]
