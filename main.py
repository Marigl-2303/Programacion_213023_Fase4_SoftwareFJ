# Importamos las clases del sistema para ejecutar la simulación integral[cite: 4]
from entidad import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ
from excepciones import ErrorSoftwareFJ, registrar_error, registrar_evento


def ejecutar_simulacion() -> None:
    """Simula 12 operaciones completas (exitosas y fallidas) sin interrumpir el sistema[cite: 4]."""
    sistema = GestorSoftwareFJ()
    registrar_evento("=== INICIO DE SIMULACIÓN SOFTWARE FJ ===")
    print("=== INICIANDO SIMULACIÓN DE OPERACIONES SOFTWARE FJ ===\n")

    # Operación 1: Registro válido de Cliente 1
    try:
        c1 = Cliente("CLI-01", "Mariana Giraldo", "mariana@softwarefj.com", "3104567890")
        sistema.registrar_cliente(c1)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN CLIENTE] {e}")

    # Operación 2: Registro válido de Cliente 2
    try:
        c2 = Cliente("CLI-02", "Carlos Mendoza", "carlos.m@empresa.co", "3009876543")
        sistema.registrar_cliente(c2)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN CLIENTE] {e}")

    # Operación 3: Registro INVÁLIDO de Cliente (correo sin arroba y teléfono corto)
    try:
        c_malo = Cliente("CLI-03", "Ana", "correo_sin_arroba", "123")
        sistema.registrar_cliente(c_malo)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN CLIENTE FALLIDA] {e}")
        print(f"❌ Captura controlada al crear cliente inválido: {e}")

    # Operación 4: Registro válido de Servicio 1 (Sala)
    try:
        s1 = ReservaSala("SRV-01", "Sala Innovación Cloud", 80000, capacidad=15)
        sistema.registrar_servicio(s1)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN SERVICIO] {e}")

    # Operación 5: Registro válido de Servicio 2 (Alquiler de Equipo)
    try:
        s2 = AlquilerEquipo("SRV-02", "Servidor Dell PowerEdge", 50000, gama="servidor")
        sistema.registrar_servicio(s2)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN SERVICIO] {e}")

    # Operación 6: Registro válido de Servicio 3 (Asesoría Especializada)
    try:
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura de Software", 120000, "Sistemas Distribuidos")
        sistema.registrar_servicio(s3)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN SERVICIO] {e}")

    # Operación 7: Creación INVÁLIDA de Servicio (tarifa negativa)
    try:
        s_malo = ReservaSala("SRV-04", "Sala Fantasma", -25000, capacidad=5)
        sistema.registrar_servicio(s_malo)
    except ErrorSoftwareFJ as e:
        registrar_error(f"[INSTANCIACIÓN SERVICIO FALLIDA] {e}")
        print(f"❌ Captura controlada al crear servicio inválido: {e}")

    # Operación 8: Reserva EXITOSA 1 (Sala por 5 horas, recargo +10%, descuento 10% + IVA)
    sistema.crear_y_confirmar_reserva("RES-01", "CLI-01", "SRV-01", duracion_horas=5, descuento=0.10, aplicar_iva=True)

    # Operación 9: Reserva FALLIDA 2 (Intento de reservar la misma Sala SRV-01 ya ocupada)
    sistema.crear_y_confirmar_reserva("RES-02", "CLI-02", "SRV-01", duracion_horas=2)

    # Operación 10: Reserva FALLIDA 3 (Equipo por 1 hora, incumple mínimo de 2 horas -> encadenamiento)
    sistema.crear_y_confirmar_reserva("RES-03", "CLI-02", "SRV-02", duracion_horas=1)

    # Operación 11: Reserva EXITOSA 4 (Asesoría especializada por 3 horas sin IVA)
    sistema.crear_y_confirmar_reserva("RES-04", "CLI-02", "SRV-03", duracion_horas=3, descuento=0.05, aplicar_iva=False)

    # Operación 12: Cancelación de reserva RES-01 y nueva reserva exitosa sobre SRV-01 liberada
    sistema.cancelar_reserva("RES-01")
    sistema.crear_y_confirmar_reserva("RES-05", "CLI-02", "SRV-01", duracion_horas=3)

    # Mostramos el reporte final en consola
    sistema.mostrar_reporte_general()
    registrar_evento("=== FIN DE SIMULACIÓN SOFTWARE FJ ===")


# Punto de entrada principal del programa
if __name__ == "__main__":
    ejecutar_simulacion()

