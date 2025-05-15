<div align='center'>

# Save, share and host AI model checkpoints Lightning fast ⚡

<img alt="Lightning" src="https://pl-public-data.s3.us-east-1.amazonaws.com/assets_lightning/LitModels.png" width="800px" style="max-width: 100%;">

</div>

______________________________________________________________________

Save, load, host, and share models without slowing down training.
**LitModels** minimizes training slowdowns from checkpoint saving. Share public links on Lightning AI or your own cloud with enterprise-grade access controls.

<div align="center">

<pre>
✅ Checkpoint without slowing training.  ✅ Granular access controls.           
✅ Load models anywhere.                 ✅ Host on Lightning or your own cloud.
</pre>

[![Discord](https://img.shields.io/discord/1077906959069626439?label=Get%20help%20on%20Discord)](https://discord.gg/WajDThKAur)
![CI testing](https://github.com/Lightning-AI/LitModels/actions/workflows/ci-testing.yml/badge.svg?event=push)
![Cloud integration](https://github.com/Lightning-AI/LitModels/actions/workflows/ci-cloud.yml/badge.svg?event=push)
[![codecov](https://codecov.io/gh/Lightning-AI/LitModels/graph/badge.svg?token=MQ0PN2cxKo)](https://codecov.io/gh/Lightning-AI/LitModels)
[![license](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/Lightning-AI/LitModels/blob/main/LICENSE)

<div style="text-align: center;">
    <a target="_blank" href="#quick-start" style="margin: 0 10px;">Quick start</a> •
    <a target="_blank" href="#examples" style="margin: 0 10px;">Examples</a> •
    <a target="_blank" href="#features" style="margin: 0 10px;">Features</a> •
    <a target="_blank" href="#performance" style="margin: 0 10px;">Performance</a> •
    <a target="_blank" href="#community" style="margin: 0 10px;">Community</a> •
    <a target="_blank" href="https://lightning.ai/docs/overview/model-registry" style="margin: 0 10px;">Docs</a>
</div>

</div>

# Quick start

Install LitModels via pip:

```bash
pip install litmodels
```

Toy example ([see real examples](#examples)):

```python
import litmodels as lm
import torch

# save a model
model = torch.nn.Module()
lm.save_model(model=model, name="model-name")

# load a model
model = lm.load_model(name="model-name")
```

# Examples

<details>
  <summary>PyTorch</summary>

Save model:

```python
import torch
from litmodels import save_model

model = torch.nn.Module()
save_model(model=model, name="your_org/your_team/torch-model")
```

Load model:

```python
from litmodels import load_model

model_ = load_model(name="your_org/your_team/torch-model")
```

</details>

<details>
  <summary>PyTorch Lightning</summary>

Save model:

```python
from lightning import Trainer
from litmodels import upload_model
from litmodels.demos import BoringModel

# Configure Lightning Trainer
trainer = Trainer(max_epochs=2)
# Define the model and train it
trainer.fit(BoringModel())

# Upload the best model to cloud storage
checkpoint_path = getattr(trainer.checkpoint_callback, "best_model_path")
# Define the model name - this should be unique to your model
upload_model(model=checkpoint_path, name="<organization>/<teamspace>/<model-name>")
```

Load model:

```python
from lightning import Trainer
from litmodels import download_model
from litmodels.demos import BoringModel

# Load the model from cloud storage
checkpoint_path = download_model(
    # Define the model name and version - this needs to be unique to your model
    name="<organization>/<teamspace>/<model-name>:<model-version>",
    download_dir="my_models",
)
print(f"model: {checkpoint_path}")

# Train the model with extended training period
trainer = Trainer(max_epochs=4)
trainer.fit(BoringModel(), ckpt_path=checkpoint_path)
```

</details>

<details>
  <summary>TensorFlow / Keras</summary>

Save model:

```python
from tensorflow import keras

from litmodels import save_model

# Define the model
model = keras.Sequential(
    [
        keras.layers.Dense(10, input_shape=(784,), name="dense_1"),
        keras.layers.Dense(10, name="dense_2"),
    ]
)

# Compile the model
model.compile(optimizer="adam", loss="categorical_crossentropy")

# Save the model
save_model("lightning-ai/jirka/sample-tf-keras-model", model=model)
```

Load model:

```python
from litmodels import load_model

model_ = load_model(
    "lightning-ai/jirka/sample-tf-keras-model", download_dir="./my-model"
)
```

</details>

<details>
  <summary>SKLearn</summary>

Save model:

```python
from sklearn import datasets, model_selection, svm
from litmodels import save_model

# Load example dataset
iris = datasets.load_iris()
X, y = iris.data, iris.target

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = model_selection.train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a simple SVC model
model = svm.SVC()
model.fit(X_train, y_train)

# Upload the saved model using litmodels
save_model(model=model, name="your_org/your_team/sklearn-svm-model")
```

Use model:

```python
from litmodels import load_model

# Download and load the model file from cloud storage
model = load_model(
    name="your_org/your_team/sklearn-svm-model", download_dir="my_models"
)

# Example: run inference with the loaded model
sample_input = [[5.1, 3.5, 1.4, 0.2]]
prediction = model.predict(sample_input)
print(f"Prediction: {prediction}")
```

</details>

# Features

<details>
    <summary>PyTorch Lightning Callback</summary>

Enhance your training process with an automatic checkpointing callback that uploads the model at the end of each epoch.

```python
import torch.utils.data as data
import torchvision as tv
from lightning import Trainer
from litmodels.integrations import LightningModelCheckpoint
from litmodels.demos import BoringModel

dataset = tv.datasets.MNIST(".", download=True, transform=tv.transforms.ToTensor())
train, val = data.random_split(dataset, [55000, 5000])

trainer = Trainer(
    max_epochs=2,
    callbacks=[
        LightningModelCheckpoint(
            # Define the model name - this should be unique to your model
            model_registry="<organization>/<teamspace>/<model-name>",
        )
    ],
)
trainer.fit(
    BoringModel(),
    data.DataLoader(train, batch_size=256),
    data.DataLoader(val, batch_size=256),
)
```

</details>

<details>
    <summary>Save any Python class as a checkpoint</summary>

Mixin classes streamline model management in Python by modularizing reusable functionalities like saving/loading, enabling consistent, conflict-free, and maintainable code across multiple models.

**Save model:**

```python
from litmodels.integrations.mixins import PickleRegistryMixin


class MyModel(PickleRegistryMixin):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
        # Your model initialization code
        ...


# Create and push a model instance
model = MyModel(param1=42, param2="hello")
model.upload_model(name="my-org/my-team/my-model")
```

Load model:

```python
loaded_model = MyModel.download_model(name="my-org/my-team/my-model")
```

</details>

<details>
    <summary>Save custom PyTorch models</summary>

Mixin classes centralize serialization logic, eliminating redundant code and ensuring consistent, error-free model persistence across projects.
The `download_model` method bypasses constructor arguments entirely, reconstructing the model directly from the registry with pre-configured architecture and weights, eliminating initialization mismatches.

Save model:

```python
import torch
from litmodels.integrations.mixins import PyTorchRegistryMixin


# Important: PyTorchRegistryMixin must be first in the inheritance order
class MyTorchModel(PyTorchRegistryMixin, torch.nn.Module):
    def __init__(self, input_size, hidden_size=128):
        super().__init__()
        self.linear = torch.nn.Linear(input_size, hidden_size)
        self.activation = torch.nn.ReLU()

    def forward(self, x):
        return self.activation(self.linear(x))


# Create and push the model
model = MyTorchModel(input_size=784)
model.upload_model(name="my-org/my-team/torch-model")
```

Use the model:

```python
# Pull the model with the same architecture
loaded_model = MyTorchModel.download_model(name="my-org/my-team/torch-model")
```

</details>

# Performance

<!--
TODO: show the chart between not using this vs using this and the impact on training (the GPU utilization side-by-side)... also, what are tangible speed ups in training and inference.
-->

# Community

💬 [Get help on Discord](https://discord.com/invite/XncpTy7DSt)\
📋 [License: Apache 2.0](https://github.com/Lightning-AI/litModels/blob/main/LICENSE)
