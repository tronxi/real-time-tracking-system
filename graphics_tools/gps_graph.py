import json
import folium

def plot_positions_from_jsonl(jsonl_path, output_map='position_map.html'):
    positions = []

    with open(jsonl_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                if data.get("type") == "POSITION":
                    payload = data["payload"]
                    lat = payload["lat"]
                    lon = payload["long"]
                    positions.append((lat, lon))
            except json.JSONDecodeError:
                continue

    if not positions:
        print("Invalid file. No positions found.")
        return

    m = folium.Map(location=positions[0], zoom_start=18)

    folium.PolyLine(positions, color="blue", weight=2.5, opacity=1).add_to(m)
    for pos in positions:
        folium.CircleMarker(location=pos, radius=2, color='red', fill=True).add_to(m)

    m.save(output_map)
    print(f"Generated: {output_map}")

if __name__ == "__main__":
    plot_positions_from_jsonl("gps_20250628_025855.jsonl")
