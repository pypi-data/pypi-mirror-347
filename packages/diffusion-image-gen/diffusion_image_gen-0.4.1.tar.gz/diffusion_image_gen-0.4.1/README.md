# Diffusion-Based Image Generation

## Overview

This project implements diffusion-based generative models for image synthesis. It provides a comprehensive framework for training and using diffusion models, with support for various diffusion processes, noise schedules, and sampling methods.

## Features

- **Multiple Diffusion Processes**: Support for Variance Exploding (VE), Variance Preserving (VP), and other diffusion types
- **Customizable Noise Schedules**: Linear, Cosine, and custom noise schedules
- **Various Samplers**: Euler-Maruyama, Exponential Integrator, ODE Probability Flow, and Predictor-Corrector samplers
- **Advanced Generation Capabilities**:
  - Unconditional image generation
  - Class-conditional image generation
  - Image colorization
  - Image inpainting/imputation
- **Interactive Dashboard**: Built with Streamlit for easy model interaction, accessible via a simple CLI command.

## Installation

### Using pip (Recommended)

You can install the package directly from PyPI:

```bash
pip install diffusion-image-gen
```

### From Source (for development)

Clone the repository:

```bash
git clone https://github.com/HectorTablero/image-gen.git
cd image-gen
pip install -e .
```

## Usage

### Basic Generation

```python
from diffusion_image_gen import GenerativeModel

# Load a pre-trained model
# Note: You will need to have a model file (.pt or .pth) available.
# model = GenerativeModel.load("path/to/your/model.pth")

# Generate images
# images = model.generate(num_images=4, n_steps=500, seed=42)
```

### Colorization

```python
# Colorize a grayscale image
# colorized = model.colorize(grayscale_image, n_steps=500)
```

### Image Inpainting

```python
# Perform inpainting with a mask
# inpainted = model.imputation(image, mask, n_steps=500)
```
**Note**: The usage examples above assume you have a trained model file. The package provides the framework, but pre-trained models are not included in the base installation.

## Interactive Dashboard

Run the dashboard to interact with your models using the command line:

```bash
diffusion-image-gen dashboard
```
This will start the Streamlit web application.

## Documentation

A comprehensive version of the documentation is available at [https://deepwiki.com/HectorTablero/image-gen](https://deepwiki.com/HectorTablero/image-gen)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Héctor Tablero Díaz - [hector.tablerodiaz@gmail.com](mailto:hector.tablerodiaz@gmail.com)
- Álvaro Martínez Gamo - [alva00003@gmail.com](mailto:alva00003@gmail.com)
