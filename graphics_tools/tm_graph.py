import json
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

filename = "events_2025-08-24_00-00-00-000_to_2025-08-25_02-54-00-000.jsonl"

timestamps = []
series = {}  # campo -> list[float]

def to_float(x):
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")

with open(filename, "r") as f:
    for line in f:
        try:
            d = json.loads(line)
            dt = datetime.fromisoformat(d["datetime"])
            payload = d["payload"]
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            continue

        # Añadimos timestamp
        timestamps.append(dt)

        # 1) Asegurar que TODAS las claves vistas hasta ahora tienen una entrada para este timestamp
        for k in series.keys():
            series[k].append(to_float(payload.get(k)))

        # 2) Detectar claves nuevas en este payload y backfill con NaN
        for k in payload.keys():
            if k not in series:
                # backfill con NaN para los timestamps previos y valor actual
                prev_len = len(timestamps) - 1
                series[k] = [float("nan")] * prev_len
                series[k].append(to_float(payload.get(k)))
            # si ya existía, ya se añadió en el paso (1)

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6))
lines = {}
# Opcional: ordenar para que lat/long salgan primero en la leyenda
ordered_keys = sorted(series.keys(), key=lambda k: (k not in ("lat", "long", "longitude", "lon", "lng"), k))

for k in ordered_keys:
    (ln,) = ax.plot(timestamps, series[k], label=k)
    lines[k] = ln

ax.set_xlabel("Time")
ax.set_ylabel("Values")
ax.set_title("Telemetry Over Time")
leg = ax.legend()
ax.grid(True)
ax.yaxis.set_major_locator(MaxNLocator(nbins=6, prune="both"))

# Eje X legible
locator = mdates.AutoDateLocator(minticks=5, maxticks=8)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))

# Interactividad: click para ocultar/mostrar
artist_to_line = {}
for legline, k in zip(leg.get_lines(), ordered_keys):
    legline.set_picker(True)
    artist_to_line[legline] = lines[k]
for legtext, k in zip(leg.get_texts(), ordered_keys):
    legtext.set_picker(True)
    artist_to_line[legtext] = lines[k]

def sync_legend_alpha():
    for legline, k in zip(leg.get_lines(), ordered_keys):
        legline.set_alpha(1.0 if lines[k].get_visible() else 0.2)
    for legtext, k in zip(leg.get_texts(), ordered_keys):
        legtext.set_alpha(1.0 if lines[k].get_visible() else 0.2)

def update_ylim_from_visible(pad_frac=0.05):
    ys = []
    for ln in lines.values():
        if not ln.get_visible():
            continue
        y = np.asarray(ln.get_ydata(), float)
        y = y[np.isfinite(y)]
        if y.size:
            ys.append((y.min(), y.max()))
    if not ys:
        return
    ymin = min(lo for lo, _ in ys)
    ymax = max(hi for _, hi in ys)
    if ymin == ymax:
        delta = 1.0 if ymin == 0 else abs(ymin) * 0.1
        ymin -= delta; ymax += delta
    else:
        pad = (ymax - ymin) * pad_frac
        ymin -= pad; ymax += pad
    ax.set_ylim(ymin, ymax)

def on_pick(event):
    ln = artist_to_line.get(event.artist)
    if ln is None:
        return
    ln.set_visible(not ln.get_visible())
    sync_legend_alpha()
    update_ylim_from_visible()
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("pick_event", on_pick)
sync_legend_alpha()
update_ylim_from_visible()
fig.tight_layout()
plt.show()
