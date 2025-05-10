import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import net_ppm  # Make sure this has `expected_avg_nitrogen_ppm`

# --- MODULE 1: Conversion Functions ---
def ppm_to_kg_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    return ppm * soil_depth_cm * bulk_density * 0.1

def ppm_to_lb_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    kg_ha = ppm_to_kg_ha(ppm, soil_depth_cm, bulk_density)
    return kg_ha * 2.20462

# --- MODULE 2: Fertilizer Recommendation DB ---
FERTILIZER_DB = {
    'nitrogen': {
        'natural': ['composted manure', 'blood meal', 'legume cover crops'],
        'synthetic': ['urea', 'ammonium nitrate']
    },
    'phosphorus': {
        'natural': ['bone meal', 'rock phosphate'],
        'synthetic': ['superphosphate']
    },
    'potassium': {
        'natural': ['wood ash', 'kelp meal'],
        'synthetic': ['muriate of potash']
    }
}

def recommend_all_fertilizers(preference='natural'):
    result = []
    for nutrient, sources in FERTILIZER_DB.items():
        ferts = sources.get(preference.lower(), [])
        result.append(f"{nutrient.title()}: {', '.join(ferts) if ferts else 'None Found'}")
    return result

# --- MODULE 3: ML Models ---
# Model A: Status prediction (Deficient / Optimal / Excessive)
X_status = np.array([
    [20, 1], [50, 1], [90, 1],
    [30, 2], [80, 2], [110, 2],
    [40, 3], [70, 3], [130, 3]
])
y_status = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])  # 0: Deficient, 1: Optimal, 2: Excessive
status_model = DecisionTreeClassifier()
status_model.fit(X_status, y_status)

STATUS_LABELS = {0: "Deficient", 1: "Optimal", 2: "Excessive"}

# Model B: Fertilizer type decision (Natural vs Synthetic)
X_fertilizer = np.array([
    [20, 1], [50, 1], [90, 1],  # Assume low ppm prefers natural
    [110, 2], [130, 2], [150, 2]  # Higher ppm prefers synthetic
])
y_fertilizer = np.array([0, 0, 0, 1, 1, 1])  # 0: Natural, 1: Synthetic
fertilizer_model = DecisionTreeClassifier()
fertilizer_model.fit(X_fertilizer, y_fertilizer)

FERTILIZER_LABELS = {0: "Natural", 1: "Synthetic"}

# --- Tkinter GUI ---
def run_analysis():
    try:
        ppm = net_ppm.expected_avg_nitrogen_ppm
        area = float(area_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric area.")
        return

    # Conversions
    kg_ha = ppm_to_kg_ha(ppm)
    lb_ha = ppm_to_lb_ha(ppm)

    # Predictions
    status = STATUS_LABELS[status_model.predict([[ppm, area]])[0]]
    fert_type = FERTILIZER_LABELS[fertilizer_model.predict([[ppm, area]])[0]]

    # Get Recommendations
    fertilizers = recommend_all_fertilizers(fert_type)

    # Display Results
    result = (
        f"PPM (auto-read): {ppm}\n"
        f"Converted: {kg_ha:.2f} kg/ha, {lb_ha:.2f} lb/ha\n"
        f"Soil Status: {status}\n"
        f"Recommended Fertilizer Type (ML): {fert_type}\n\n"
        "Recommended Fertilizers:\n" +
        "\n".join(fertilizers)
    )
    result_label.config(text=result)

# --- Main Window ---
root = tk.Tk()
root.title("Soil Fertility Recommendation System")

# Layout
ttk.Label(root, text="Enter Area (ha):").grid(column=0, row=0, padx=10, pady=5, sticky='e')
area_entry = ttk.Entry(root)
area_entry.grid(column=1, row=0)

run_button = ttk.Button(root, text="Analyze", command=run_analysis)
run_button.grid(column=0, row=1, columnspan=2, pady=10)

result_label = ttk.Label(root, text="", justify="left", foreground="darkgreen")
result_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

root.mainloop()
