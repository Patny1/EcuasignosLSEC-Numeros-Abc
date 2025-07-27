# 🇪🇨 ECUASIGNOS – Reconocimiento de Números y Abecedario en Lengua de Señas Ecuatoriana (LSEC)

Este proyecto implementa un sistema de reconocimiento en tiempo real de **números del 1 al 10** y **letras del abecedario** en **Lengua de Señas Ecuatoriana (LSEC)** usando **visión por computadora** y un modelo entrenado con **YOLOv10s** (Ultralytics).

## ✨ Características principales

- 📦 Carga dinámica del modelo YOLO (`.pt`) personalizado y entrenado.
- 🧠 Detección robusta con lógica de **confirmación temporal** para reducir falsos positivos.
- 🎯 Visualización en vivo con **anotaciones sobre la imagen capturada**.
- 🧑‍💻 Interfaz por teclado para **mostrar un saludo** utilizando el nombre detectado por señas.

## 🔧 Requisitos

- Python 3.8 o superior  
- [Ultralytics](https://docs.ultralytics.com/) (instalación con `pip install ultralytics`)
- OpenCV (`pip install opencv-python`)
- Archivo de pesos entrenado: `best.pt`
- Archivo de configuración: `data.yaml` con las clases definidas

## 🚀 Ejecución del proyecto

1. Clona este repositorio:
   ```bash
   git clone https://github.com/Patny1/EcuasignosLSEC-Numeros-Abc.git
   cd EcuasignosLSEC-Numeros-Abc
   ```

2. Instala los requisitos:
   ```bash
   pip install -r requirements.txt
   ```

3. Asegúrate de tener los archivos `best.pt` y `data.yaml` en el directorio del proyecto.

4. Ejecuta el script principal:
   ```bash
   python main.py
   ```

## 📂 Estructura del Proyecto

```
EcuasignosLSEC-Numeros-Abc/

EcuasignosLSEC-Numeros-Abc/
├── src/             # Scripts principales para detección y lógica del sistema
│ └── main.py        # Script principal de ejecución
├── model/           # Pesos del modelo YOLO y configuraciones
│ ├── best.pt        # Pesos del modelo YOLO entrenado
│ └── data.yaml      # Clases del modelo
├── run/             # Carpetas de resultados y pruebas de detección
├── requirements.txt # Lista de dependencias
├── README.md         # Este archivo
└── LICENSE          # Licencia del proyecto (MIT)


```

## 👩‍💻 Autora

**Patricia Constante**  
Proyecto : _ECUASIGNOS_ – Reconocimiento de LSEC con inteligencia artificial y visión artificial.  
Julio 2025  

## 📜 Licencia

Distribuido bajo la Licencia MIT. Consulta el archivo `LICENSE` para más información.

---

> 💡 Este proyecto busca democratizar el acceso a tecnologías inclusivas y visibilizar la Lengua de Señas Ecuatoriana a través de herramientas de código abierto.
