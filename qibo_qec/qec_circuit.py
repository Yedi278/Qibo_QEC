from qibo import Circuit, gates
from qibo.result import CircuitResult
from qibo.backends import _check_backend, _Global

class Qec_Circuit(Circuit):
    """A subclass of qibo.Circuit for error corrected circuits."""

    def __init__(self, 
                circuit:Circuit=None, 
                nqubits:int=None, 
                accelerators=None, 
                density_matrix: bool = False,
                wire_names:list[str]=[],
                **kwargs):
        super().__init__(nqubits=nqubits, accelerators=accelerators, density_matrix=density_matrix, wire_names=wire_names, **kwargs)

        self.circuit = circuit
        self.qec_circuit = Circuit(nqubits=nqubits, wire_names=wire_names)
        self.results = None

    def __call__(self, initial_state=None, nshots=1024, **kwargs):

        self.results:CircuitResult = self.execute(initial_state=initial_state, nshots=nshots, kwargs=kwargs)

        return self.results
    

    
