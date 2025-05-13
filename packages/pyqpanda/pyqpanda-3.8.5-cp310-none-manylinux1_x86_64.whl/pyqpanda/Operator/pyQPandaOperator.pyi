import numpy
from typing import overload

class FermionOperator:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.FermionOperator) -> None

        2. __init__(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> None

        4. __init__(self: pyQPandaOperator.FermionOperator, arg0: str, arg1: complex) -> None

        5. __init__(self: pyQPandaOperator.FermionOperator, arg0: Dict[str, complex]) -> None
        """
    @overload
    def __init__(self, arg0: float) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.FermionOperator) -> None

        2. __init__(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> None

        4. __init__(self: pyQPandaOperator.FermionOperator, arg0: str, arg1: complex) -> None

        5. __init__(self: pyQPandaOperator.FermionOperator, arg0: Dict[str, complex]) -> None
        """
    @overload
    def __init__(self, arg0: complex) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.FermionOperator) -> None

        2. __init__(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> None

        4. __init__(self: pyQPandaOperator.FermionOperator, arg0: str, arg1: complex) -> None

        5. __init__(self: pyQPandaOperator.FermionOperator, arg0: Dict[str, complex]) -> None
        """
    @overload
    def __init__(self, arg0: str, arg1: complex) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.FermionOperator) -> None

        2. __init__(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> None

        4. __init__(self: pyQPandaOperator.FermionOperator, arg0: str, arg1: complex) -> None

        5. __init__(self: pyQPandaOperator.FermionOperator, arg0: Dict[str, complex]) -> None
        """
    @overload
    def __init__(self, arg0: dict[str, complex]) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.FermionOperator) -> None

        2. __init__(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> None

        4. __init__(self: pyQPandaOperator.FermionOperator, arg0: str, arg1: complex) -> None

        5. __init__(self: pyQPandaOperator.FermionOperator, arg0: Dict[str, complex]) -> None
        """
    def data(self) -> list[tuple[tuple[list[tuple[int, bool]], str], complex]]:
        """data(self: pyQPandaOperator.FermionOperator) -> List[Tuple[Tuple[List[Tuple[int, bool]], str], complex]]

        Get the data of the fermion operator.

        Args:
             None

        Returns:
             A data structure representing the fermion operator's data.

        """
    def error_threshold(self) -> float:
        """error_threshold(self: pyQPandaOperator.FermionOperator) -> float

        Retrieve the error threshold for the fermion operator.

        Args:
             None

        Returns:
             A double representing the error threshold.

        """
    def isEmpty(self) -> bool:
        """isEmpty(self: pyQPandaOperator.FermionOperator) -> bool"""
    def is_empty(self) -> bool:
        """is_empty(self: pyQPandaOperator.FermionOperator) -> bool

        Check if the fermion operator is empty.

        Args:
             None

        Returns:
             A boolean indicating whether the operator is empty.

        """
    def normal_ordered(self) -> FermionOperator:
        """normal_ordered(self: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        Returns the normal ordered form of the fermion operator.

        Args:
             None

        Returns:
             A new FermionOperator in normal ordered form.
        """
    def setErrorThreshold(self, arg0: float) -> None:
        """setErrorThreshold(self: pyQPandaOperator.FermionOperator, arg0: float) -> None"""
    def set_error_threshold(self, arg0: float) -> None:
        """set_error_threshold(self: pyQPandaOperator.FermionOperator, arg0: float) -> None

        Set the error threshold for the fermion operator.

        Args:
             threshold: A double representing the new error threshold.

        Returns:
             None.

        """
    def toString(self) -> str:
        """toString(self: pyQPandaOperator.FermionOperator) -> str"""
    def to_string(self) -> str:
        """to_string(self: pyQPandaOperator.FermionOperator) -> str

        Convert the fermion operator to a string representation.

        Args:
             None

        Returns:
             A string representing the fermion operator.

        """
    @overload
    def __add__(self, arg0: FermionOperator) -> FermionOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __add__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """
    @overload
    def __add__(self, arg0: complex) -> FermionOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __add__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """
    def __iadd__(self, arg0: FermionOperator) -> FermionOperator:
        """__iadd__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator"""
    def __imul__(self, arg0: FermionOperator) -> FermionOperator:
        """__imul__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator"""
    def __isub__(self, arg0: FermionOperator) -> FermionOperator:
        """__isub__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator"""
    @overload
    def __mul__(self, arg0: FermionOperator) -> FermionOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __mul__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """
    @overload
    def __mul__(self, arg0: complex) -> FermionOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __mul__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """
    def __radd__(self, arg0: complex) -> FermionOperator:
        """__radd__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator"""
    def __rmul__(self, arg0: complex) -> FermionOperator:
        """__rmul__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator"""
    def __rsub__(self, arg0: complex) -> FermionOperator:
        """__rsub__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator"""
    @overload
    def __sub__(self, arg0: FermionOperator) -> FermionOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __sub__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """
    @overload
    def __sub__(self, arg0: complex) -> FermionOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.FermionOperator, arg0: pyQPandaOperator.FermionOperator) -> pyQPandaOperator.FermionOperator

        2. __sub__(self: pyQPandaOperator.FermionOperator, arg0: complex) -> pyQPandaOperator.FermionOperator
        """

class PauliOperator:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.PauliOperator) -> None

        2. __init__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> None

        3. __init__(self: pyQPandaOperator.PauliOperator, matrix: List[List[float]], is_reduce_duplicates: bool = False) -> None

        4. __init__(self: pyQPandaOperator.PauliOperator, key: str, value: complex, is_reduce_duplicates: bool = False) -> None

        5. __init__(self: pyQPandaOperator.PauliOperator, pauli_map: Dict[str, complex], is_reduce_duplicates: bool = False) -> None
        """
    @overload
    def __init__(self, arg0: complex) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.PauliOperator) -> None

        2. __init__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> None

        3. __init__(self: pyQPandaOperator.PauliOperator, matrix: List[List[float]], is_reduce_duplicates: bool = False) -> None

        4. __init__(self: pyQPandaOperator.PauliOperator, key: str, value: complex, is_reduce_duplicates: bool = False) -> None

        5. __init__(self: pyQPandaOperator.PauliOperator, pauli_map: Dict[str, complex], is_reduce_duplicates: bool = False) -> None
        """
    @overload
    def __init__(self, matrix: list[list[float]], is_reduce_duplicates: bool = ...) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.PauliOperator) -> None

        2. __init__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> None

        3. __init__(self: pyQPandaOperator.PauliOperator, matrix: List[List[float]], is_reduce_duplicates: bool = False) -> None

        4. __init__(self: pyQPandaOperator.PauliOperator, key: str, value: complex, is_reduce_duplicates: bool = False) -> None

        5. __init__(self: pyQPandaOperator.PauliOperator, pauli_map: Dict[str, complex], is_reduce_duplicates: bool = False) -> None
        """
    @overload
    def __init__(self, key: str, value: complex, is_reduce_duplicates: bool = ...) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.PauliOperator) -> None

        2. __init__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> None

        3. __init__(self: pyQPandaOperator.PauliOperator, matrix: List[List[float]], is_reduce_duplicates: bool = False) -> None

        4. __init__(self: pyQPandaOperator.PauliOperator, key: str, value: complex, is_reduce_duplicates: bool = False) -> None

        5. __init__(self: pyQPandaOperator.PauliOperator, pauli_map: Dict[str, complex], is_reduce_duplicates: bool = False) -> None
        """
    @overload
    def __init__(self, pauli_map: dict[str, complex], is_reduce_duplicates: bool = ...) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.PauliOperator) -> None

        2. __init__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> None

        3. __init__(self: pyQPandaOperator.PauliOperator, matrix: List[List[float]], is_reduce_duplicates: bool = False) -> None

        4. __init__(self: pyQPandaOperator.PauliOperator, key: str, value: complex, is_reduce_duplicates: bool = False) -> None

        5. __init__(self: pyQPandaOperator.PauliOperator, pauli_map: Dict[str, complex], is_reduce_duplicates: bool = False) -> None
        """
    def dagger(self) -> PauliOperator:
        """dagger(self: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        Returns the adjoint (dagger) of the Pauli operator.

        This function computes and returns the adjoint of the current operator.

        Args:
             None

        Returns:
             A new instance of PauliOperator representing the adjoint.

        """
    def data(self) -> list[tuple[tuple[dict[int, str], str], complex]]:
        """data(self: pyQPandaOperator.PauliOperator) -> List[Tuple[Tuple[Dict[int, str], str], complex]]

        Retrieves the data representation of the Pauli operator.

        This function returns the internal data structure representing the operator.

        Args:
             None

        Returns:
             The data representation of the Pauli operator.

        """
    def error_threshold(self) -> float:
        """error_threshold(self: pyQPandaOperator.PauliOperator) -> float

        Retrieves the current error threshold for the operator.

        This function returns the error threshold value set for the operator.

        Args:
             None

        Returns:
             A double representing the error threshold.

        """
    def getMaxIndex(self) -> int:
        """getMaxIndex(self: pyQPandaOperator.PauliOperator) -> int"""
    def get_max_index(self) -> int:
        """get_max_index(self: pyQPandaOperator.PauliOperator) -> int

        Retrieves the maximum qubit index used in the operator.

        This function returns the highest index of qubits present in the Pauli operator.

        Args:
             None

        Returns:
             An integer representing the maximum qubit index.

        """
    def isAllPauliZorI(self) -> bool:
        """isAllPauliZorI(self: pyQPandaOperator.PauliOperator) -> bool"""
    def isEmpty(self) -> bool:
        """isEmpty(self: pyQPandaOperator.PauliOperator) -> bool"""
    def is_all_pauli_z_or_i(self) -> bool:
        """is_all_pauli_z_or_i(self: pyQPandaOperator.PauliOperator) -> bool

        Checks if all terms are either Pauli Z or identity.

        This function evaluates whether all components of the operator are either Pauli Z or the identity operator.

        Args:
             None

        Returns:
             A boolean indicating if all terms are Pauli Z or identity (true) or not (false).

        """
    def is_empty(self) -> bool:
        """is_empty(self: pyQPandaOperator.PauliOperator) -> bool

        Checks if the Pauli operator is empty.

        This function determines whether the current operator contains any terms.

        Args:
             None

        Returns:
             A boolean indicating if the operator is empty (true) or not (false).

        """
    def reduce_duplicates(self) -> None:
        """reduce_duplicates(self: pyQPandaOperator.PauliOperator) -> None

        Reduces duplicates in the Pauli operator representation.

        This function modifies the operator to remove duplicate elements.

        Args:
             None

        Returns:
             None.

        """
    def remapQubitIndex(self, arg0: dict[int, int]) -> PauliOperator:
        """remapQubitIndex(self: pyQPandaOperator.PauliOperator, arg0: Dict[int, int]) -> pyQPandaOperator.PauliOperator"""
    def remap_qubit_index(self, arg0: dict[int, int]) -> PauliOperator:
        """remap_qubit_index(self: pyQPandaOperator.PauliOperator, arg0: Dict[int, int]) -> pyQPandaOperator.PauliOperator

        Remaps the qubit indices in the operator.

        This function updates the qubit indices according to the provided mapping.

        Args:
             const std::map<int, int>& index_map: A mapping of old indices to new indices.

        Returns:
             None.

        """
    def setErrorThreshold(self, arg0: float) -> None:
        """setErrorThreshold(self: pyQPandaOperator.PauliOperator, arg0: float) -> None"""
    def set_error_threshold(self, arg0: float) -> None:
        """set_error_threshold(self: pyQPandaOperator.PauliOperator, arg0: float) -> None

        Sets the error threshold for the operator.

        This function allows the user to define a new error threshold value.

        Args:
             double threshold: The new error threshold value to set.

        Returns:
             None.

        """
    def toHamiltonian(self, arg0: bool) -> list[tuple[dict[int, str], float]]:
        """toHamiltonian(self: pyQPandaOperator.PauliOperator, arg0: bool) -> List[Tuple[Dict[int, str], float]]"""
    def toString(self) -> str:
        """toString(self: pyQPandaOperator.PauliOperator) -> str"""
    def to_hamiltonian(self, arg0: bool) -> list[tuple[dict[int, str], float]]:
        """to_hamiltonian(self: pyQPandaOperator.PauliOperator, arg0: bool) -> List[Tuple[Dict[int, str], float]]

        Converts the Pauli operator to its Hamiltonian representation.

        This function transforms the current Pauli operator into its corresponding Hamiltonian form.

        Args:
             None

        Returns:
             A new Hamiltonian representation of the operator.

        """
    def to_matrix(self) -> numpy.ndarray[numpy.complex128[m, n]]:
        """to_matrix(self: pyQPandaOperator.PauliOperator) -> numpy.ndarray[numpy.complex128[m, n]]

        Converts the Pauli operator to a matrix form.

        This function transforms the Pauli operator into its matrix representation.

        Args:
             None

        Returns:
             An EigenMatrixX representing the matrix form of the operator.

        """
    def to_string(self) -> str:
        """to_string(self: pyQPandaOperator.PauliOperator) -> str

        Converts the Pauli operator to a string representation.

        This function provides a human-readable format of the Pauli operator.

        Args:
             None

        Returns:
             A string representing the Pauli operator.

        """
    @overload
    def __add__(self, arg0: PauliOperator) -> PauliOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __add__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """
    @overload
    def __add__(self, arg0: complex) -> PauliOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __add__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """
    def __iadd__(self, arg0: PauliOperator) -> PauliOperator:
        """__iadd__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator"""
    def __imul__(self, arg0: PauliOperator) -> PauliOperator:
        """__imul__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator"""
    def __isub__(self, arg0: PauliOperator) -> PauliOperator:
        """__isub__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator"""
    @overload
    def __mul__(self, arg0: PauliOperator) -> PauliOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __mul__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """
    @overload
    def __mul__(self, arg0: complex) -> PauliOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __mul__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """
    def __radd__(self, arg0: complex) -> PauliOperator:
        """__radd__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator"""
    def __rmul__(self, arg0: complex) -> PauliOperator:
        """__rmul__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator"""
    def __rsub__(self, arg0: complex) -> PauliOperator:
        """__rsub__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator"""
    @overload
    def __sub__(self, arg0: PauliOperator) -> PauliOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __sub__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """
    @overload
    def __sub__(self, arg0: complex) -> PauliOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.PauliOperator, arg0: pyQPandaOperator.PauliOperator) -> pyQPandaOperator.PauliOperator

        2. __sub__(self: pyQPandaOperator.PauliOperator, arg0: complex) -> pyQPandaOperator.PauliOperator
        """

