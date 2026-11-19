# Importamos abstractmethod para declarar métodos polimórficos obligatorios[cite: 2, 3]
from abc import abstractmethod
# Importamos la clase base abstracta EntidadSistema[cite: 3]
from entidad import EntidadSistema
# Importamos las excepciones de validación y cálculo[cite: 3]
from excepciones import DatoInvalidoError, CalculoInconsistenteError


class Servicio(EntidadSistema):
    """Clase abstracta para los servicios ofrecidos por Software FJ[cite: 2, 3]."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Validamos y asignamos el ID desde la clase padre[cite: 2]
        super().__init__(id_servicio)
        # Validamos que el nombre del servicio no esté vacío[cite: 3]
        if not nombre or not str(nombre).strip():
            raise DatoInvalidoError("El nombre del servicio no puede estar vacío.")
        # Validamos que la tarifa base sea estrictamente positiva[cite: 3]
        if tarifa_base <= 0:
            raise DatoInvalidoError(f"La tarifa base debe ser mayor a 0 (recibido: {tarifa_base}).")

        # Encapsulamos los atributos del servicio[cite: 2]
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        self._disponible = bool(estado)

    @abstractmethod
    def validar_parametros(self, duracion_horas: int) -> None:
        """Valida las reglas específicas de duración de cada tipo de servicio[cite: 3]."""
        pass

    @abstractmethod
    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Método polimórfico y sobrecargado con parámetros opcionales (descuento e IVA)[cite: 3]."""
        pass

    def _aplicar_ajustes(self, subtotal: float, descuento: float, aplicar_iva: bool) -> float:
        """Aplica descuentos e impuestos validando la consistencia financiera[cite: 3]."""
        # Verificamos que el porcentaje de descuento esté entre 0% y 50%[cite: 3]
        if descuento < 0 or descuento > 0.5:
            raise CalculoInconsistenteError(f"Descuento fuera de rango permitido (0% - 50%): {descuento * 100}%.")
        # Aplicamos el descuento al subtotal
        total = subtotal * (1 - descuento)
        # Si aplicar_iva es True, sumamos el 19% de IVA
        if aplicar_iva:
            total *= 1.19
        # Comprobamos que el monto resultante sea positivo[cite: 3]
        if total <= 0:
            raise CalculoInconsistenteError("El costo final calculado debe ser mayor a cero.")
        # Retornamos el valor redondeado a 2 decimales
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio especializado 1: Reserva de salas tecnológicas[cite: 2, 3]."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        # Validamos que la capacidad de la sala sea positiva[cite: 3]
        if capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser mayor a 0 personas.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion_horas: int) -> None:
        """Las salas solo pueden reservarse entre 1 y 12 horas[cite: 3]."""
        if duracion_horas < 1 or duracion_horas > 12:
            raise DatoInvalidoError("Las salas solo se reservan entre 1 y 12 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo aplicando recargo del 10% si la reserva supera las 4 horas[cite: 3]."""
        self.validar_parametros(duracion_horas)
        subtotal = self.tarifa_base * duracion_horas
        if duracion_horas > 4:
            subtotal *= 1.10
        return self._aplicar_ajustes(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Sala [{self.id}] {self.nombre} (Cap: {self._capacidad} pers.) - ${self.tarifa_base:,.0f}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado 2: Alquiler de equipos de cómputo y servidores[cite: 2, 3]."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, gama: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        # Validamos que la gama pertenezca a las categorías permitidas[cite: 3]
        if str(gama).lower() not in ("estandar", "alta", "servidor"):
            raise DatoInvalidoError(f"Gama de equipo desconocida: '{gama}'.")
        self._gama = gama.capitalize()

    def validar_parametros(self, duracion_horas: int) -> None:
        """El alquiler de equipos requiere un mínimo de 2 horas[cite: 3]."""
        if duracion_horas < 2:
            raise DatoInvalidoError("El alquiler mínimo de equipos es de 2 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo sumando un seguro fijo de $15.000 por equipo[cite: 3]."""
        self.validar_parametros(duracion_horas)
        subtotal = (self.tarifa_base * duracion_horas) + 15000
        return self._aplicar_ajustes(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Equipo [{self.id}] {self.nombre} (Gama {self._gama}) - ${self.tarifa_base:,.0f}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado 3: Consultoría y asesoría en ingeniería[cite: 2, 3]."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_base, disponible)
        if not especialidad or not str(especialidad).strip():
            raise DatoInvalidoError("Debe indicar el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion_horas: int) -> None:
        """Las asesorías deben durar entre 1 y 8 horas[cite: 3]."""
        if duracion_horas <= 0 or duracion_horas > 8:
            raise DatoInvalidoError("Las asesorías especializadas deben durar entre 1 y 8 horas.")

    def calcular_costo(self, duracion_horas: int, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Calcula el costo lineal por hora de consultoría[cite: 3]."""
        self.validar_parametros(duracion_horas)
        subtotal = self.tarifa_base * duracion_horas
        return self._aplicar_ajustes(subtotal, descuento, aplicar_iva)

    def obtener_resumen(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Asesoría [{self.id}] {self.nombre} ({self._especialidad}) - ${self.tarifa_base:,.0f}/h [{estado}]"
