from qibo import Circuit, gates


class QEC:
    """A class for Quantum Error Correction (QEC) codes."""

    def __init__(self, code_type="bit_flip"):

        self.code_type:str = code_type
        self.encoded_circuit:Circuit = None
        self.encoded_nqb:int = 0

        print(f"Initialized QEC with code type: {self.code_type}")


    def apply_code(self, circuit:Circuit) -> Circuit|None:

        match self.code_type:

            case "bit_flip":
                return self.bit_flip_code(circuit)

        return self.encoded_circuit

    def bit_flip_code(self, circuit:Circuit) -> Circuit|None:

        self.encoded_nqb = circuit.nqubits * 3 + 2 * circuit.nqubits
        print(f"Applying {self.code_type} code to a circuit with {self.encoded_nqb} qubit(s).")

        # Create new wire names for the encoded circuit
        self.wire_names = []
        for i in range(circuit.nqubits):
            for j in range(3):
                self.wire_names.append(f"q{i}{j}")
            self.wire_names.append(f"a{i}0")
            self.wire_names.append(f"a{i}1")
                
        # Initialize the encoded circuit
        self.encoded_circuit = Circuit(self.encoded_nqb, wire_names=self.wire_names)

        # Encoding: Apply CNOT gates to encode each qubit into three qubits
        for i in range(circuit.nqubits):
            self.encoded_circuit.add(gates.CNOT(i*5, i*5+1))
            self.encoded_circuit.add(gates.CNOT(i*5, i*5+2))

        # Map original gates to the encoded circuit
        
        print(circuit.associate_gates_with_parameters())
        ##

        # Stabilizer measurements: Measure syndromes using ancilla qubits
        for i in range(circuit.nqubits):

            # Measure Z0Z1
            self.encoded_circuit.add(gates.H(i*5+3))
            self.encoded_circuit.add(gates.CZ(i*5, i*5+3))
            self.encoded_circuit.add(gates.CZ(i*5+1, i*5+3))
            self.encoded_circuit.add(gates.H(i*5+3))

            # Measure Z1Z2
            self.encoded_circuit.add(gates.H(i*5+4))
            self.encoded_circuit.add(gates.CZ(i*5+1, i*5+4))
            self.encoded_circuit.add(gates.CZ(i*5+2, i*5+4))
            self.encoded_circuit.add(gates.H(i*5+4))


        return self.encoded_circuit