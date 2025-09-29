from qibo import Circuit, gates

class Qec_Circuit(Circuit):
    """A subclass of qibo.Circuit for error corrected circuits."""

    def __init__(self, circuit:Circuit, nqubits:int=0, wire_names:list[str]=[]):
        super().__init__(nqubits=nqubits, wire_names=wire_names)

        self.circuit = circuit
        self.qec_circuit = Circuit(nqubits=nqubits, wire_names=wire_names)

    def __init__(self, nqubits:int=0, wire_names:list[str]=[]):
        super().__init__(nqubits=nqubits, wire_names=wire_names)

        self.qec_circuit = Circuit(nqubits=nqubits, wire_names=wire_names)

    def __call__(self, initial_state=None, nshots=1024, **kwargs):

        results = self.execute(initial_state=initial_state, nshots=nshots, kwargs=kwargs)

        results_dict = results.__dict__

        print((results_dict['_state']))

        return results