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
    "fontsize": "10",
    "ranksep": "1.2",   # separacion horizontal entre rangos
    "nodesep": "0.6",   # separacion entre nodos
}

with Diagram(
    filename="slides/figuras/cansat_architecture_slide",
    show=True,
    outformat="png",
    direction="LR",          # ⬅️ Clusters y nodos de izquierda a derecha
    graph_attr=graph_attr,
):
    # --- Infraestructura (derecha) ---
    with Cluster("Infraestructura de visualización"):
        rabbit = RabbitMQ("RabbitMQ")
        backend = Rack("Backend Spring Boot")
        db = PostgreSQL("PostgreSQL")
        frontend = Flutter("Frontend Flutter")
        rtmp_srv = Rack("Servidor RTMP")

        backend >> db
        backend >> frontend
        rabbit >> backend
        rtmp_srv >> frontend

        infra_anchor = Blank("")   # ancla del cluster

    # --- Estación de tierra (centro) ---
    with Cluster("Estación de tierra"):
        pi_ground = Rack("RPi 4")
        lora_rx = Rack("Receptor LoRa")

        lora_rx >> pi_ground
        pi_ground >> rabbit

        ground_anchor = Blank("")

    # --- CanSat (izquierda) ---
    with Cluster("CanSat"):
        pi_zero = Rack("RPi Zero 2 W")
        imu = Rack("IMU BNO085")
        gnss = Rack("GNSS BN-880")
        cam = Rack("Cámara CSI")
        bmp = Rack("BMP388")
        lora_tx = Rack("Transmisor LoRa")

        [imu, gnss, cam, bmp] >> pi_zero
        pi_zero >> lora_tx >> lora_rx

        # Enlaces por Wi-Fi (si disponible)
        pi_zero >> Edge(label="si hay Wi-Fi") >> rabbit
        pi_zero >> Edge(label="si hay Wi-Fi") >> rtmp_srv

        cansat_anchor = Blank("")

    # --- Forzar orden L→R de clusters con aristas invisibles ---
    cansat_anchor >> Edge(style="invis") >> ground_anchor
    ground_anchor >> Edge(style="invis") >> infra_anchor
