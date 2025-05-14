# TNO Quantum: Optimization - QUBO - Postprocessors

TNO Quantum provides generic software components aimed at facilitating the development
of quantum applications.

This package contains implementations of QUBO postprocessors.

## Documentation

Documentation of the `tno.quantum.optimization.qubo.postprocessors` package can be found [here](https://tno-quantum.github.io/documentation/).


## Install

Easily install the `tno.quantum.optimization.qubo.postprocessors` package using pip:

```console
$ python -m pip install tno.quantum.optimization.qubo.postprocessors
```

## Usage

The following example shows how to list the available postprocessors and how to instantiate them.

```python
from tno.quantum.optimization.qubo.components import PostprocessorConfig
supported_postprocessors = PostprocessorConfig.supported_items()
postprocessor = PostprocessorConfig(name='steepest_descent_postprocessor').get_instance()
```

Alternatively, a postprocessor can also be instantiated directly.

```python
from tno.quantum.optimization.qubo.postprocessors import SteepestDescentPostprocessor
postprocessor = SteepestDescentPostprocessor()
```

## (End)use limitations
The content of this software may solely be used for applications that comply with international export control laws.
