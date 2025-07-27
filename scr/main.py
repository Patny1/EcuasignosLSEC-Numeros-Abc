"""
Lengua de Señas Ecuatoriana – Reconocimiento de Números del 1 al 10 y las letras del abecedario
====================================================================

Este script utiliza un modelo YOLOv10s entrenado con Ultralytics para detectar
y reconocer números del 1 al 10 y el abecedario en Lengua de Señas Ecuatoriana (LSEC) en tiempo real
a través de la cámara web. El modelo ha sido personalizado y entrenado con datos
propios anotados en formato YOLO.

Características principales:
----------------------------
- Carga dinámica del modelo YOLO (.pt) entrenado.
- Lógica de confirmación temporal para evitar falsos positivos.
- Visualización de detecciones con anotaciones en vivo.
- Interfaz básica por teclado para mostrar un saludo con el nombre detectado.

Requisitos:
-----------
- Python 3.8+
- OpenCV (`cv2`)
- Ultralytics (`pip install ultralytics`)
- Archivo de pesos `best.pt` entrenado previamente.
- Archivo `data.yaml` con las clases definidas.

Autor: Patricia Constante
Proyecto: ECUASIGNOS Reconocimiento de LSEC con YOLO y Visión Artificial
Versión: 1.0
Fecha: Julio 2025
Licencia: MIT

Repositorio GitHub: https://github.com/Patny1/EcuasignosLSEC-Numeros-Abc

"""

import cv2
import time
import threading
import tkinter as tk
from ultralytics import YOLO

# Configuración
model = YOLO('model/best.pt')


CONFIDENCE_THRESHOLD = 0.60
TIME_THRESHOLD = 0.6

# Variables globales compartidas
current_word = ""
last_detected_letter = None
detection_start_time = None
frame = None
running = True

saludo_mostrar = ""
saludo_start_time = None
SALUDO_DURACION = 3

lock = threading.Lock()

def camera_loop():
    global current_word, last_detected_letter, detection_start_time, frame, running
    global saludo_mostrar, saludo_start_time

    cap = cv2.VideoCapture(0)#camara
    if not cap.isOpened():
        print("Error: no se pudo abrir la cámara.")
        running = False
        return

    while running:
        ret, f = cap.read()
        if not ret:
            print("Error al leer frame.")
            break

        results = model.predict(f, device='cpu', verbose=False)
        annotated_frame = results[0].plot().copy()

        detected_letter = None
        highest_confidence = 0

        for box in results[0].boxes:
            conf = float(box.conf[0])
            if conf > highest_confidence and conf > CONFIDENCE_THRESHOLD:
                highest_confidence = conf
                cls_id = int(box.cls[0])
                detected_letter = model.names[cls_id]

        with lock:
            if detected_letter:
                if detected_letter == last_detected_letter:
                    if detection_start_time is not None:
                        elapsed = time.time() - detection_start_time
                        if elapsed >= TIME_THRESHOLD:
                            if not current_word.endswith(detected_letter):
                                current_word += detected_letter
                                print(f"Letra '{detected_letter}' agregada. Palabra actual: {current_word}")
                else:
                    last_detected_letter = detected_letter
                    detection_start_time = time.time()
            else:
                last_detected_letter = None
                detection_start_time = None

            # Mostrar palabra o saludo
            if saludo_mostrar:
                elapsed_saludo = time.time() - saludo_start_time
                if elapsed_saludo < SALUDO_DURACION:
                    texto_mostrar = saludo_mostrar
                    color_texto = (255, 0, 0)
                else:
                    saludo_mostrar = ""
                    texto_mostrar = f"Nombre: {current_word}"
                    color_texto = (0, 255, 0)
            else:
                texto_mostrar = f"Nombre: {current_word}"
                color_texto = (0, 255, 0)

        cv2.putText(annotated_frame,
                    texto_mostrar,
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color_texto,
                    2)

        frame = annotated_frame.copy()
        cv2.imshow("Deteccion LSEC - Nombres", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            running = False
            break

    cap.release()
    cv2.destroyAllWindows()
    running = False

def saludar():
    global saludo_mostrar, saludo_start_time, current_word, last_detected_letter, detection_start_time
    with lock:
        if current_word:
            saludo_mostrar = f"HOLA, {current_word}!"
            saludo_start_time = time.time()
            print(saludo_mostrar)
            current_word = ""
            last_detected_letter = None
            detection_start_time = None

def limpiar_palabra():
    global current_word, last_detected_letter, detection_start_time
    with lock:
        current_word = ""
        last_detected_letter = None
        detection_start_time = None
    label_palabra.config(text="Palabra actual: ")

def borrar_ultimo():
    global current_word
    with lock:
        if len(current_word) > 0:
            current_word = current_word[:-1]
    label_palabra.config(text=f"Palabra actual: {current_word}")

import tkinter as tk

root = tk.Tk()
root.title("LSEC Control - Mini GUI")

label_palabra = tk.Label(root, text="Palabra actual: ", font=("Arial", 16))
label_palabra.pack(pady=10)

btn_saludo = tk.Button(root, text="Saludar", width=15, command=saludar)
btn_saludo.pack(pady=5)

btn_reset = tk.Button(root, text="Reset", width=15, command=limpiar_palabra)
btn_reset.pack(pady=5)

btn_delete = tk.Button(root, text="Delete", width=15, command=borrar_ultimo)
btn_delete.pack(pady=5)

def actualizar_label():
    with lock:
        label_palabra.config(text=f"Palabra actual: {current_word}")
    if running:
        root.after(200, actualizar_label)

thread_cam = threading.Thread(target=camera_loop, daemon=True)
thread_cam.start()

actualizar_label()

root.mainloop()

running = False
thread_cam.join()
