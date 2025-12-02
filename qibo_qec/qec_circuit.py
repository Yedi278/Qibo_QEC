from qibo import Circuit
from qibo.result import CircuitResult
import numpy as np

class Qec_Circuit(Circuit):
    """A subclass of qibo.Circuit for error corrected circuits."""

    def __init__(self, 
                circuit:Circuit=None, 
                nqubits:int=None, 
                accelerators=None, 
                density_matrix: bool = False,
                wire_names:list[str]=None,
                **kwargs):
        
        super().__init__(nqubits=nqubits, accelerators=accelerators, density_matrix=density_matrix, wire_names=wire_names, **kwargs)

        self.circuit = circuit
        self.qec_circuit = Circuit(nqubits=nqubits, wire_names=wire_names)
        self.results = None

    def generate_bitstring_combinations(self, n):
        """Generate all bitstring combinations given bitstring length `n`."""
        bitstrings = []
        for i in range(2**n):
            bitstrings.append(format(i, f"0{n}b"))
        return bitstrings

    def transform_initial_state(self, initial_state):

        initial_state_transformed = np.zeros(2**self.nqubits, dtype=complex)
        initial_state_transformed[0] = 1.0        

        if initial_state is None: return initial_state_transformed
        
        if(np.abs(np.linalg.norm(initial_state) - 1.0) > 1e-8):
            print("Initial state is not normalized.")
            return None

        num_states_old = len(initial_state)
        nqubits_original = int(np.log2(num_states_old))

        ratio = self.nqubits // nqubits_original
        
        for i in range(num_states_old):

            b = format(i, f"0{nqubits_original}b")

            b_transformed = ''
            for bit in b:
                b_transformed += f'{bit}'+'0'*(ratio-1)

            initial_state_transformed[int(b_transformed, 2)] = initial_state[i]

        return initial_state_transformed

    def __call__(self, initial_state=None, nshots=1024, **kwargs):

        initial_state_transformed = self.transform_initial_state(initial_state)
        
        self.results:CircuitResult = self.execute(initial_state=initial_state_transformed, nshots=nshots, **kwargs)

        return self.results
    

if __name__ == "__main__":
    from qibo import gates

    qc = Circuit(3)
    # qc.add([ gates.H(0) ])

    qc_qec = Qec_Circuit(qc, nqubits=qc.nqubits*3)

    initial_state = np.zeros(2**qc.nqubits, dtype=complex)

    initial_state[7] = 1.0

    result = qc_qec(initial_state=initial_state, nshots=1000)

    print(result)
