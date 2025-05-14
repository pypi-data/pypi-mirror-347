"""This module contains tests for the ``SteepestDescentPostprocessor`` class."""

from tno.quantum.optimization.qubo.components import (
    QUBO,
    BasicResult,
    PostprocessorConfig,
)
from tno.quantum.optimization.qubo.postprocessors import SteepestDescentPostprocessor
from tno.quantum.utils import BitVector


def test_supported_items() -> None:
    """Test if `SteepestDescentPostprocessor` appears as supported item."""
    supported_items = PostprocessorConfig.supported_items()
    assert "steepest_descent_postprocessor" in supported_items
    assert (
        supported_items["steepest_descent_postprocessor"]
        is SteepestDescentPostprocessor
    )


def test_steepest_descent_default() -> None:
    """Test basic postprocessing of `SteepestDescentPostProcessor`."""
    postprocessor = SteepestDescentPostprocessor()

    qubo = QUBO([[1, 2, 3], [4, -50, 6], [7, 8, 9]])
    hint = BasicResult.from_result("000", 0.0)

    result = postprocessor.postprocess(qubo, hint)

    assert result.best_bitvector == BitVector("010")
    assert result.best_value == float("-50.0")
