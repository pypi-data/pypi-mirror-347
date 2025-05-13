<div align="center">
  
# ~ _tinyllama_ ~

<img src="https://github.com/miftahmoha/tinyllama/assets/102898329/43f42dfc-6b6c-4865-bdde-952785674fde" alt="TinyLlama Logo" width=550></img>


_Model classes and pre-training utilities for a tiny version of Llama in PyTorch._

</div>

## Installation

``` bash
pip install tinyllama
```

## Parsing

Parses single or multiple files.

```python
# ".txt" files
from tinyllama.readers import get_text
corpus = get_text("./txt_path")

# ".pdf" files
from tinyllama.readers import get_pdf_text
corpus = get_pdf_text("./pdf_path")
```

To parse multiple files:

```python
# ".txt" files
from tinyllama.readers import get_text
corpus = ''.join(get_text(pdf_path) for txt_path in txt_paths)

# ".pdf" files
from tinyllama.readers import get_pdf_text
corpus = ''.join(get_pdf_text(pdf_path) for pdf_path in pdf_paths)
```

## Pre-training a model

### Initializing a tokenizer

With a simple character-level tokenizer:

```python
from tinyllama.tokenizers import CharacterTokenizer
tokenizer = CharacterTokenizer()
```

To turn a corpus into tokens:

```python
tokens  = tokenizer.tokenize(corpus)
```

### Initializing a Llama model

```python
from tinyllama import Llama
model = Llama(context_window=500, emb_dim=10, n_heads=2, n_blocks=2, vocab_size=tokenizer.vocab_size)
```

#### Multi-Query attention

Multi-query attention allows to reduce the number of queries and keys inside a multi-head attention block, reducing the number of the parameters in the process and having the heads sharing queries and keys instead.

```python
model = Llama(context_window=500, emb_dim=10, n_heads=2, n_blocks=2, gq_ratio=1/2, vocab_size=tokenizer.vocab_size)
```

The parameter `gq_ratio` represents the ratio $\frac{number \  of \ queries/keys}{number \ of \ heads}$, `1/2` means dividing the number of queries and keys by 2. The default value is set to 1.

### Launching a pre-training job

```python
from tinyllama import TrainConfig, Trainer
TrainConfig = TrainConfig(batch_size=32, epochs=64, lr=1e-3, log_interval=50)
Trainer = Trainer(TrainConfig)
Trainer.run(model, tokens)
```

Logs are disabled by default, to activate set environement variable `DISABLE_LOGS` to 0 with `DISABLE_LOGS=0 python3 file.py`. 

## Insight

Insight class run a training job on a clone model and returns information related to the training state. 

To disable cloning, set `tune_on_clone` to `False`, you can set a custom training configuration for tuning with the argument `TUNE_CONFIG = TrainConfig(..)`.

### Gradients

Returns a histogram representing the distribution of the gradients with mean, standard deviation and saturation.

A high saturation is an indication that the model is not learning, very low saturation ≈0% indicates that it's learning way too much _(not very good)_.

#### Activations (SwiGLU layers)

Note that a training job is necessary, you don't want to keep those values in memory since you need to store the tensors at each forward pass. Before training, those values are _hooked_ then _retrieved_.

```python
from tinyllama.insight import SwigluInsight, SwigluPath

SwigluInsight_ = SwigluInsight(track_direction=SwigluPath.BACKWARD)
SwigluInsight_.run(model, tokens)
```

If your model is learning correctly, saturation should stabilize as you go deeper into the layers.

<div align="center"> <img src="https://github.com/user-attachments/assets/24fe35ce-5eeb-4633-8129-86e722198914" alt="swiglu" width=500></img> </div>

