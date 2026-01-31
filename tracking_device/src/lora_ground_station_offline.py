import serial
import os
import json
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from pyqtgraph.Qt import QtWidgets, QtCore
from collections import deque
import signal

PORT = '/dev/cu.usbmodem2101'
max_points = 90000

yaw, roll, pitch = deque(maxlen=max_points), deque(maxlen=max_points), deque(maxlen=max_points)
temps, altitudes = deque(maxlen=max_points), deque(maxlen=max_points)

class TelemetryWindow(QtWidgets.QMainWindow):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.setWindowTitle("Realtime Telemetry")
        self.resize(1600, 900)
        self.setStyleSheet("background-color: white;")

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        self.labels = {}
        values_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(values_layout)

        label_styles = {
            "yaw": "color: red; font-size: 36px; font-weight: bold; background-color: white;",
            "roll": "color: green; font-size: 36px; font-weight: bold; background-color: white;",
            "pitch": "color: blue; font-size: 36px; font-weight: bold; background-color: white;",
            "temperature": "color: magenta; font-size: 36px; font-weight: bold; background-color: white;",
            "altitude": "color: orange; font-size: 36px; font-weight: bold; background-color: white;"
        }

        positions = {
            "yaw": (0, 0),
            "roll": (0, 1),
            "pitch": (0, 2),
            "temperature": (1, 0),
            "altitude": (1, 1)
        }

        for key, pos in positions.items():
            lbl = QtWidgets.QLabel(f"{key}: ---")
            lbl.setStyleSheet(label_styles[key])
            lbl.setAlignment(QtCore.Qt.AlignCenter)
            self.labels[key] = lbl
            values_layout.addWidget(lbl, *pos)

        orientation_row = QtWidgets.QHBoxLayout()
        orientation_container = QtWidgets.QWidget()
        orientation_container.setLayout(orientation_row)

        # --- Gráfica de orientación ---
        self.p1 = pg.PlotWidget(title="Orientation (Yaw, Roll, Pitch)")
        self.p1.setTitle("Orientation (Yaw, Roll, Pitch)", size="24pt", color="k")
        self.curve_yaw = self.p1.plot(pen=pg.mkPen('r', width=10), name="Yaw")
        self.curve_roll = self.p1.plot(pen=pg.mkPen('g', width=10), name="Roll")
        self.curve_pitch = self.p1.plot(pen=pg.mkPen('b', width=10), name="Pitch")
        orientation_row.addWidget(self.p1, stretch=2)

        # Añadir crosshair y label
        self.crosshair(self.p1, "orientation")

        # --- 3D ---
        self.view3d = gl.GLViewWidget()
        self.view3d.setCameraPosition(distance=10)
        orientation_row.addWidget(self.view3d, stretch=1)

        axis = gl.GLAxisItem()
        axis.setSize(5, 5, 5)
        self.view3d.addItem(axis)

        self.verts = np.array([
            [1,1,1], [1,1,-1], [1,-1,1], [1,-1,-1],
            [-1,1,1], [-1,1,-1], [-1,-1,1], [-1,-1,-1]
        ])
        self.faces = np.array([
            [0,1,3], [0,2,3],
            [4,5,7], [4,6,7],
            [0,1,5], [0,4,5],
            [2,3,7], [2,6,7],
            [0,2,6], [0,4,6],
            [1,3,7], [1,5,7],
        ])
        self.colors = np.array([[0,0,1,0.8] for _ in self.faces])
        self.mesh = gl.GLMeshItem(vertexes=self.verts, faces=self.faces, faceColors=self.colors,
                                  smooth=False, drawEdges=True, edgeColor=(0,0,0,1))
        self.mesh.scale(1.5,1.5,1.5)
        self.view3d.addItem(self.mesh)

        main_layout.addWidget(orientation_container, stretch=1)

        # --- Temperatura ---
        self.p2 = pg.PlotWidget()
        self.p2.setTitle("Temperature (°C)", size="24pt", color="k")
        self.curve_temp = self.p2.plot(pen=pg.mkPen('m', width=10))
        self.crosshair(self.p2, "temperature")
        main_layout.addWidget(self.p2, stretch=1)

        # --- Altitud ---
        self.p3 = pg.PlotWidget()
        self.p3.setTitle("Altitude (m)", size="24pt", color="k")
        self.curve_alt = self.p3.plot(pen=pg.mkPen('orange', width=10))
        self.crosshair(self.p3, "altitude")
        main_layout.addWidget(self.p3, stretch=1)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(100)

    def crosshair(self, plot, name):
        vLine = pg.InfiniteLine(angle=90, movable=False, pen='k')
        hLine = pg.InfiniteLine(angle=0, movable=False, pen='k')
        text = pg.TextItem("", anchor=(1,1))
        plot.addItem(vLine, ignoreBounds=True)
        plot.addItem(hLine, ignoreBounds=True)
        plot.addItem(text)

        def mouseMoved(evt):
            pos = evt[0]
            if plot.sceneBoundingRect().contains(pos):
                mousePoint = plot.plotItem.vb.mapSceneToView(pos)
                x = int(mousePoint.x())
                if name == "orientation" and 0 <= x < len(yaw):
                    y1, y2, y3 = yaw[x], roll[x], pitch[x]
                    vLine.setPos(x)
                    hLine.setPos(y1)
                    text.setText(f"x={x}, yaw={y1:.2f}, roll={y2:.2f}, pitch={y3:.2f}")
                    text.setPos(x, y1)
                elif name == "temperature" and 0 <= x < len(temps):
                    y = temps[x]
                    vLine.setPos(x)
                    hLine.setPos(y)
                    text.setText(f"x={x}, temp={y:.2f}")
                    text.setPos(x, y)
                elif name == "altitude" and 0 <= x < len(altitudes):
                    y = altitudes[x]
                    vLine.setPos(x)
                    hLine.setPos(y)
                    text.setText(f"x={x}, alt={y:.2f}")
                    text.setPos(x, y)

        proxy = pg.SignalProxy(plot.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
        setattr(self, f"proxy_{name}", proxy)

    def update_data(self):
        if self.ser.in_waiting > 0:
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                try:
                    payload = json.loads(line)
                except Exception:
                    return

                yaw.append(payload.get("yaw", None))
                roll.append(payload.get("roll", None))
                pitch.append(payload.get("pitch", None))
                temps.append(payload.get("temperature", None))
                altitudes.append(payload.get("altitude", None))

                for k, v in payload.items():
                    if k in self.labels and v is not None:
                        self.labels[k].setText(f"{k}: {v:.2f}")

                x = list(range(len(yaw)))
                self.curve_yaw.setData(x, list(yaw))
                self.curve_roll.setData(x, list(roll))
                self.curve_pitch.setData(x, list(pitch))
                self.curve_temp.setData(x, list(temps))
                self.curve_alt.setData(x, list(altitudes))

                y = np.radians(payload.get("yaw", 0))
                p = np.radians(payload.get("pitch", 0))
                r = np.radians(payload.get("roll", 0))

                Rz = np.array([
                    [np.cos(y), -np.sin(y), 0],
                    [np.sin(y),  np.cos(y), 0],
                    [0, 0, 1]
                ])
                Ry = np.array([
                    [np.cos(p), 0, np.sin(p)],
                    [0, 1, 0],
                    [-np.sin(p), 0, np.cos(p)]
                ])
                Rx = np.array([
                    [1, 0, 0],
                    [0, np.cos(r), -np.sin(r)],
                    [0, np.sin(r),  np.cos(r)]
                ])

                R = Rz @ Ry @ Rx
                verts_rot = (self.verts @ R.T)
                self.mesh.setMeshData(vertexes=verts_rot, faces=self.faces, faceColors=self.colors)

    def closeEvent(self, event):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")
        event.accept()


if __name__ == "__main__":
    print("Checking port access...")
    if os.path.exists(PORT) and os.access(PORT, os.R_OK | os.W_OK):
        try:
            ser = serial.Serial(PORT, 115200, timeout=0)
            print("Serial port opened.")

            signal.signal(signal.SIGINT, signal.SIG_DFL)

            app = QtWidgets.QApplication([])
            window = TelemetryWindow(ser)
            window.show()
            app.exec_()

        except Exception as e:
            print(f"Error opening port: {e}")
    else:
        print(f"Port {PORT} not accessible or doesn't exist.")
