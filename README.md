# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

Proyecto correspondiente a la **Fase 4 – Componente Práctico (Prácticas Simuladas)** del curso **Programación (213023)** de la Universidad Nacional Abierta y a Distancia (UNAD)[cite: 5].

* **Programa:** Ingeniería de Sistemas – ECBTI[cite: 2]
* **Curso y Grupo:** Programación (`213023_343`)[cite: 5]
* **Estudiante:** Mariana Giraldo Londoño
* **Tutor:** Juan Pablo Arango Cardona

---

## Descripción General

Aplicación modular desarrollada en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** para gestionar clientes, catálogo de servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas de la empresa **Software FJ**[cite: 2].

El sistema opera completamente en memoria mediante objetos y listas internas (sin motores de bases de datos) y utiliza un sistema centralizado de auditoría (`sistema_software_fj.log`) para registrar eventos y excepciones controladas, garantizando la continuidad operativa ante cualquier fallo de ejecución[cite: 2, 3, 4].

---

## Arquitectura Modular del Repositorio

| Archivo | Módulo / Responsabilidad |
| :--- | :--- |
| `excepciones.py` | Configura el sistema de registro (`logging`) en `sistema_software_fj.log` y define la jerarquía de excepciones personalizadas[cite: 2, 3, 4]. |
| `entidad.py` | Implementa la clase abstracta base `EntidadSistema` y la clase concreta `Cliente` con encapsulación mediante propiedades (`@property`) y validaciones estrictas[cite: 3]. |
| `servicios.py` | Define la clase abstracta `Servicio` y sus tres especializaciones polimórficas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`)[cite: 3]. |
| `reserva.py` | Implementa la clase `Reserva`, integrando cliente, servicio, duración y ciclo de vida (`PENDIENTE`, `CONFIRMADA`, `CANCELADA`) con encadenamiento de errores[cite: 3]. |
| `gestor.py` | Contiene la clase orquestadora `GestorSoftwareFJ`, encargada de administrar las listas internas y asegurar la estabilidad mediante bloques `try/except/else/finally`[cite: 2, 3]. |
| `main.py` | Script principal que ejecuta la batería de 12 operaciones simuladas (casos válidos y errores controlados) y genera el reporte final en consola. |

---

## Diseño Orientado a Objetos

### Jerarquía de Clases

| Clase | Tipo | Función en el Sistema |
| :--- | :--- | :--- |
| `EntidadSistema` | Abstracta (`ABC`) | Define el identificador encapsulado (`_id`) y obliga a implementar `obtener_resumen()`[cite: 2, 3]. |
| `Cliente` | Concreta | Valida nombre (mín. 3 caracteres), formato de correo electrónico (expresión regular) y teléfono numérico (mín. 7 dígitos)[cite: 3]. |
| `Servicio` | Abstracta (`ABC`) | Establece el contrato común de validación (`validar_parametros`) y cálculo sobrecargado (`calcular_costo`)[cite: 3]. |
| `ReservaSala` | Concreta | Reserva por horas (1 a 12 h); aplica un recargo operativo del 10 % cuando supera las 4 horas[cite: 2, 3]. |
| `AlquilerEquipo` | Concreta | Alquiler mínimo de 2 horas; incluye un seguro fijo obligatorio de $15.000 por operación[cite: 2, 3]. |
| `AsesoriaEspecializada` | Concreta | Consultoría técnica por horas (1 a 8 h) con tarifa lineal según área de especialidad[cite: 2, 3]. |
| `Reserva` | Concreta | Gestiona confirmación, bloqueo automático de disponibilidad del servicio y cancelación con liberación de recurso[cite: 3]. |
| `GestorSoftwareFJ` | Controlador | Administra colecciones en memoria (`_clientes`, `_servicios`, `_reservas`) y audita cada transacción[cite: 2]. |

### Pilares de POO Aplicados
* **Abstracción:** Uso del módulo estándar `abc` (`ABC` y `@abstractmethod`) en `EntidadSistema` y `Servicio`[cite: 2, 3].
* **Encapsulación:** Protección de atributos internos con guion bajo (`_id`, `_nombre`, `_tarifa_base`, `_estado`) y acceso controlado mediante decoradores `@property` y `@setter`[cite: 2, 3].
* **Herencia y Polimorfismo:** Sobrescritura de `calcular_costo()`, `validar_parametros()` y `obtener_resumen()` en cada subclase de servicio[cite: 2, 3].
* **Sobrecarga de Métodos:** El método `calcular_costo(duracion_horas, descuento=0.0, aplicar_iva=True)` soporta múltiples combinaciones de cálculo (tarifa base, con descuento porcentual y con o sin IVA del 19 %)[cite: 3].

---

## Manejo Avanzado de Excepciones

Todas las excepciones de negocio heredan de `ErrorSoftwareFJ`[cite: 3]:

| Excepción Personalizada | Condición de Activación |
| :--- | :--- |
| `ParametroFaltanteError` | Ausencia de identificador obligatorio al instanciar entidades[cite: 3]. |
| `DatoInvalidoError` | Formatos incorrectos (correo/teléfono), tarifas negativas o duraciones fuera de rango[cite: 3]. |
| `ServicioNoDisponibleError` | Intento de confirmar una reserva sobre un servicio previamente ocupado[cite: 3]. |
| `ReservaInvalidaError` | Consultas de clientes/servicios inexistentes, duplicidad de IDs o estados de reserva incompatibles[cite: 3]. |
| `CalculoInconsistenteError` | Porcentajes de descuento fuera del rango permitido (0 % – 50 %) o totales no positivos[cite: 3]. |

**Estructuras de control implementadas:**
* **`try / except`:** Captura de errores de instanciación en `main.py` sin detener el flujo principal[cite: 3, 4].
* **`try / except / else / finally`:** Control integral en `GestorSoftwareFJ.registrar_cliente()` y `crear_y_confirmar_reserva()` para registrar éxito en `else` y auditoría de cierre en `finally`[cite: 3].
* **Encadenamiento de excepciones (`raise ... from ...`):** Implementado en `Reserva.procesar_y_confirmar()` para envolver fallos de validación de servicio dentro de `ReservaInvalidaError` conservando la causa raíz (`__cause__`)[cite: 3].

---

## Escenarios de Simulación (`main.py`)

El script principal ejecuta **12 operaciones completas** verificando la resiliencia del sistema[cite: 4]:

| # | Operación Simulada | Resultado Esperado |
| :-: | :--- | :--- |
| 1 | Registro válido de cliente (`CLI-01` – Mariana Giraldo) | Operación exitosa |
| 2 | Registro válido de cliente (`CLI-02` – Carlos Mendoza) | Operación exitosa |
| 3 | Registro inválido de cliente (correo sin `@` y teléfono corto) | Error controlado (`DatoInvalidoError`) |
| 4 | Creación válida de servicio `ReservaSala` (`SRV-01`) | Operación exitosa |
| 5 | Creación válida de servicio `AlquilerEquipo` (`SRV-02`) | Operación exitosa |
| 6 | Creación válida de servicio `AsesoriaEspecializada` (`SRV-03`) | Operación exitosa |
| 7 | Creación inválida de servicio con tarifa negativa (`-$25.000`) | Error controlado (`DatoInvalidoError`) |
| 8 | Reserva exitosa `RES-01` (Sala 5h, recargo +10 %, desc. 10 % + IVA) | Confirmada y servicio bloqueado |
| 9 | Reserva fallida `RES-02` sobre sala `SRV-01` ya ocupada | Error controlado (`ServicioNoDisponibleError`) |
| 10 | Reserva fallida `RES-03` de equipo por 1h (mínimo 2h) | Error encadenado (`ReservaInvalidaError`) |
| 11 | Reserva exitosa `RES-04` de asesoría (3h, desc. 5 %, sin IVA) | Confirmada correctamente |
| 12 | Cancelación de `RES-01` y nueva reserva `RES-05` sobre `SRV-01` | Liberación y reasignación exitosa |

---

## Instrucciones de Ejecución

**Requisitos:** Python 3.10 o superior (utiliza únicamente la biblioteca estándar de Python: `abc`, `re`, `logging`, `typing`).

1. Clonar el repositorio:
   ```bash
   git clone [https://github.com/Marigl-2303/Programacion_213023_Fase4_SoftwareFJ.git](https://github.com/Marigl-2303/Programacion_213023_Fase4_SoftwareFJ.git)
   cd Programacion_213023_Fase4_SoftwareFJ
