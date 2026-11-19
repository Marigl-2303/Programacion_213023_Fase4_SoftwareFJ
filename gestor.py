# Importamos anotaciones de tipo para listas internas y retornos opcionales[cite: 2]
from typing import List, Optional
# Importamos las clases del modelo de dominio[cite: 3]
from entidad import Cliente
from servicios import Servicio
from reserva import Reserva
# Importamos las excepciones y utilidades de auditoría en logs[cite: 3, 4]
from excepciones import (
    ErrorSoftwareFJ,
    ReservaInvalidaError,
    registrar_evento,
    registrar_error
)


class GestorSoftwareFJ:
    """
    Controlador principal que administra listas internas de clientes, servicios y reservas
    garantizando continuidad operativa mediante bloques try/except/else/finally[cite: 2, 3].
    """

    def __init__(self):
        # Inicializamos las listas internas en memoria sin bases de datos[cite: 2]
        self._clientes: List[Cliente] = []
        self._servicios: List[Servicio] = []
        self._reservas: List[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> bool:
        """Registra un cliente verificando que no exista duplicidad de ID[cite: 3]."""
        try:
            if any(c.id == cliente.id for c in self._clientes):
                raise ReservaInvalidaError(f"Ya existe un cliente registrado con ID {cliente.id}.")
            self._clientes.append(cliente)
        except ErrorSoftwareFJ as e:
            registrar_error(f"[REGISTRO CLIENTE FALLIDO] {e}")
            print(f"❌ Error al registrar cliente: {e}")
            return False
        else:
            registrar_evento(f"[CLIENTE REGISTRADO] {cliente.obtener_resumen()}")
            print(f"✅ {cliente.obtener_resumen()}")
            return True
        finally:
            registrar_evento("Auditoría: Finalizó operación de registro de cliente.")

    def registrar_servicio(self, servicio: Servicio) -> bool:
        """Registra un servicio verificando que su ID sea único en la lista interna[cite: 2, 3]."""
        try:
            if any(s.id == servicio.id for s in self._servicios):
                raise ReservaInvalidaError(f"Ya existe un servicio registrado con ID {servicio.id}.")
            self._servicios.append(servicio)
        except ErrorSoftwareFJ as e:
            registrar_error(f"[REGISTRO SERVICIO FALLIDO] {e}")
            print(f"❌ Error al registrar servicio: {e}")
            return False
        else:
            registrar_evento(f"[SERVICIO REGISTRADO] {servicio.obtener_resumen()}")
            print(f"✅ {servicio.obtener_resumen()}")
            return True

    def crear_y_confirmar_reserva(
        self,
        id_reserva: str,
        id_cliente: str,
        id_servicio: str,
        duracion_horas: int,
        descuento: float = 0.0,
        aplicar_iva: bool = True
    ) -> Optional[Reserva]:
        """Orquesta la creación, cálculo y confirmación de una reserva con control de excepciones[cite: 3]."""
        reserva = None
        try:
            # Buscamos el cliente en la lista interna
            cliente = next((c for c in self._clientes if c.id == id_cliente), None)
            if not cliente:
                raise ReservaInvalidaError(f"Cliente con ID '{id_cliente}' no encontrado.")

            # Buscamos el servicio en la lista interna
            servicio = next((s for s in self._servicios if s.id == id_servicio), None)
            if not servicio:
                raise ReservaInvalidaError(f"Servicio con ID '{id_servicio}' no encontrado.")

            # Instanciamos y confirmamos la reserva
            reserva = Reserva(id_reserva, cliente, servicio, duracion_horas)
            reserva.procesar_y_confirmar(descuento=descuento, aplicar_iva=aplicar_iva)
            self._reservas.append(reserva)

        except ErrorSoftwareFJ as e:
            # Extraemos la causa raíz si existe encadenamiento de excepciones[cite: 3]
            causa = f" | Causa raíz: {e.__cause__}" if e.__cause__ else ""
            registrar_error(f"[RESERVA FALLIDA - {id_reserva}] {e}{causa}")
            print(f"❌ Error en reserva {id_reserva}: {e}{causa}")
            return None
        else:
            registrar_evento(f"[RESERVA CONFIRMADA] {reserva.obtener_resumen()}")
            print(f"✅ {reserva.obtener_resumen()}")
            return reserva
        finally:
            registrar_evento(f"Auditoría: Cierre de transacción para reserva '{id_reserva}'.")

    def cancelar_reserva(self, id_reserva: str) -> bool:
        """Cancela una reserva activa y registra el evento en el log[cite: 3, 4]."""
        try:
            reserva = next((r for r in self._reservas if r.id == id_reserva), None)
            if not reserva:
                raise ReservaInvalidaError(f"No existe la reserva '{id_reserva}' para cancelar.")
            reserva.cancelar()
        except ErrorSoftwareFJ as e:
            registrar_error(f"[CANCELACIÓN FALLIDA] {e}")
            print(f"❌ Error al cancelar: {e}")
            return False
        else:
            registrar_evento(f"[RESERVA CANCELADA] {reserva.obtener_resumen()}")
            print(f"⚠️ {reserva.obtener_resumen()}")
            return True

    def mostrar_reporte_general(self) -> None:
        """Imprime en consola el resumen de todos los registros almacenados en memoria[cite: 2]."""
        print("\n" + "=" * 75)
        print("REPORTE FINAL EN MEMORIA - SOFTWARE FJ")
        print("=" * 75)
        print(f"Total Clientes registrados : {len(self._clientes)}")
        print(f"Total Servicios creados    : {len(self._servicios)}")
        print(f"Total Reservas procesadas  : {len(self._reservas)}")
        for r in self._reservas:
            print("  ->", r.obtener_resumen())
        print("=" * 75)
