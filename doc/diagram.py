from diagrams import Cluster, Diagram, Edge
from diagrams.generic.compute import Rack
from diagrams.generic.network import Router
from diagrams.onprem.queue import RabbitMQ
from diagrams.generic.blank import Blank
from diagrams.programming.framework import Flutter
from diagrams.onprem.database import PostgreSQL
graph_attr = {
    "margin": "0",
    "pad": "0",
    "dpi": "300",
    "fontsize": "10"
}

with Diagram(filename="Imagenes/Bitmap/cansat_architecture", show=True, outformat="png", direction="TB", graph_attr=graph_attr):
    with Cluster("Infraestructura en visualización", direction="LR"):
        rabbit = RabbitMQ("RabbitMQ")
        backend = Rack("Backend Spring Boot")
        db = PostgreSQL("PostgreSQL")
        frontend = Flutter("Frontend Flutter")
        rtmp_srv = Rack("Servidor RTMP")
        backend >> db
        backend >> frontend
        rabbit >> backend
        rtmp_srv >> frontend

    with Cluster("Estación de Tierra", direction="LR"):
        pi_ground = Rack("RPi 4")
        lora_rx = Rack("Receptor LoRa")
        lora_rx >> pi_ground
        pi_ground >> rabbit

    with Cluster("CanSat", direction="LR"):
        pi_zero = Rack("RPi Zero 2 W")
        imu = Rack("IMU BNO085")
        gnss = Rack("GNSS BN-880")
        cam = Rack("Cámara CSI")
        bmp = Rack("BMP388")
        lora_tx = Rack("Transmisor LoRa")

        [imu, gnss, cam, bmp] >> pi_zero
        pi_zero >> lora_tx >> lora_rx

        pi_zero >> Edge(label="si hay conectividad Wi-Fi") >> rabbit
        pi_zero >> Edge(label="si hay conectividad Wi-Fi") >> rtmp_srv