![data2](https://github.com/user-attachments/assets/6b56eb9c-af4d-477b-b561-acff948984c0)

By default, `track_direction` is set to `SwigluPath.BACKWARD`. If you want to look at the forward activation, set it to `SwigluPath.FORWARD`.

#### Parameters

```python
from tinyllama.insight import GradInsight
GradInsight_ = GradInsight(num_params_to_track=1500)
GradInsight_.run(model)
```

<div align="center"> <img src="https://github.com/user-attachments/assets/1779b234-097d-4a33-8088-e5ae2c728836" alt="gradients" width=500></img> </div>

![data1](https://github.com/user-attachments/assets/d16d38e2-eaae-4dac-b18c-6dec962978bc)

This is an example of a high saturation, also we don't see an well rounded distribution. 

To avoid clutter, the legend is disabled. If you're tracking a small number of parameters, set argument `show_params_name` to `True`.

### Gradient over data ratio $\frac{l_r \cdot grad}{data}$

Returns a plot representing the gradient/data ratio in each step of the training. 

```python
from tinyllama.insight import GdrInsight
GdrInsight = GdrInsight(num_params_to_track=50, num_iters=1500)
GdrInsight.run(model, tokens)
```

Ratios should stabilize as training goes, high values means the network is learning way too fast _(not good)_ while low values means that it's learning way too slow _(not good aswell)_. Usually you want to observe values in the `1e-2` ~ `1e-3` range.

<div align="center"> <img src="https://github.com/user-attachments/assets/4064dbc1-ca7a-4d1d-97e8-79f31b11a8c9" alt="gradients" width=500></img> </div>

Not surprising after looking at the previous graphs, however this metric will show its usefulness when the other metrics fail _(when the model doesn't learn even with low saturations)_. 

To avoid clutter, the legend is disabled. If you're tracking a small number of parameters, set argument `show_params_name` to `True`.

### Learning rate

Returns a plot representing the loss for each learning rate, _the scale for the argument start and end is logarithmic_. 

```python
from tinyllama.insight import LrInsight                                                                                                         
LrInsight_ = LrInsight(start=-5, end=0, n_lrs=50)
LrInsight_.run(model, tokens)
```

<div align="center"> <img src="https://github.com/user-attachments/assets/bbd8f8c7-5d20-4e2e-a27f-72f42b777e05" alt="lr" width=500></img> </div>

For each `lr`, we set an `epoch` of `1`. Feel free to change it with the argument `epochs_for_each`.

### Hyperparameter tuning

Plots and returns a tuple containaing (1) training datapoints and the associated loss _(evaluated with training)_ and (2) testing datapoints and their **estimated** loss _(evaluated with a Gaussian process)_.

If you want to disable plots, set environement variable `DISABLE_PLOT` to 0.

```python
from tinyllama.gptuner import GPTuneConfig, GPTune
GPTuneConfig = GPTuneConfig(max_num_training_samples=100, hyperparams_to_tune=["emb_dim", "n_heads"], l_bounds=[10, 2], u_bounds=[50, 5], max_num_evaluations=500)
GPTune = GPTune(GPTuneConfig)
XY_train, XY_test = GPTune.run(model, tokens, TrainConfig)
```

`GPTune` predicts the loss of different hyperparameter configurations without running full training cycles. It uses a Gaussian process model that learns from a small set of evaluated training samples to estimate performance across the entire hyperparameter space.

`max_num_training_samples`: sets the number of training samples, more training samples means better overall coverage of the space which will lead to better precision. The samples are extracted using a latin hypercube, depends on how the space is constrained (intervals where hyperparameters lie), there'll be a maximum number of samples that can fit into the space.

`l_bounds`: sets lower bounds of each hyperparameter, follows the order of `hyperparams_to_tune`.

`u_bounds`: sets upper bounds of each hyperparameter, follows the order of `hyperparams_to_tune`.

`hyperparams_to_tune`: sets the hyperparameters to tune, the others are extracted from model.

`hyperparams_to_plot`: sets the hyperparameters to plot, it must be of length `<= 2` and a subset of `hyperparams_to_tune`.

`max_num_evaluation_samples`: sets the numbers of evaluations, same observation concerning the constrained space in which the number of integer samples is finite.

Numbers of hyparameters needs to be <= 2 to get a plot, if you still want to get a plot of subset, use `hyperparams_to_plot` argument to the list of hyperparameters that you want to plot.

```python
from tinyllama.gptuner import GPTuneConfig, GPTune
GPTuneConfig = GPTuneConfig(max_num_training_samples=100, hyperparams_to_tune=[""emb_dim"", "n_heads", "context_window"], hyperparams_to_plot=["epochs", "n_heads"] l_bounds=[10, 2, 150], u_bounds=[50, 5, 250], max_num_evaluations=500)
GPTune = GPTune(GPTuneConfig)
GPTune.run(model, tokens, TrainConfig)
```

<div align="center"> <img src="https://github.com/user-attachments/assets/d31f9027-7dde-4d3a-bdd8-06a5f03bed38" alt="gptune_3d" width=500></img> </div>

You can also have 1D plots.

```python
from tinyllama.gptuner import GPTuneConfig, GPTune
GPTuneConfig = GPTuneConfig(max_num_training_samples=100, hyperparams_to_tune=["epochs", "n_heads", "context_window"], hyperparams_to_plot=["n_heads"] l_bounds=[10, 2, 150], u_bounds=[50, 5, 250], max_num_evaluations=500)
GPTune = GPTune(GPTuneConfig)
GPTune.run(model, tokens, TrainConfig)
```

<div align="center"> <img src="https://github.com/user-attachments/assets/1c4c28d9-7c2e-44a9-885e-4370f45f08d9" alt="gptune_2d" width=500></img> </div>


## Generating

Generates a response to a prompt.

```python
from tinyllama import generate
# kv_cache is set to True by default.
generate(model, prompt, max_tokens=900, kv_cache=True)
```
