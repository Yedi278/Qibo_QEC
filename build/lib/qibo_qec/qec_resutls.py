from qibo.result import CircuitResult, QuantumState, MeasurementOutcomes
from qibo.ui.drawing_utils import (
    QIBO_COMPLEMENTARY_COLOR,
    QIBO_DEFAULT_COLOR,
    generate_bitstring_combinations,
)

class Qec_Results(CircuitResult):
    """A subclass of qibo.CircuitResult for error corrected circuit results."""

    def __init__(self, results:QuantumState|MeasurementOutcomes):
        super().__init__(results)
        self.bit_string_combinations = generate_bitstring_combinations(self.nqubits)
    