class VarFermionOperator:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarFermionOperator) -> None

        2. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: float) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarFermionOperator) -> None

        2. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: complex_var) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarFermionOperator) -> None

        2. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: str, arg1: complex_var) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarFermionOperator) -> None

        2. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: dict[str, complex_var]) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarFermionOperator) -> None

        2. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarFermionOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    def data(self) -> list[tuple[tuple[list[tuple[int, bool]], str], complex_var]]:
        """data(self: pyQPandaOperator.VarFermionOperator) -> List[Tuple[Tuple[List[Tuple[int, bool]], str], pyQPandaOperator.complex_var]]

        Get the data of the variable fermion operator.

        Args:
             None

        Returns:
             A data structure representing the variable fermion operator's data.

        """
    def error_threshold(self) -> float:
        """error_threshold(self: pyQPandaOperator.VarFermionOperator) -> float

        Retrieve the error threshold for the variable fermion operator.

        Args:
             None

        Returns:
             A double representing the error threshold.

        """
    def isEmpty(self) -> bool:
        """isEmpty(self: pyQPandaOperator.VarFermionOperator) -> bool"""
    def is_empty(self) -> bool:
        """is_empty(self: pyQPandaOperator.VarFermionOperator) -> bool

        Check if the variable fermion operator is empty.

        Args:
             None

        Returns:
             A boolean indicating whether the operator is empty.
        """
    def normal_ordered(self) -> VarFermionOperator:
        """normal_ordered(self: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        Returns the normal ordered form of the variable fermion operator.

        Args:
             None

        Returns:
             A new VarFermionOperator in normal ordered form.

        """
    def setErrorThreshold(self, arg0: float) -> None:
        """setErrorThreshold(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None"""
    def set_error_threshold(self, arg0: float) -> None:
        """set_error_threshold(self: pyQPandaOperator.VarFermionOperator, arg0: float) -> None

        Set the error threshold for the variable fermion operator.

        Args:
             threshold (double): A double representing the new error threshold.

        Returns:
             None.

        """
    def toString(self) -> str:
        """toString(self: pyQPandaOperator.VarFermionOperator) -> str"""
    def to_string(self) -> str:
        """to_string(self: pyQPandaOperator.VarFermionOperator) -> str

        Convert the variable fermion operator to a string representation.

        Args:
             None

        Returns:
             A string representing the variable fermion operator.

        """
    @overload
    def __add__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __add__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """
    @overload
    def __add__(self, arg0: complex_var) -> VarFermionOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __add__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """
    def __iadd__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__iadd__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator"""
    def __imul__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__imul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator"""
    def __isub__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__isub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator"""
    @overload
    def __mul__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __mul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """
    @overload
    def __mul__(self, arg0: complex_var) -> VarFermionOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __mul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """
    def __radd__(self, arg0: complex_var) -> VarFermionOperator:
        """__radd__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator"""
    def __rmul__(self, arg0: complex_var) -> VarFermionOperator:
        """__rmul__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator"""
    def __rsub__(self, arg0: complex_var) -> VarFermionOperator:
        """__rsub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator"""
    @overload
    def __sub__(self, arg0: VarFermionOperator) -> VarFermionOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __sub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """
    @overload
    def __sub__(self, arg0: complex_var) -> VarFermionOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.VarFermionOperator) -> pyQPandaOperator.VarFermionOperator

        2. __sub__(self: pyQPandaOperator.VarFermionOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarFermionOperator
        """

class VarPauliOperator:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarPauliOperator) -> None

        2. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: float) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarPauliOperator) -> None

        2. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: complex_var) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarPauliOperator) -> None

        2. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: str, arg1: complex_var) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarPauliOperator) -> None

        2. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    @overload
    def __init__(self, arg0: dict[str, complex_var]) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.VarPauliOperator) -> None

        2. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        3. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> None

        4. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: str, arg1: pyQPandaOperator.complex_var) -> None

        5. __init__(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[str, pyQPandaOperator.complex_var]) -> None
        """
    def dagger(self) -> VarPauliOperator:
        """dagger(self: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        Return the adjoint (dagger) of the Pauli operator.

        Args:
             None

        Returns:
             A new VarPauliOperator representing the adjoint.

        """
    def data(self) -> list[tuple[tuple[dict[int, str], str], complex_var]]:
        """data(self: pyQPandaOperator.VarPauliOperator) -> List[Tuple[Tuple[Dict[int, str], str], pyQPandaOperator.complex_var]]

        Get the data of the variable Pauli operator.

        Args:
             None

        Returns:
             A data structure representing the variable Pauli operator's data.

        """
    @overload
    def error_threshold(self) -> float:
        """error_threshold(*args, **kwargs)
        Overloaded function.

        1. error_threshold(self: pyQPandaOperator.VarPauliOperator) -> float

        2. error_threshold(self: pyQPandaOperator.VarPauliOperator) -> float

        Retrieve the error threshold for the variable Pauli operator.

        Args:
             None

        Returns:
             A double representing the error threshold.

        """
    @overload
    def error_threshold(self) -> float:
        """error_threshold(*args, **kwargs)
        Overloaded function.

        1. error_threshold(self: pyQPandaOperator.VarPauliOperator) -> float

        2. error_threshold(self: pyQPandaOperator.VarPauliOperator) -> float

        Retrieve the error threshold for the variable Pauli operator.

        Args:
             None

        Returns:
             A double representing the error threshold.

        """
    def getMaxIndex(self) -> int:
        """getMaxIndex(self: pyQPandaOperator.VarPauliOperator) -> int"""
    def get_maxIndex(self) -> int:
        """get_maxIndex(self: pyQPandaOperator.VarPauliOperator) -> int

        Retrieve the maximum index used in the Pauli operator.

        Args:
             None

        Returns:
             An integer representing the maximum index.

        """
    def isAllPauliZorI(self) -> bool:
        """isAllPauliZorI(self: pyQPandaOperator.VarPauliOperator) -> bool"""
    def isEmpty(self) -> bool:
        """isEmpty(self: pyQPandaOperator.VarPauliOperator) -> bool"""
    def is_all_pauli_z_or_i(self) -> bool:
        """is_all_pauli_z_or_i(self: pyQPandaOperator.VarPauliOperator) -> bool

        Check if the operator consists only of Pauli Z or identity.

        Args:
             None

        Returns:
             A boolean indicating if all operators are Z or I.

        """
    def is_empty(self) -> bool:
        """is_empty(self: pyQPandaOperator.VarPauliOperator) -> bool

        Check if the variable Pauli operator is empty.

        Args:
             None

        Returns:
             A boolean indicating whether the operator is empty.

        """
    def remapQubitIndex(self, arg0: dict[int, int]) -> VarPauliOperator:
        """remapQubitIndex(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[int, int]) -> pyQPandaOperator.VarPauliOperator"""
    def remap_qubit_index(self, arg0: dict[int, int]) -> VarPauliOperator:
        """remap_qubit_index(self: pyQPandaOperator.VarPauliOperator, arg0: Dict[int, int]) -> pyQPandaOperator.VarPauliOperator

        Remap the qubit indices of the variable Pauli operator.

        Args:
             A mapping of old indices to new indices.

        Returns:
             None.

        """
    def setErrorThreshold(self, arg0: float) -> None:
        """setErrorThreshold(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None"""
    def set_error_threshold(self, arg0: float) -> None:
        """set_error_threshold(self: pyQPandaOperator.VarPauliOperator, arg0: float) -> None

        Set the error threshold for the variable Pauli operator.

        Args:
             threshold (double): A double representing the new error threshold.

        Returns:
             None.

        """
    def toHamiltonian(self, arg0: bool) -> list[tuple[dict[int, str], float]]:
        """toHamiltonian(self: pyQPandaOperator.VarPauliOperator, arg0: bool) -> List[Tuple[Dict[int, str], float]]"""
    def toString(self) -> str:
        """toString(self: pyQPandaOperator.VarPauliOperator) -> str"""
    def to_hamiltonian(self, arg0: bool) -> list[tuple[dict[int, str], float]]:
        """to_hamiltonian(self: pyQPandaOperator.VarPauliOperator, arg0: bool) -> List[Tuple[Dict[int, str], float]]

        Convert the variable Pauli operator to a Hamiltonian representation.

        Args:
             None

        Returns:
             A Hamiltonian representation of the operator.

        """
    def to_string(self) -> str:
        """to_string(self: pyQPandaOperator.VarPauliOperator) -> str

        Convert the variable Pauli operator to a string representation.

        Args:
             None

        Returns:
             A string representing the variable Pauli operator.

        """
    @overload
    def __add__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __add__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """
    @overload
    def __add__(self, arg0: complex_var) -> VarPauliOperator:
        """__add__(*args, **kwargs)
        Overloaded function.

        1. __add__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __add__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """
    def __iadd__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__iadd__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator"""
    def __imul__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__imul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator"""
    def __isub__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__isub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator"""
    @overload
    def __mul__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __mul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """
    @overload
    def __mul__(self, arg0: complex_var) -> VarPauliOperator:
        """__mul__(*args, **kwargs)
        Overloaded function.

        1. __mul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __mul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """
    def __radd__(self, arg0: complex_var) -> VarPauliOperator:
        """__radd__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator"""
    def __rmul__(self, arg0: complex_var) -> VarPauliOperator:
        """__rmul__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator"""
    def __rsub__(self, arg0: complex_var) -> VarPauliOperator:
        """__rsub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator"""
    @overload
    def __sub__(self, arg0: VarPauliOperator) -> VarPauliOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __sub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """
    @overload
    def __sub__(self, arg0: complex_var) -> VarPauliOperator:
        """__sub__(*args, **kwargs)
        Overloaded function.

        1. __sub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.VarPauliOperator) -> pyQPandaOperator.VarPauliOperator

        2. __sub__(self: pyQPandaOperator.VarPauliOperator, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.VarPauliOperator
        """

class complex_var:
    @overload
    def __init__(self) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.complex_var) -> None

        2. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var) -> None

        3. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var, arg1: QPanda::Variational::var) -> None
        """
    @overload
    def __init__(self, arg0) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.complex_var) -> None

        2. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var) -> None

        3. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var, arg1: QPanda::Variational::var) -> None
        """
    @overload
    def __init__(self, arg0, arg1) -> None:
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: pyQPandaOperator.complex_var) -> None

        2. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var) -> None

        3. __init__(self: pyQPandaOperator.complex_var, arg0: QPanda::Variational::var, arg1: QPanda::Variational::var) -> None
        """
    def imag(self, *args, **kwargs):
        """imag(self: pyQPandaOperator.complex_var) -> QPanda::Variational::var"""
    def real(self, *args, **kwargs):
        """real(self: pyQPandaOperator.complex_var) -> QPanda::Variational::var"""
    def __add__(self, arg0: complex_var) -> complex_var:
        """__add__(self: pyQPandaOperator.complex_var, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.complex_var"""
    def __mul__(self, arg0: complex_var) -> complex_var:
        """__mul__(self: pyQPandaOperator.complex_var, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.complex_var"""
    def __sub__(self, arg0: complex_var) -> complex_var:
        """__sub__(self: pyQPandaOperator.complex_var, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.complex_var"""
    def __truediv__(self, arg0: complex_var) -> complex_var:
        """__truediv__(self: pyQPandaOperator.complex_var, arg0: pyQPandaOperator.complex_var) -> pyQPandaOperator.complex_var"""

def i(arg0: int) -> PauliOperator:
    """i(arg0: int) -> pyQPandaOperator.PauliOperator

    Construct a Pauli I operator.

    Args:
         index (int): Pauli operator index.

    Returns:
         Pauli operator I.

    """
def matrix_decompose_hamiltonian(arg0: list[list[float]]) -> PauliOperator:
    """matrix_decompose_hamiltonian(arg0: List[List[float]]) -> pyQPandaOperator.PauliOperator

    Decompose matrix into Hamiltonian.

    Args:
         matrix (EigenMatrixX): 2^N * 2^N double matrix.

    Returns:
         Decomposed Hamiltonian representation.

    """
def trans_Pauli_operator_to_vec(arg0: PauliOperator) -> list[float]:
    """trans_Pauli_operator_to_vec(arg0: pyQPandaOperator.PauliOperator) -> List[float]

    Transform Pauli operator to vector.

    Args:
         operator: Input Pauli operator to be transformed.

    Returns:
         Vector equivalent of the input Pauli operator.

    """
def trans_vec_to_Pauli_operator(arg0: list[float]) -> PauliOperator:
    """trans_vec_to_Pauli_operator(arg0: List[float]) -> pyQPandaOperator.PauliOperator

    Transform vector to Pauli operator.

    Args:
         vector: Input vector to be transformed.

    Returns:
         Pauli operator equivalent of the input vector.

    """
def x(index: int) -> PauliOperator:
    """x(index: int) -> pyQPandaOperator.PauliOperator

    Construct a Pauli X operator.

    Args:
         index (int): Pauli operator index.

    Returns:
         Pauli operator X.

    """
def y(arg0: int) -> PauliOperator:
    """y(arg0: int) -> pyQPandaOperator.PauliOperator

    Construct a Pauli Y operator.

    Args:
         index (int): Pauli operator index.

    Returns:
         Pauli operator Y.

    """
def z(arg0: int) -> PauliOperator:
    """z(arg0: int) -> pyQPandaOperator.PauliOperator

    Construct a Pauli Z operator.

    Args:
         index (int): Pauli operator index.

    Returns:
         Pauli operator Z.

    """
