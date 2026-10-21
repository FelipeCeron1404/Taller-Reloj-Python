# Reloj Circular

Taller de **Estructuras de Datos**: desarrollo de un reloj con Python aplicando **listas circulares dobles**.

- **Estudiante:** Felipe Alejandro Cerón Cifuentes
- **Docente:** Jhonatan Andrés Mideros Narváez
- **Universidad Cooperativa de Colombia**, cuarto semestre

## Requisitos del taller

| Requisito | Cómo se cumple |
|---|---|
| Solo Python | Un único archivo `main.py`, sin librerías externas ni instalaciones |
| Sin `import` | El código no contiene ninguna instrucción `import` (ver abajo) |
| Frontend | Ventana gráfica con menú lateral, reloj análogo, tarjetas, botones y temas de color |
| Sin HTML ni CSS | Todo se dibuja desde Python |
| Funcionalidad adicional | Seis secciones: reloj, relojes del mundo, alarmas, cronómetro, temporizador y visor de la estructura |

## Cómo ejecutarlo

```bash
python main.py
```

Se necesita Python 3.8 o superior instalado desde python.org. El instalador oficial ya incluye todo lo necesario.

## ¿Cómo se abre una ventana sin `import`?

Al arrancar, Python carga su propio sistema de módulos antes de ejecutar el programa. La clase `RuntimeBridge` usa la variable `__loader__`, que Python entrega a todo script, para llegar a ese sistema que ya está en memoria. Desde ahí obtiene el reloj del sistema (`time`) y la interfaz gráfica que trae Python de fábrica (`tkinter`). El programa no tiene ninguna instrucción `import` y no instala nada.

## La lista circular doble en el proyecto

La clase `CircularDoublyLinkedList` sigue la estructura vista en clase: `Node` con `data`, `prev` y `next`, `insert_at_beginning`, `insert_at_end` y `delete`. Sobre ella, `RingCursor` recorre la lista hacia adelante (`next`) y hacia atrás (`prev`).

| Parte del reloj | Uso de la lista circular doble |
|---|---|
| Mecanismo del reloj | Tres listas: horas (24 nodos), minutos (60) y segundos (60). Cada segundo el cursor pasa al nodo `next`. Cuando la lista de segundos vuelve al `head`, avanza la de minutos, y luego la de horas |
| Temporizador | Cuenta regresiva recorriendo las listas con `prev`. Al pasar de 00 a 59 se "presta" un minuto |
| Relojes del mundo | 12 ciudades en una lista circular. Con anterior y siguiente se navega sin fin |
| Alarmas | Cada alarma es un nodo insertado en orden por hora. Se eliminan con `delete` y se guardan en `alarmas.txt` |
| Cronómetro | Cada vuelta se inserta al final. Se muestran recorriendo hacia atrás, de la más reciente a la más antigua |
| Temas y menú | Los temas de color y las secciones del menú también son listas circulares (Ctrl + ← / → y Ctrl + T) |
| Visor de estructura | Dibuja en vivo los nodos, el `head`, el nodo actual y sus punteros `prev` y `next` |

## Funcionalidades

- Reloj análogo con segundero suave y reloj digital con la fecha en español
- Formato de 12 o 24 horas
- Relojes de 12 ciudades del mundo, con su diferencia horaria
- Alarmas con nombre, activar o desactivar, eliminar, posponer 5 minutos y sonido
- Cronómetro con vueltas, que marca la vuelta más rápida y la más lenta
- Temporizador con atajos (1, 3, 5, 10 minutos, Pomodoro y 1 hora) y anillo de progreso
- Cinco temas de color: Medianoche, Claro, Océano, Atardecer y Bosque
