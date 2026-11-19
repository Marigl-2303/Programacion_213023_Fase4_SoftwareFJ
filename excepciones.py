# Importamos el módulo logging para gestionar el registro de eventos y errores en archivo[cite: 2, 4]
import logging

# Configuramos el archivo de logs con nivel INFO, formato de fecha/hora y codificación UTF-8[cite: 2, 4]
logging.basicConfig(
    filename="sistema_software_fj.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)


def registrar_evento(mensaje: str) -> None:
    """Registra una operación exitosa o evento informativo en el archivo de logs[cite: 2, 4]."""
    # Escribe el mensaje de información en sistema_software_fj.log
    logging.info(mensaje)


def registrar_error(mensaje: str) -> None:
    """Registra una excepción o fallo controlado en el archivo de logs[cite: 2, 3, 4]."""
    # Escribe el mensaje de error en sistema_software_fj.log
    logging.error(mensaje)


class ErrorSoftwareFJ(Exception):
    """Excepción base personalizada para todos los errores de negocio del sistema Software FJ[cite: 2, 3]."""
    pass


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un parámetro tiene un formato, tipo o rango de valor inválido[cite: 3]."""
    pass


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un dato obligatorio para instanciar o procesar una entidad[cite: 3]."""
    pass


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio solicitado se encuentra ocupado o inactivo[cite: 3]."""
    pass


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza ante intentos de reserva incorrectos o transiciones de estado no permitidas[cite: 3]."""
    pass


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando el cálculo de tarifas, impuestos o descuentos arroja valores incoherentes[cite: 3]."""
    pass
  
