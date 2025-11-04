from qibo.result import CircuitResult, QuantumState, MeasurementOutcomes

class Qec_Results(CircuitResult):
    """A subclass of qibo.CircuitResult for error corrected circuit results."""

    def __init__(self, state:QuantumState, outcomes:MeasurementOutcomes):
        super().__init__(state=state, outcomes=outcomes)
        