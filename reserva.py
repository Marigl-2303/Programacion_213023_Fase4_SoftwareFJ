Python
# Importamos las entidades base y clases del dominio[cite: 3]
from entidad import EntidadSistema, Cliente
from servicios import Servicio
# Importamos las excepciones para validación y encadenamiento[cite: 3]
from excepciones import (
    DatoInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    ErrorSoftwareFJ
)


class Reserva(EntidadSistema):
    """Integra Cliente, Servicio, duración y estado con manejo de ciclo de vida[cite: 3]."""

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        # Inicializamos el ID mediante la clase abstracta EntidadSistema[cite: 3]
        super().__init__(id_reserva)
        # Validamos que los objetos recibidos correspondan a las clases esperadas[cite: 3]
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("Se requiere una instancia válida de Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("Se requiere una instancia válida de Servicio.")
        if not isinstance(duracion_horas, int) or duracion_horas <= 0:
            raise DatoInvalidoError("La duración en horas debe ser un entero positivo.")

        # Encapsulamos los atributos de la reserva[cite: 2, 3]
        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "PENDIENTE"
        self._costo_total = 0.0

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def procesar_y_confirmar(self, descuento: float = 0.0, aplicar_iva: bool = True) -> float:
        """Procesa el costo y confirma la reserva aplicando encadenamiento de excepciones[cite: 3]."""
        # Verificamos que la reserva esté en estado PENDIENTE[cite: 3]
        if self._estado != "PENDIENTE":
            raise ReservaInvalidaError(f"No se puede confirmar una reserva en estado '{self._estado}'.")

        # Verificamos disponibilidad actual del servicio[cite: 3]
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self._servicio.nombre}' no está disponible actualmente."
            )

        try:
            # Ejecutamos el cálculo polimórfico del servicio[cite: 2, 3]
            self._costo_total = self._servicio.calcular_costo(
                self._duracion_horas, descuento=descuento, aplicar_iva=aplicar_iva
            )
        except ErrorSoftwareFJ as error_origen:
            # Encadenamiento de excepciones para conservar la causa raíz del fallo[cite: 3]
            raise ReservaInvalidaError(
                f"Fallo al procesar la reserva {self.id} para el servicio {self._servicio.nombre}."
            ) from error_origen

        # Actualizamos estado a CONFIRMADA y bloqueamos la disponibilidad del servicio[cite: 3]
        self._estado = "CONFIRMADA"
        self._servicio.disponible = False
        return self._costo_total

    def cancelar(self) -> None:
        """Cancela la reserva y libera nuevamente el servicio asociado[cite: 3]."""
        if self._estado == "CANCELADA":
            raise ReservaInvalidaError(f"La reserva {self.id} ya se encontraba cancelada.")
        self._estado = "CANCELADA"
        self._servicio.disponible = True

    def obtener_resumen(self) -> str:
        """Retorna la información detallada de la reserva[cite: 3]."""
        return (
            f"Reserva [{self.id}] | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion_horas}h | "
            f"Estado: {self._estado} | Total: ${self._costo_total:,.2f}"
        )
