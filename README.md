# Sistema Integral de Gestión de Clientes, Servicios y Reservas – Software FJ

**Curso:** Programación (213023) – Fase 4 (Prácticas Simuladas)  
**Universidad Nacional Abierta y a Distancia – UNAD**  
**Autora:** Mariana Giraldo Londoño  
**Tutor:** Juan Pablo Arango Cardona

## Descripción del Proyecto
Aplicación modular orientada a objetos en Python diseñada para gestionar clientes, servicios especializados (reservas de salas, alquiler de equipos y asesorías) y reservas sin uso de bases de datos. Implementa clases abstractas, herencia, polimorfismo, encapsulación, sobrecarga de parámetros y manejo avanzado de excepciones con trazabilidad en el archivo `sistema_software_fj.log`.

## Estructura del Repositorio
- `excepciones.py`: Jerarquía de excepciones personalizadas y configuración del sistema de logs.
- `entidad.py`: Clase abstracta `EntidadSistema` y clase `Cliente` con encapsulación y validaciones estrictas.
- `servicios.py`: Clase abstracta `Servicio` y subclases polimórficas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`).
- `reserva.py`: Clase `Reserva` con gestión de estados y encadenamiento de excepciones.
- `gestor.py`: Controlador en memoria con bloques `try/except/else/finally`.
- `main.py`: Simulación de 12 operaciones completas (casos exitosos y fallidos).
