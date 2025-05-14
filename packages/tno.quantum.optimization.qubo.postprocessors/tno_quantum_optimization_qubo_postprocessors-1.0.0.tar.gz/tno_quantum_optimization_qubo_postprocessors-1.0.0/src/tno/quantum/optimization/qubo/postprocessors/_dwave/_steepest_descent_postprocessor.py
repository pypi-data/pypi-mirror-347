"""This module contains the ``SteepestDescentPostprocessor`` class."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, SupportsInt

from numpy.random import RandomState

from tno.quantum.optimization.qubo.components import Postprocessor
from tno.quantum.optimization.qubo.solvers import (
    DimodSampleSetResult,
    SteepestDescentSolver,
)
from tno.quantum.utils.validation import (
    check_int,
    check_kwarglike,
    check_random_state,
)

if TYPE_CHECKING:
    from tno.quantum.optimization.qubo.components import QUBO, ResultInterface


class SteepestDescentPostprocessor(Postprocessor[DimodSampleSetResult]):
    """Implementation of :py:class:`~tno.quantum.optimization.qubo.components.Postprocessor` using steepest descent.

    This postprocessor makes use of :py:class:`~tno.quantum.optimization.qubo.solvers.SteepestDescentSolver`.

    Example:
        >>> from tno.quantum.optimization.qubo.components import QUBO, BasicResult
        >>> from tno.quantum.optimization.qubo.postprocessors import SteepestDescentPostprocessor
        >>>
        >>> qubo = QUBO([[1, 2, 3], [4, -50, 6], [7, 8, 9]])
        >>> hint = BasicResult.from_result("000", 0.0) # or obtain a result from a solver
        >>>
        >>> postprocessor = SteepestDescentPostprocessor()
        >>> result = postprocessor.postprocess(qubo, hint)
        >>> result.best_bitvector
        BitVector(010)
    """  # noqa: E501

    def __init__(
        self,
        random_state: int | RandomState | None = None,
        num_reads: SupportsInt = 1,
        **sample_kwargs: Any,
    ) -> None:
        """Init :py:class:`SteepestDescentPostprocessor`.

        Args:
            random_state: Random state for reproducibility. Overrides the D-Wave
                `seed` argument. Default is ``None``.
            num_reads: Maximum number of random samples to be drawn. Default is 1.
            sample_kwargs: Additional keyword arguments that can be used for the
                sampler. See the `D-Wave documentation`__ for possible additional
                keyword definitions.

        Raises:
            ValueError: If `random_state` has invalid value, or `num_reads` is less
                than 1.
            TypeError: If `num_reads` is not an integer.

        .. __: https://docs.ocean.dwavesys.com/en/stable/docs_samplers/generated/dwave.samplers.SteepestDescentSolver.sample.html
        """
        self.solver = SteepestDescentSolver(
            random_state=check_random_state(random_state, "random_state"),
            num_reads=check_int(num_reads, "num_reads", l_bound=1),
            **sample_kwargs,
        )

    @property
    def random_state(self) -> RandomState:
        return self.solver.random_state

    @random_state.setter
    def random_state(self, value: int | RandomState | None = None) -> None:
        self.solver.random_state = check_random_state(value, "random_state")

    @property
    def num_reads(self) -> int:
        return self.solver.num_reads

    @num_reads.setter
    def num_reads(self, value: SupportsInt) -> None:
        self.solver.num_reads = check_int(value, "num_reads", l_bound=1)

    @property
    def sample_kwargs(self) -> dict[str, Any]:
        return self.solver.sample_kwargs

    @sample_kwargs.setter
    def sample_kwargs(self, value: dict[str, Any]) -> None:
        self.solver.sample_kwargs = check_kwarglike(value, "sample_kwargs")

    def _postprocess(self, qubo: QUBO, hint: ResultInterface) -> DimodSampleSetResult:
        """Perform postprocessing on the given result with respect to the given QUBO."""
        # Generate initial states based on the previous result:
        # From the Freq object, take the bitvectors (with the lowest value first)
        # and duplicate the correct number of times.
        triples = [(bit_vector, value, num) for bit_vector, value, num in hint.freq]
        triples.sort(key=lambda triple: triple[1])
        initial_states = [
            bit_vector.bits for bit_vector, _, num in triples for _ in range(num)
        ]
        self.solver.sample_kwargs["initial_states"] = initial_states

        # Solve using underlying solver
        return self.solver.solve(qubo)
