---

marp: true
lang: es
title: "Diseño e implementación de un sistema de adquisición, transmisión y visualización de datos basado en CanSat"
description: "TFM – Sergio García Sánchez"
paginate: true
size: 16:9
theme: default
class: lead
style: |
  :root { --accent: #2563eb; }
  section.lead h1, section.lead h2 { color: var(--accent); }
  section { font-size: 30px; }
  footer { color: #666; font-size: 18px; }
  .title-wrap {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
    padding-top: 12px;
  }
  .title-wrap h1 {
    font-size: 60px;
    line-height: 1.12;
    margin: 0 0 18px 0;
    color: var(--accent);
  }
  .title-wrap .meta {
    font-size: 30px;
    line-height: 1.35;
    color: #111;
    margin: 0 0 14px 0;
  }
  .title-wrap .director {
    font-size: 26px;
    color: #333;
    margin: 0;
  }
  .title-wrap .accent {
    width: 88px;
    height: 6px;
    background: var(--accent);
    border-radius: 3px;
    margin: 20px auto 16px;
  }
  .ucm-center {
    display: block;
    margin: 18px auto 0;
    height: 92px;
    object-fit: contain;
    opacity: 0.95;
  }
header: ""
---

<!-- _class: lead -->
<div class="title-wrap">
  <h1>Diseño e implementación de un sistema de adquisición, transmisión y visualización de datos basado en CanSat</h1>
  <p class="meta"><strong>Sergio García Sánchez</strong> — Máster en Ingeniería Informática (UCM)</p>
  <p class="director"><strong>Director:</strong> Adrián Riesco Rodríguez</p>
  <div class="accent"></div>
</div>

<img src="./figuras/ucm.jpg" class="ucm-center" alt="UCM">



---

## Índice

1. **Introduction** 

2. **Objectives** 

3. **Fundamentos y estado del arte**  

4. **Diseño y arquitectura**  

5. **Validación y resultados**  

6. **Conclusions**  

7. **Future work**

8. **Q&A**  

---

## 1. Introduction


This project presents the **design and implementation** of a complete system for:

- Building a **CanSat-like device** with sensors, GPS and camera  
- Sending data in real time via **WiFi** or **radio**  
- Displaying telemetry, position, attitude, and video in a **reusable web interface**


---

<style>
.row { display: flex; gap: 24px; align-items: flex-start; }
.row .text { flex: 1; }
.row img { width: 38%; max-width: 420px; }
</style>


### What is a CanSat?

<div class="row">
  <div class="text">
    <ul>
      <li>Miniature satellite with the approximate size of a soda can (66 mm diameter × 115 mm height)</li>
      <li>Equipped with sensors, onboard computer, power supply, radio system, and parachute</li>
      <li>Launched from rockets or drones to simulate a space mission, typically from 500 – 1000 m altitude</li>
      <li>Widely used for educational purposes and in competitions (ESA CanSat, NASA CanSat)</li>
    </ul>
  </div>
  <img src="./figuras/cansat_size.png" alt="CanSat" style="max-height: 300px;">
</div>

---

### Motivation

- Existing CanSat projects focus mainly on hardware and electronics  
- Data visualization is often ad-hoc, not reusable  
- Lack of an easy-to-deploy **modular web platform** for telemetry and video  
---
## 2. Objectives – CanSat

- Build a **CanSat (66 × 115 mm, 300–350 g)** with:
  - GPS receiver  
  - Camera for live video  
  - Barometric sensor for pressure/altitude  
  - IMU for attitude  
  - Battery with solar charging option  

- Send data in real time:
  - **WiFi** when available  
  - **LoRa radio** as fallback (with ground station)


---
## 2. Objectives – Web Platform

- Provide a **modular, reusable platform** for:
  - Live telemetry and last values  
  - Real-time charts of sensor data  
  - GNSS position on a map  
  - 3D attitude model  
  - Live video streaming  
  - Data export for analysis
---

<style>
.grid{
  display:flex;
  flex-wrap:wrap;
  gap:24px;
  align-items:stretch;
}
.grid > .tool{
  flex:1 1 calc(50% - 24px);
  min-width:380px;
  display:flex;
  flex-direction:column;
}
.tool .head{ margin:0 0 12px 0; line-height:1.35; }
.tool .fig{
  flex:1;
  display:flex;
  align-items:center;
  justify-content:center;
  padding:4px 0;
}
.tool .fig img{
  max-width:100%;
  max-height:240px;
  object-fit:contain;
  display:block;
}
</style>

## 3. Fundamentos - Herramientas de visualización

<div class="grid">
  <div class="tool">
    <p class="head"><strong>SerialPlot:</strong> visor de puerto serie para ver y graficar datos en tiempo real desde Arduino IDE.</p>
    <img src="./figuras/serialplot.png" alt="SerialPlot">
  </div>

  <div class="tool">
    <p class="head"><strong>Matplotlib / PyQtGraph:</strong> librerías de Python para generar gráficos.</p>
    <img src="./figuras/matplotlib.png" alt="Matplotlib o PyQtGraph">
  </div>
</div>

---

<div class="grid">
  <div class="tool">
    <p class="head"><strong>Excel / Google Sheets:</strong> hojas de cálculo para calcular y graficar datos, no soporta streaming.</p>
    <img src="./figuras/excel.jpg" alt="Excel o Google Sheets">
  </div>

  <div class="tool">
    <p class="head"><strong>LabVIEW:</strong> entorno gráfico de National Instruments para adquisición de datos y control.</p>
    <img src="./figuras/labview.png" alt="LabVIEW">
  </div>
</div>

---

<style>
.table-compact{width:100%;border-collapse:collapse;font-size:22px;}
.table-compact th,.table-compact td{border:1px solid #ddd;padding:6px 8px;vertical-align:top;}
.table-compact th{background:#f7f7f7;text-align:left;}
.table-compact td{word-break:break-word;}
.table-compact td:nth-child(1){white-space:nowrap;}
</style>

## 3. Fundamentos - Microcontroladores

<table class="table-compact">
  <thead>
    <tr>
      <th>Característica</th>
      <th>Raspberry Pi Zero 2 W</th>
      <th>ESP32</th>
      <th>Arduino Nano</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Procesador</strong></td>
      <td>ARM Cortex-A53 (4×, 1&nbsp;GHz)</td>
      <td>Xtensa LX6 (2×, 240&nbsp;MHz)</td>
      <td>ATmega328P (1×, 16&nbsp;MHz)</td>
    </tr>
    <tr>
      <td><strong>Memoria</strong></td>
      <td>512&nbsp;MB SDRAM</td>
      <td>520&nbsp;KB SRAM + 4&nbsp;MB Flash</td>
      <td>2&nbsp;KB SRAM + 32&nbsp;KB Flash</td>
    </tr>
    <tr>
      <td><strong>Wi-Fi</strong></td>
      <td>Sí</td>
      <td>Sí</td>
      <td>No</td>
    </tr>
    <tr>
      <td><strong>Bluetooth</strong></td>
      <td>4.2 + BLE</td>
      <td>4.2 + BLE</td>
      <td>No</td>
    </tr>
    <tr>
      <td><strong>SPI</strong></td>
      <td>1</td>
      <td>4</td>
      <td>1</td>
    </tr>
    <tr>
      <td><strong>I²C</strong></td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <td><strong>UART</strong></td>
      <td>1</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <td><strong>Compatibilidad cámara</strong></td>
      <td>CSI (cámara oficial)</td>
      <td>OV2640 (ESP32-CAM)</td>
      <td>No</td>
    </tr>
    <tr>
      <td><strong>Consumo típico</strong></td>
      <td>0.7–1.5&nbsp;W</td>
      <td>0.2–0.6&nbsp;W</td>
      <td>0.05–0.2&nbsp;W</td>
    </tr>
    <tr>
      <td><strong>Precio estimado</strong></td>
      <td>15–20&nbsp;€</td>
      <td>4–8&nbsp;€</td>
      <td>25–30&nbsp;€</td>
    </tr>
  </tbody>
</table>



---

## 3. Fundamentos – Interfaces de comunicación

<style>
.table-serial {
  width: 100%;
  border-collapse: collapse;
  font-size: 24px;              /* ajusta 22–26 según necesites */
}
.table-serial th, .table-serial td {
  border: 1px solid #ddd;
  padding: 6px 8px;             /* padding reducido para que entre */
  vertical-align: top;
}
.table-serial thead th {
  background: #f6f7f9;
  text-align: left;
}
.table-serial td:nth-child(1),
.table-serial td:nth-child(2),
.table-serial td:nth-child(5) {  /* columnas más “cortas” en ancho */
  white-space: nowrap;
}
.table-serial .muted {
  color: #666; font-size: 90%;
}
</style>

<table class="table-serial">
  <thead>
    <tr>
      <th>Característica</th>
      <th>SPI</th>
      <th>I²C</th>
      <th>UART</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tipo de comunicación</td>
      <td>Síncrona</td>
      <td>Síncrona</td>
      <td>Asíncrona</td>
    </tr>
    <tr>
      <td>Arquitectura</td>
      <td>Primario–secundario</td>
      <td>Primario–secundario</td>
      <td>Punto a punto</td>
    </tr>
    <tr>
      <td>Nº de líneas</td>
      <td>4 <span class="muted">(CLK, CS, MOSI, MISO)</span></td>
      <td>2 <span class="muted">(SDA, SCL)</span></td>
      <td>2 <span class="muted">(TX, RX)</span></td>
    </tr>
    <tr>
      <td>Dúplex</td>
      <td>Full</td>
      <td>Half</td>
      <td>Full</td>
    </tr>
    <tr>
      <td>Nº de dispositivos</td>
      <td>1 primario, varios secundarios</td>
      <td>1 primario, varios secundarios</td>
      <td>Solo dos</td>
    </tr>
    <tr>
      <td>Velocidad típica</td>
      <td>1–10&nbsp;Mbps</td>
      <td>100&nbsp;kbit/s – 3.4&nbsp;Mbps</td>
      <td>9.6&nbsp;kbit/s – 3&nbsp;Mbps</td>
    </tr>
    <tr>
      <td>Control de dirección</td>
      <td>Señal CS por secundario</td>
      <td>Dirección en protocolo</td>
      <td>No necesario</td>
    </tr>
  </tbody>
</table>

---

## 3. Fundamentos – Comunicación por radiofrecuencia

<style>
.table-rf {
  width: 100%;
  border-collapse: collapse;
  font-size: 26px; /* Ajusta a 24 si no entra bien */
}
.table-rf th, .table-rf td {
  border: 1px solid #ddd;
  padding: 6px 10px;
  text-align: center;
  vertical-align: middle;
}
.table-rf thead th {
  background: #f6f7f9;
  text-align: center;
}
.table-rf td:first-child {
  text-align: left;
  font-weight: bold;
}
</style>

<table class="table-rf">
  <thead>
    <tr>
      <th>Característica</th>
      <th>LoRa</th>
      <th>XBee (802.15.4)</th>
      <th>APC220</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Frecuencia</td>
      <td>433 / 868 / 915 MHz</td>
      <td>2.4 GHz</td>
      <td>433 MHz</td>
    </tr>
    <tr>
      <td>Modulación</td>
      <td>CSS (Chirp Spread)</td>
      <td>DSSS + O-QPSK</td>
      <td>GFSK</td>
    </tr>
    <tr>
      <td>Velocidad de datos</td>
      <td>0.3–27 kbps</td>
      <td>250 kbps</td>
      <td>1.2–19.2 kbps</td>
    </tr>
    <tr>
      <td>Alcance típico</td>
      <td>hasta 15 km</td>
      <td>30–300 m</td>
      <td>hasta 1 km</td>
    </tr>
    <tr>
      <td>Corrección errores</td>
      <td>FEC (CR 4/5–4/8)</td>
      <td>No especificado</td>
      <td>FEC + AGC</td>
    </tr>
    <tr>
      <td>Interfaz MCU</td>
      <td>UART</td>
      <td>UART</td>
      <td>UART</td>
    </tr>
  </tbody>
</table>

---

## 3. Fundamentos – Sensor de presión barométrica

- Mide **presión atmosférica** → se calcula altitud usando el modelo ISA  
- A mayor altura, menor presión (relación con densidad del aire)  
- Factores que afectan la precisión: temperatura, humedad, viento  
- Usado para estimar **altura relativa durante el vuelo**

**Ejemplos de sensores comunes:**
<style>
.table-compact{width:100%;border-collapse:collapse;font-size:22px;}
.table-compact th,.table-compact td{border:1px solid #ddd;padding:6px 8px;vertical-align:top;}
.table-compact th{background:#f7f7f7;text-align:left;}
.table-compact td{word-break:break-word;}
.table-compact td:nth-child(1){white-space:nowrap;}
</style>

## Sensores de presión / altitud

<table class="table-compact">
  <thead>
    <tr>
      <th>Sensor</th>
      <th>Rango de presión</th>
      <th>Precisión</th>
      <th>Interfaz</th>
      <th>Consumo</th>
      <th>Precio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>BMP388</strong></td>
      <td>300–1250 hPa</td>
      <td>±8 Pa (±0,66 m)</td>
      <td>I²C / SPI</td>
      <td>3.4 µA</td>
      <td>~3,50 €</td>
    </tr>
    <tr>
      <td><strong>BME280</strong></td>
      <td>300–1100 hPa</td>
      <td>±12 Pa (±1 m)</td>
      <td>I²C / SPI</td>
      <td>2.7 µA</td>
      <td>~4,00 €</td>
    </tr>
    <tr>
      <td><strong>MPL3115A2</strong></td>
      <td>50–1100 hPa</td>
      <td>±0,04 hPa (±0,3 m)</td>
      <td>I²C</td>
      <td>40 µA</td>
      <td>~6,00 €</td>
    </tr>
  </tbody>
</table>
i


---

## 3. Fundamentos – IMU (Inertial Measurement Unit)

- Mide **aceleración** (3 ejes) y **velocidad angular** (3 ejes)  
- Algunos modelos incluyen **magnetómetro** para calcular rumbo  
- Permite conocer la **orientación** en términos de pitch, yaw y roll  
- Modelos avanzados incluyen procesador interno para fusión sensorial

**Sensores IMU:**
<style>
.table-compact{width:100%;border-collapse:collapse;font-size:22px;}
.table-compact th,.table-compact td{border:1px solid #ddd;padding:6px 8px;vertical-align:top;}
.table-compact th{background:#f7f7f7;text-align:left;}
.table-compact td{word-break:break-word;}
.table-compact td:nth-child(1){white-space:nowrap;}
</style>

<table class="table-compact">
  <thead>
    <tr>
      <th>Sensor</th>
      <th>Componentes</th>
      <th>Salida de orientación</th>
      <th>Interfaz</th>
      <th>Consumo</th>
      <th>Precio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>MPU6050</strong></td>
      <td>Acelerómetro + Giroscopio</td>
      <td>No (requiere fusión externa)</td>
      <td>I²C</td>
      <td>3.9 mA</td>
      <td>~1,50 €</td>
    </tr>
    <tr>
      <td><strong>BNO055</strong></td>
      <td>Acelerómetro + Giroscopio + Magnetómetro</td>
      <td>Sí (fusión interna)</td>
      <td>I²C / UART</td>
      <td>12 mA</td>
      <td>~9,00 €</td>
    </tr>
    <tr>
      <td><strong>BNO085</strong></td>
      <td>Acelerómetro + Giroscopio + Magnetómetro</td>
      <td>Sí (mayor precisión)</td>
      <td>I²C / UART / SPI</td>
      <td>3.5 mA</td>
      <td>~14,00 €</td>
    </tr>
  </tbody>
</table>




---

## 3. Fundamentos – GNSS

- Sistemas: **GPS**, **Galileo**, **GLONASS**, **BeiDou**  
- Un receptor necesita **≥3 satélites** para calcular posición (trilateración)  
- Variables: precisión, frecuencia de actualización, constelaciones soportadas  

**Comparativa de módulos GNSS:**

<style>
.table-gnss {
  width: 100%;
  border-collapse: collapse;
  font-size: 24px;
}
.table-gnss th, .table-gnss td {
  border: 1px solid #ddd;
  padding: 6px 10px;
  vertical-align: middle;
  text-align: center;
}
.table-gnss thead th {
  background: #f6f7f9;
}
.table-gnss td:first-child {
  text-align: left;
  font-weight: bold;
  white-space: nowrap;
}
</style>

<table class="table-gnss">
  <thead>
    <tr>
      <th>Módulo</th>
      <th>Constelaciones</th>
      <th>Precisión típica</th>
      <th>Frecuencia</th>
      <th>Consumo</th>
      <th>Precio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BN-880</td>
      <td>GPS, GLONASS, Galileo, BeiDou</td>
      <td>~2 m CEP</td>
      <td>1–10 Hz</td>
      <td>50 mA @ 5V</td>
      <td>15–25 €</td>
    </tr>
    <tr>
      <td>NEO-M8N</td>
      <td>GPS, GLONASS, Galileo, BeiDou</td>
      <td>~2 m CEP</td>
      <td>1–18 Hz</td>
      <td>&lt;150 mA @ 5V</td>
      <td>35–40 €</td>
    </tr>
    <tr>
      <td>NEO-F9P</td>
      <td>GPS, GLONASS, Galileo, BeiDou (RTK)</td>
      <td>cm-level (con RTK)</td>
      <td>hasta 20 Hz</td>
      <td>100 mA @ 3.3V</td>
      <td>110–130 €</td>
    </tr>
  </tbody>
</table>


<!-- ---

## 3. Fundamentos – Protocolos de transmisión de video

| Protocolo | Transporte | Latencia típica | Segmentación |
|----------|------------|----------------|-------------|
| **RTMP** | TCP (1935) | 3–5 s          | Chunks multiplexados |
| **HLS**  | HTTP (TCP) | 5–15 s         | Archivos .ts + playlist |
| **DASH** | HTTP (TCP) | 4–10 s         | MP4 + manifiesto .mpd |
| **WebRTC** | UDP      | <500 ms        | Flujo continuo P2P | -->


---

## 4. Diseño e implementación – Hardware

- **Unidad de procesamiento:** Raspberry Pi Zero 2 W
- **Sensores:**
  - BMP388 (presión y temperatura)
  - BNO085 (IMU con fusión sensorial)
  - BN-880 (GNSS multi-constelación + brújula)
- **Cámara CSI:** Raspberry Pi Camera Module v2
- **Transmisión:** WiFi si hay red disponible, LoRa E32-900T20D si no
- **Alimentación:** batería 18650 + cargador MCP73871 + boost converter a 5V
- **Estación de tierra:** Raspberry Pi 4 + receptor LoRa


---

## 4. Selección de tecnologías – Software

- **Software embebido:**  
  - Scripts en Python para lectura de sensores, GNSS, captura de vídeo y envío de datos  

- **Backend:**  
  - Spring Boot (Java) + API REST  
  - RabbitMQ (AMQP) para mensajería de eventos  
  - PostgreSQL para persistencia  

- **Frontend:**  
  - Desarrollado en **Flutter**  
  - Comunicación en tiempo real mediante WebSocket


---

## 4. Selección de tecnologías – Arquitectura general

<img src="./figuras/cansat_architecture_slide.png" alt="CanSat" height="500" width="1000">


---

## 4. Selección de tecnologías – Conexion

<style>
.two-imgs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: center;
  justify-items: center;
}
.two-imgs img {
  max-height: 420px;
  width: 100%;
  object-fit: contain;
}
</style>


<div class="two-imgs">
  <img src="./figuras/conexion_sensores.png" alt="Conexión sensores">
  <img src="./figuras/conexion_gps.png" alt="Conexión GNSS">
</div>


---

## 4. Selección de tecnologías – Conexion


<div class="two-imgs">
  <img src="./figuras/conexion_cargador.png" alt="Conexión sensores">
  <img src="./figuras/conexion_ground.png" alt="Conexión GNSS">
</div>


---

## 4. Selección de tecnologías – Conexion


<div class="two-imgs">
  <img src="./figuras/pcb_montaje_frontal.png" alt="Conexión sensores">
  <img src="./figuras/pcb_montaje_trasero.png" alt="Conexión GNSS">
</div>


---


## 4. Selección de tecnologías – Interfaz

<div style="display:flex; justify-content:center; align-items:center; height:100%;">
  <img src="./figuras/initerfaz_general.png"
       alt="CanSat"
       height="550"
       style="margin-bottom:20px;">
</div>


---

## 5. Pruebas – Integración con datos simulados

- **Objetivo:** validar backend y frontend **sin hardware**
- **Telemetría simulada (Python + RabbitMQ):**
  - Publicación periódica de eventos JSON (altitud, temperatura, GNSS, actitud)
  - Verificación de ingesta, persistencia y actualización **en tiempo real** (métricas, gráficas, mapa)
- **Vídeo simulado (Python + FFmpeg → RTMP):**
  - Generación de frames sintéticos y envío a **servidor RTMP**
  - Reproducción en el **frontend** con baja latencia


---

## 5. Pruebas – Sistema real (CanSat + Estación + Servicios)

- **Transmisión por WiFi:**  
  Eventos → RabbitMQ → PostgreSQL → WebSocket → Frontend  
  **Latencia < 1 s** desde la generación a la visualización

- **Transmisión por LoRa (868 MHz):**  
  Recepción estable en campo abierto **hasta > 1 km**  
  Pérdidas ocasionales a distancias superiores (acorde al módulo empleado)

- **Autonomía energética:** ≈ **2 h** de operación continua con telemetría + vídeo

- **Persistencia y exportación:**  
  Datos en **PostgreSQL** y descarga en **JSONL** vía API

<!-- ---

<style>
.table-tests {
  width: 100%;
  border-collapse: collapse;
  font-size: 26px;
}
.table-tests th, .table-tests td {
  border: 1px solid #ddd;
  padding: 6px 10px;
  vertical-align: middle;
}
.table-tests thead th {
  background: #f6f7f9;
  text-align: left;
}
.table-tests td:first-child { white-space: nowrap; font-weight: 600; }
</style>

## 5. Resultados (resumen)

<table class="table-tests">
  <thead>
    <tr>
      <th>Prueba</th>
      <th>Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Transmisión por WiFi</td>
      <td>Latencia < 1 s, integración end-to-end correcta</td>
    </tr>
    <tr>
      <td>Transmisión por LoRa</td>
      <td>Recepción estable hasta > 1 km (campo abierto)</td>
    </tr>
    <tr>
      <td>Autonomía</td>
      <td>≈ 2 h de operación continua (telemetría + vídeo)</td>
    </tr>
    <tr>
      <td>Persistencia/Exportación</td>
      <td>Datos en PostgreSQL y descarga en JSONL vía API</td>
    </tr>
  </tbody>
</table> -->

---


## 6. Conclusions

- **Goal achieved:** reusable, hardware-independent platform for real-time CanSat data visualization.
- **Modular architecture:** data capture, transmission, backend, frontend → independent changes; easier maintenance & reuse.
- **Validation:** built a real CanSat; hardware-independent; adaptable to other sensors/configurations.
- **Video challenge (Pi Zero 2 W):** unstable → 640×480 @ 15 fps + hardware-accelerated FFmpeg → smooth, continuous video.



---

## 7. Future Work

- Add more **real-time charts** and custom visualizations
- Implement **telecommanding system** to remotely control sensors and configuration
- Add **authentication** to protect sensitive data
- Support monitoring of **multiple CanSats** simultaneously

---

<style>
.questions { display: grid; place-items: center; text-align: center; padding: 0 6%; }
h1 { font-size: 86px; color: var(--accent); margin: 0 0 12px; }
p.meta { font-size: 34px; color: #111; margin: 6px 0 0; }
.footer { color: #666; font-size: 28px; margin-top: 20px}
</style>

<div class="questions">
<h1>Preguntas</h1>
<p class="meta">Diseño e implementación de un sistema de adquisición, transmisión y visualización de datos basado en CanSat</p>
<p class="meta">Sergio García Sánchez</p>
<p class="footer">Gracias por su atención</p>
</div>

