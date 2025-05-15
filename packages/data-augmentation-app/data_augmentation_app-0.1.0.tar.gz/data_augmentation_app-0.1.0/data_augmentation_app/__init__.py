from importlib.metadata import version

__version__ = version("data-augmentation-app")   # ← lo leerá setuptools

from .augmentation_core import augment
from .layers_personalizadas import (
    RandomFlip, RandomRotation, RandomZoom,
    RandomChannelShift, RandomColorDistorsion,
    GaussianNoise, SaltPepperNoise,
)

__all__ = [
    "augment",
    "RandomFlip", "RandomRotation", "RandomZoom",
    "RandomChannelShift", "RandomColorDistorsion",
    "GaussianNoise", "SaltPepperNoise",
]
