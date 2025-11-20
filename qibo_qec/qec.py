from qibo import Circuit, gates
from .qec_circuit import Qec_Circuit

class QEC:
    """A class for Quantum Error Correction (QEC) codes."""

    def __init__(self, code_type="bit_flip"):

        self.code_type:str = code_type
        self.log:bool = True
        self.encoded_circuit:Circuit = None
        self.encoded_nqb:int = 0    # Number of qubits in the encoded circuit
        self.wire_names:list[str] = [] # Wire names for the encoded circuit
        self.meas_target:list[int] = [] # List to store measurement gates targets

        print(f"Initialized QEC with code type: {self.code_type}")

    def apply_code(self, circuit:Circuit, test_gates:list=None, correction:bool=True) -> Qec_Circuit:
        """Applies the selected QEC code to the given quantum circuit."""

        self.encoded_circuit = None
        match self.code_type:

            case "bit_flip":
                return self.bit_flip_code(circuit, test_gates, correction)
            case "phase_flip":
                return self.phase_flip_code(circuit, test_gates, correction)
            case _:
                raise NotImplementedError(f"Code type {self.code_type} not supported yet.")

        return self.encoded_circuit

    def bit_flip_code(self, circuit:Circuit, test_gates:list=None, correction:bool=True) -> Qec_Circuit:
        """Applies the Bit-Flip QEC code to the given quantum circuit."""

        self.encoded_nqb = circuit.nqubits * 3
        if self.log: print(f"Applying {self.code_type} code to a circuit with {self.encoded_nqb} qubit(s).")

        # Create new wire names for the encoded circuit
        self.wire_names = []
        for i in range(circuit.nqubits):
            self.wire_names.append(f"q_{i}")
            self.wire_names.append(f"a_{i}0")
            self.wire_names.append(f"a_{i}1")

        # Initialize the encoded circuit
        self.encoded_circuit = Qec_Circuit(circuit=circuit, nqubits=self.encoded_nqb, wire_names=self.wire_names)

        # Encoding: Apply CNOT gates to encode each qubit into three qubits
        for i in range(circuit.nqubits):
            self.encoded_circuit.add(gates.CNOT(i*3, i*3+1))
            self.encoded_circuit.add(gates.CNOT(i*3, i*3+2))

        # add test error gates if provided

        if test_gates is not None:
            for gate in test_gates:
                self.encoded_circuit.add(gate)

        # Map original gates to the encoded circuit
        
        for gate_ in circuit.queue:
            gate = gate_.__dict__

            match gate["name"]:
                
                case "x":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.X(target*3))
                    self.encoded_circuit.add(gates.X(target*3+1))
                    self.encoded_circuit.add(gates.X(target*3+2))

                case "z":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.Z(target*3))
                    self.encoded_circuit.add(gates.Z(target*3+1))
                    self.encoded_circuit.add(gates.Z(target*3+2))

                case "h":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.H(target*3))
                    self.encoded_circuit.add(gates.H(target*3+1))
                    self.encoded_circuit.add(gates.H(target*3+2))

                case "cx":
                    control = gate["_control_qubits"][0]
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.CNOT(control*3, target*3))
                    self.encoded_circuit.add(gates.CNOT(control*3+1, target*3+1))
                    self.encoded_circuit.add(gates.CNOT(control*3+2, target*3+2))
                
                case "measure":
                    self.meas_target.append(gate['_target_qubits'][0])  # Store measurement target for later
                

                case _:
                    print(f"Gate {gate['name']} not supported in bit-flip code yet.")

        # # Stabilizer measurements: Measure syndromes using ancilla qubits
        # for i in range(circuit.nqubits):

        #     # Measure Z0Z1
        #     self.encoded_circuit.add(gates.H(i*5+3))
        #     self.encoded_circuit.add(gates.CZ(i*5, i*5+3))
        #     self.encoded_circuit.add(gates.CZ(i*5+1, i*5+3))
        #     self.encoded_circuit.add(gates.H(i*5+3))

        #     # Measure Z1Z2
        #     self.encoded_circuit.add(gates.H(i*5+4))
        #     self.encoded_circuit.add(gates.CZ(i*5+1, i*5+4))
        #     self.encoded_circuit.add(gates.CZ(i*5+2, i*5+4))
        #     self.encoded_circuit.add(gates.H(i*5+4))

        if correction:
            for i in range(circuit.nqubits):

                self.encoded_circuit.add(gates.CNOT(i*3, i*3+1))
                self.encoded_circuit.add(gates.CNOT(i*3, i*3+2))
                self.encoded_circuit.add(gates.TOFFOLI(i*3+1, i*3+2, i*3))

        # Final measurements if the original circuit had measurements
        if self.meas_target:
            for target in self.meas_target:
                self.encoded_circuit.add(gates.M(target*3))

        return self.encoded_circuit
    

    def phase_flip_code(self, circuit:Circuit, test_gates:list=None, correction:bool=True) -> Qec_Circuit:
        """Applies the Phase-Flip QEC code to the given quantum circuit."""

        self.encoded_nqb = circuit.nqubits * 3
        if self.log: print(f"Applying {self.code_type} code to a circuit with {self.encoded_nqb} qubit(s).")

        # Create new wire names for the encoded circuit
        self.wire_names = []
        for i in range(circuit.nqubits):
            self.wire_names.append(f"q_{i}")
            self.wire_names.append(f"a_{i}0")
            self.wire_names.append(f"a_{i}1")

        # Initialize the encoded circuit
        self.encoded_circuit = Qec_Circuit(circuit=circuit, nqubits=self.encoded_nqb, wire_names=self.wire_names)

        # Encoding: Apply CNOT gates to encode each qubit into three qubits
        for i in range(circuit.nqubits):
            self.encoded_circuit.add(gates.CNOT(i*3, i*3+1))
            self.encoded_circuit.add(gates.CNOT(i*3, i*3+2))
            self.encoded_circuit.add( [ gates.H(i*3), 
                                        gates.H(i*3+1), 
                                        gates.H(i*3+2) 
                                        ] )

        # add test error gates if provided
        if test_gates is not None:
            for gate in test_gates:
                self.encoded_circuit.add(gate)
        
        # Map original gates to the encoded circuit
        for gate_ in circuit.queue:
            gate = gate_.__dict__

            match gate["name"]:
                
                case "x":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.X(target*3))
                    self.encoded_circuit.add(gates.X(target*3+1))
                    self.encoded_circuit.add(gates.X(target*3+2))

                case "z":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.Z(target*3))
                    self.encoded_circuit.add(gates.Z(target*3+1))
                    self.encoded_circuit.add(gates.Z(target*3+2))

                case "h":
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.H(target*3))
                    self.encoded_circuit.add(gates.H(target*3+1))
                    self.encoded_circuit.add(gates.H(target*3+2))

                case "cx":
                    control = gate["_control_qubits"][0]
                    target = gate["_target_qubits"][0]
                    self.encoded_circuit.add(gates.CNOT(control*3, target*3))
                    self.encoded_circuit.add(gates.CNOT(control*3+1, target*3+1))
                    self.encoded_circuit.add(gates.CNOT(control*3+2, target*3+2))
                
                case "measure":
                    self.meas_target.append(gate['_target_qubits'][0])  # Store measurement target for later

                case _:
                    print(f"Gate {gate['name']} not supported in bit-flip code yet.")

        if correction:
            for i in range(circuit.nqubits):
    
                self.encoded_circuit.add( [gates.H(i*3), gates.H(i*3+1), gates.H(i*3+2)])
                self.encoded_circuit.add(gates.CNOT(i*3, i*3+1))
                self.encoded_circuit.add(gates.CNOT(i*3, i*3+2))
                self.encoded_circuit.add(gates.TOFFOLI(i*3+1, i*3+2, i*3))

        # Final measurements if the original circuit had measurements
        if self.meas_target:
            for target in self.meas_target:
                self.encoded_circuit.add(gates.M(target*3))

        return self.encoded_circuit
    