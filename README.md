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

Las clases llevan nombres del caso de estudio, el reloj:

| Concepto visto en clase | Clase o atributo en el reloj |
|---|---|
| Nodo (`Node`) | `DialMark`: una marca de la carátula, con `value` |
| Puntero al nodo anterior y al siguiente | `before` y `after` |
| Lista circular doble | `Dial`: la carátula completa |
| Primer nodo (`head`) | `origin`: la marca de origen, el 00 |
| Insertar al inicio y al final, eliminar | `place_first`, `place_last`, `place_before` y `remove` |
| Recorrer adelante y atrás | `DialHand`: la manecilla, con `advance` y `retreat` |

| Parte del reloj | Uso de la lista circular doble |
|---|---|
| Mecanismo del reloj | Tres diales: horas (24 marcas), minutos (60) y segundos (60). Cada segundo la manecilla avanza a la marca siguiente (`after`). Cuando el dial de segundos vuelve al `origin`, avanza el de minutos, y luego el de horas |
| Temporizador | Cuenta regresiva: las manecillas retroceden con `before`. Al pasar de 00 a 59 se "presta" un minuto |
| Relojes del mundo | 12 ciudades en una lista circular. Con anterior y siguiente se navega sin fin |
| Alarmas | Cada alarma es un nodo insertado en orden por hora. Se eliminan con `remove` y se guardan en `alarmas.txt` |
| Cronómetro | Cada vuelta se inserta al final. Se muestran recorriendo hacia atrás, de la más reciente a la más antigua |
| Temas y menú | Los temas de color y las secciones del menú también son listas circulares (Ctrl + ← / → y Ctrl + T) |
| Visor de estructura | Dibuja en vivo las marcas del dial, el `origin`, la marca actual y sus enlaces `before` y `after` |

## Funcionalidades

- Reloj análogo con segundero suave y reloj digital con la fecha en español
- Formato de 12 o 24 horas
- Relojes de 12 ciudades del mundo, con su diferencia horaria
- Alarmas con nombre, activar o desactivar, eliminar, posponer 5 minutos y sonido
- Cronómetro con vueltas, que marca la vuelta más rápida y la más lenta
- Temporizador con atajos (1, 3, 5, 10 minutos, Pomodoro y 1 hora) y anillo de progreso
- Cinco temas de color: Medianoche, Claro, Océano, Atardecer y Bosque
