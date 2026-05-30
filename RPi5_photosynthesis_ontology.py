# =====================================================
# Photosynthesis Simulation with Environmental Factors
# Save results as JPEG plots (no MP4)
# =====================================================

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os

# -----------------------------
# 1️⃣ Create Ontology Graph
# -----------------------------
G = nx.DiGraph()

entities = ["Sunlight", "Cloud", "Rain", "Humidity", "Water", "CO2", 
            "Chlorophyll", "Chloroplast", "Chemical Energy", "Glucose", "O2"]
G.add_nodes_from(entities)

relationships = [
    ("Sunlight", "Chlorophyll", "absorbed by"),
    ("Cloud", "Sunlight", "reduces"),
    ("Rain", "Water", "adds"),
    ("Humidity", "Chloroplast", "modifies"),
    ("Chlorophyll", "Chemical Energy", "converts energy"),
    ("Water", "Chloroplast", "used in"),
    ("CO2", "Chloroplast", "used in"),
    ("Chemical Energy", "Glucose", "synthesizes"),
    ("Chloroplast", "Glucose", "produces"),
    ("Glucose", "O2", "byproduct")
]

for src, dst, label in relationships:
    G.add_edge(src, dst, label=label)

# -----------------------------
# 2️⃣ Simulation Function
# -----------------------------
def simulate_photosynthesis(sunlight, water, co2, cloud=0.0, rain=0.0, humidity=0.5, temperature=25):
    sunlight_effective = sunlight * (1 - cloud)
    water_effective = min(1.0, water + rain * 0.3)
    temp_factor = max(0, 1 - abs(temperature - 25)/25)
    humidity_factor = 1 - abs(humidity - 0.5)
    limiting_factor = min(sunlight_effective, water_effective, co2)
    efficiency = 0.9
    glucose = efficiency * limiting_factor * temp_factor * humidity_factor * 100
    o2 = glucose * 0.8
    return glucose, o2

# -----------------------------
# 3️⃣ Simulation Over Time
# -----------------------------
time_steps = 50
sunlight_levels = np.clip(np.linspace(0.5, 1.0, time_steps) + 0.05*np.random.randn(time_steps), 0, 1)
cloud_levels = np.random.uniform(0, 0.4, time_steps)
rain_levels = np.random.uniform(0, 0.3, time_steps)
humidity_levels = 0.5 + 0.1 * np.sin(np.linspace(0, 3*np.pi, time_steps))

water_level = 0.8
co2_level = 0.9
temperature = 28

glucose_history = []
o2_history = []

for t in range(time_steps):
    glucose, o2 = simulate_photosynthesis(
        sunlight=sunlight_levels[t],
        water=water_level,
        co2=co2_level,
        cloud=cloud_levels[t],
        rain=rain_levels[t],
        humidity=humidity_levels[t],
        temperature=temperature
    )
    glucose_history.append(glucose)
    o2_history.append(o2)

# -----------------------------
# 4️⃣ Save Ontology Graph as JPEG
# -----------------------------
plt.figure(figsize=(12,8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=2500, font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue')
plt.title("Photosynthesis Ontology with Environmental Factors")
plt.savefig("photosynthesis_ontology.jpeg", dpi=150)
plt.close()

# -----------------------------
# 5️⃣ Save Glucose & O2 Time Series as JPEG
# -----------------------------
plt.figure(figsize=(10,6))
plt.plot(range(time_steps), glucose_history, label="Glucose", color="green", linewidth=2)
plt.plot(range(time_steps), o2_history, label="O2", color="blue", linewidth=2)
plt.xlabel("Time Step")
plt.ylabel("Production Units")
plt.title("Photosynthesis Simulation Over Time")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("photosynthesis_simulation_time_series.jpeg", dpi=150)
plt.close()

print("✓ Saved JPEG plots:")
print("   • photosynthesis_ontology.jpeg")
print("   • photosynthesis_simulation_time_series.jpeg")
