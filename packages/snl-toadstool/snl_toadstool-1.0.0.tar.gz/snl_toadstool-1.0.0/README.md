Summary
-------
The primary objective of Toadstool is to provide the PyTorch boilerplate for training and testing loops, along with a callback interface that allows for any customizability you'd like. (See: models/dl\_utils.py)

A secondary objective of Toadstool is to provide generally useful callbacks and other methods for conducting deep learning experiments. (See: everything else)

Toadstool is meant to be a shallow abstraction over PyTorch and thus does not abstract many decisions other training libraries will hide from end users.

Basic Usage
-----------
``` python
from toadstool import Trainer
from toadstool.models.callbacks import CudaCallback, EarlyStopping, GradClipCallback, MonitorCallback

num_epochs = 5
t = Trainer(model, optim, loss_fn,
            callbacks=[GradClipCallback(),
                       MonitorCallback(),
                       EarlyStopping(patience=1),
                       CudaCallback(device)],
               opt_to_none=True)
t.fit(num_epochs, trainl, validl)
```
In its simplest form:
- `model`: torch.nn.Module
- `optim`: torch.optim.Optimizer
- `loss_fn`: torch.nn.modules.loss.*
- `trainl`, `validl`: torch.nn.data.dataloader

However, all are duck typed, so you can easily wrap them to suit your needs.

Basic tenets of Toadstool:
1. You design the model
    - should accept the `x` (batch) from the dataset and should return a `y^` (predicted target) that is accepted by the loss function.
2. You design the data
    - should return a tuple (x, y) or (batch, target)
        - x is passed to the model
        - y is passed to the loss function

Examples
--------

The following examples aim to demonstrate the basic use case of toadstool.
Toadstool focuses on handling the boilerplate PyTorch code of running data through a model.
While Toadstool does come with some example models and datasets that match the expected Toadstool format
(see Basic Usage), these exemplars are not required to be used.
The Toadstool models and datasets were originally created for a specific task,
but are intended to be generic enough to be useful on additional tasks.

The expected use cases of Toadstool are:
1. creating custom models and datasets that match the framework
2. creating callbacks and wrappers that adapt already created models and datasets to the framework

Included examples:

`example.ipynb`
> **Task**: Sentiment classification on IMDB dataset
>
> **Format**: Utilizes Toadstool model (`toadstool.models.zoo.TransformerModel`) on the torchtext dataset `IMDB`.

Advanced Topics
---------------
### Distributed training
`src/toadstool/distributed.py` contains helper functions for setting up a process group and executing a `run_fn` worker
call for that process group.

Especially useful along with `toadstool.models.utils` `fsdp_wrap` and `ddp_wrap` to automatically shard/distribute data
and model interactions across the process group.

Contributing
------------
Please insure any pull requests pass `ruff format`, `ruff check`, and `pytest`


Testing
-------

Tests are in the `tests` folder. See documentation on pytest for information on
how to write and extend these tests. The tests are a blend of unit and behavior
tests.

To test, make sure you have installed pytest and the other dependencies needed
for the toadstool codebase. Then, in the app root, run:
```
pytest
```
for more extensive tests of the given example models
```
pytest --models
```
