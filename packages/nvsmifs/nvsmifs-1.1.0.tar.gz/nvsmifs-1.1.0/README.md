---

# nvsmifs

A user-friendly wrapper for `nvidia-smi`, forked from [pmav99's repository](https://github.com/pmav99), with added support for fan speed and power draw monitoring. This tool is particularly useful in multi-GPU systems, allowing you to filter GPUs based on resource usage (e.g., selecting the least utilized GPU).

---

## Features

- **Enhanced GPU Monitoring**: Includes fan speed and power draw metrics.
- **Resource-Based Filtering**: Easily identify the least utilized GPU in your system.
- **Flexible Usage**: Use as a CLI tool or integrate it as a Python library.

---

## Table of Contents

1. [Usage](#usage)
   - [CLI](#cli)
   - [Library](#library)
2. [Quick Example: GPU Info](#quick-example-gpu-info)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
   - [Using pipx (Recommended)](#using-pipx-recommended)
   - [Using pip](#using-pip)
5. [Contributing](#contributing)
6. [License](#license)

---

## Usage

### CLI

Run the following commands to explore available options:

```shell
nvsmifs --help
nvsmifs ls --help
nvsmifs ps --help
```

### Library

You can also use `nvsmifs` as a Python library for more advanced workflows:

```python
import nvsmifs

gpus = nvsmifs.get_gpus()
available_gpus = nvsmifs.get_available_gpus()
gpu_processes = nvsmifs.get_gpu_processes()
```

---

## Quick Example: GPU Info

Here's a simple Python function to display detailed GPU information:

```python
import nvsmifs

def gpu_info():
    for gpu in nvsmifs.get_gpus():
        if gpu.display_active == 'Enabled':
            gpu_details = (
                f"ID: {gpu.id}, Power: {gpu.power_draw}W, "
                f"Name: {gpu.name}, Temp: {gpu.temperature}°C, "
                f"Fan Speed: {gpu.fan_speed}%, Utilization: {gpu.gpu_util}%"
            )
            print(gpu_details)

gpu_info()
```

Output example:

```
ID: 0, Power: 50W, Name: NVIDIA GTX 1080, Temp: 65°C, Fan Speed: 30%, Utilization: 20%
```

---

## Prerequisites

Ensure the following requirements are met before using `nvsmifs`:

- An NVIDIA GPU
- `nvidia-smi` installed and accessible
- Python 2.7 or 3.6+

---

## Installation

### Using pipx (Recommended)

The recommended installation method is via [pipx](https://github.com/pipxproject/pipx). Install `nvsmifs` with:

```shell
pipx install nvsmifs
```

This creates a virtual environment in `~/.local/pipx/venvs/nvsmifs` and adds the `nvsmifs` executable to `~/.local/bin`.

### Using pip

Alternatively, install directly with pip:

```shell
pip install --user nvsmifs
```

---

## Contributing

Contributions are welcome! If you'd like to improve this project, please:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with a clear description of your changes.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
