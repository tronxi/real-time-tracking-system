import json
import folium
from folium.plugins import MousePosition, Fullscreen, MeasureControl

TOOLTIP_FIELDS = [
    "gps_altitude", "altitude", "speed", "pressure", "temperature",
    "cpuTemperature", "roll", "pitch", "yaw"
]

def _fmt(v):
    try:
        f = float(v)
        return f"{f:.2f}"
    except (TypeError, ValueError):
        return str(v)

def plot_positions_from_jsonl(jsonl_path, output_map='position_map.html'):
    points = []

    with open(jsonl_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            if data.get("type") != "TM":
                continue

            payload = data.get("payload", {})
            lat = payload.get("lat")
            lon = payload.get("long")
            if lat is None or lon is None:
                continue

            try:
                lat = float(lat)
                lon = float(lon)
            except (TypeError, ValueError):
                continue

            points.append({
                "lat": lat,
                "lon": lon,
                "datetime": data.get("datetime", ""),
                "payload": payload
            })

    if not points:
        print("Invalid file. No positions found.")
        return

    m = folium.Map(location=[points[0]["lat"], points[0]["lon"]], zoom_start=18)

    path = [(p["lat"], p["lon"]) for p in points]
    folium.PolyLine(path, color="blue", weight=2.5, opacity=1).add_to(m)

    for p in points:

        rows_tt = ""
        present = [k for k in TOOLTIP_FIELDS if k in p["payload"]]
        if not present:
            present = list(p["payload"].keys())[:6]
        for k in present:
            rows_tt += f"<tr><th style='text-align:left;padding-right:8px'>{k}</th><td>{_fmt(p['payload'][k])}</td></tr>"

        tooltip_html = f"""
        <div style="font-family:system-ui,sans-serif;font-size:12px;">
          <div><strong>{p['datetime']}</strong></div>
          <div>lat: {p['lat']:.6f}, lon: {p['lon']:.6f}</div>
          <table style="margin-top:4px;">{rows_tt}</table>
        </div>
        """
        tooltip = folium.Tooltip(tooltip_html, sticky=True, direction='top')

        rows_popup = "".join(
            f"<tr><th style='text-align:left;padding-right:8px'>{k}</th><td>{p['payload'][k]}</td></tr>"
            for k in p["payload"].keys()
        )
        popup_html = f"""
        <div style="font-family:system-ui,sans-serif;font-size:12px;">
          <div style="margin-bottom:6px;"><strong>{p['datetime']}</strong></div>
          <div>lat: {p['lat']:.6f}, lon: {p['lon']:.6f}</div>
          <table style="margin-top:6px;">{rows_popup}</table>
        </div>
        """
        popup = folium.Popup(popup_html, max_width=350)

        folium.CircleMarker(
            location=(p["lat"], p["lon"]),
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.9,
            weight=1,
            tooltip=tooltip,
            popup=popup
        ).add_to(m)

    MousePosition(position='bottomright', separator=' | ', prefix='Mouse', num_digits=6).add_to(m)
    Fullscreen().add_to(m)
    MeasureControl(primary_length_unit='meters').add_to(m)

    m.save(output_map)
    print(f"Generated: {output_map}")

if __name__ == "__main__":
    plot_positions_from_jsonl("events_2025-08-23_07-00-00-000_to_2025-08-23_11-36-26-000.jsonl")
