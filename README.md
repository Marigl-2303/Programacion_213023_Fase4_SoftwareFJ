# Software FJ — Plataforma Modular de Gestión de Clientes, Servicios y Reservas

**Universidad Nacional Abierta y a Distancia (UNAD)** · Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)  
**Curso:** Programación (`213023`) — Fase 4: Prácticas Simuladas · **Grupo:** `213023_343`  
**Autora:** Mariana Giraldo Londoño · **Tutor:** Juan Pablo Arango Cardona

---

## 1. Propósito y Alcance Técnico

Este repositorio implementa una solución de software en **Python** orientada a objetos para administrar el ciclo operativo de **Software FJ** (registro de clientes, catálogo de servicios tecnológicos y control de reservas) operando íntegramente en memoria mediante colecciones dinámicas (`list`), sin dependencias de bases de datos externas.

La arquitectura prioriza la **tolerancia a fallos y la trazabilidad**: cualquier anomalía en los datos de entrada, disponibilidad de recursos o reglas financieras es interceptada mediante excepciones de dominio y registrada en el archivo `sistema_software_fj.log`, permitiendo que el flujo de ejecución continúe sin interrupciones.

---

## 2. Organización de Módulos

El proyecto adopta una separación estricta de responsabilidades en seis archivos independientes:

```text
Programacion_213023_Fase4_SoftwareFJ/
├── excepciones.py   # Jerarquía de errores de negocio y configuración del logger
├── entidad.py       # Clase base abstracta EntidadSistema y modelo Cliente
├── servicios.py     # Contrato abstracto Servicio y 3 especializaciones polimórficas
├── reserva.py       # Ciclo de vida de reservas, estados y encadenamiento de errores
├── gestor.py        # Orquestador en memoria (GestorSoftwareFJ) con try/except/else/finally
├── main.py          # Batería de 12 pruebas de integración y reporte final en consola
└── README.md        # Documentación técnica del repositorio
