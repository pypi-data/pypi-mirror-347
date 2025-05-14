"""This package contains implementations of QUBO :py:class:`~tno.quantum.optimization.qubo.components.Postprocessor` s.

Example:
-------
The following example shows how to list the available postprocessors and how to instantiate them.

>>> from tno.quantum.optimization.qubo.components import PostprocessorConfig
>>> list(PostprocessorConfig.supported_items())
['steepest_descent_postprocessor']
>>> postprocessor = PostprocessorConfig(name='steepest_descent_postprocessor').get_instance()

Alternatively, a postprocessor can also be instantiated directly.

>>> from tno.quantum.optimization.qubo.postprocessors import SteepestDescentPostprocessor
>>> postprocessor = SteepestDescentPostprocessor()
"""  # noqa: E501

from tno.quantum.optimization.qubo.postprocessors._dwave._steepest_descent_postprocessor import (  # noqa: E501
    SteepestDescentPostprocessor,
)

__all__ = ["SteepestDescentPostprocessor"]

__version__ = "1.0.0"
