# Importamos ABC y abstractmethod para construir clases abstractas[cite: 3]
from abc import ABC, abstractmethod
# Importamos re para validar expresiones regulares en el correo electrónico
import re
# Importamos las excepciones personalizadas necesarias para validar atributos[cite: 3]
from excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadSistema(ABC):
    """Clase abstracta base que representa cualquier entidad general del sistema Software FJ[cite: 2, 3]."""

    def __init__(self, id_entidad: str):
        # Verificamos que el ID exista y no esté compuesto solo por espacios en blanco[cite: 3]
        if not id_entidad or not str(id_entidad).strip():
            # Lanzamos excepción si el parámetro obligatorio está ausente[cite: 3]
            raise ParametroFaltanteError("El ID de la entidad es obligatorio.")
        # Encapsulamos el identificador como atributo protegido
        self._id = str(id_entidad).strip()

    @property
    def id(self) -> str:
        """Propiedad de solo lectura para acceder al ID encapsulado[cite: 2]."""
        return self._id

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las clases hijas a implementar su descripción[cite: 2, 3]."""
        pass


class Cliente(EntidadSistema):
    """Clase derivada que modela un cliente con encapsulación y validaciones estrictas[cite: 2, 3]."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Inicializamos el identificador mediante el constructor de la superclase[cite: 2]
        super().__init__(id_cliente)
        # Asignamos los atributos pasando por sus respectivos setters validados[cite: 3]
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        """Getter encapsulado del nombre del cliente[cite: 2, 3]."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter que valida que el nombre tenga al menos 3 caracteres válidos[cite: 3]."""
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. Debe tener mínimo 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        """Getter encapsulado del correo electrónico[cite: 2, 3]."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Setter que verifica la estructura válida de correo electrónico[cite: 3]."""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not valor or not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Getter encapsulado del número telefónico[cite: 2, 3]."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Setter que exige que el teléfono sea numérico y de mínimo 7 dígitos[cite: 3]."""
        limpio = str(valor).strip() if valor is not None else ""
        if not limpio.isdigit() or len(limpio) < 7:
            raise DatoInvalidoError(f"Teléfono inválido: '{valor}'. Debe contener solo dígitos (mínimo 7).")
        self._telefono = limpio

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen descriptivo del cliente[cite: 2, 3]."""
        return f"Cliente [{self.id}] {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"
