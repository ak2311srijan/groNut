import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# --- MODULE 1: Conversion Functions ---
def ppm_to_kg_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    return ppm * soil_depth_cm * bulk_density * 0.1

def ppm_to_lb_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    kg_ha = ppm_to_kg_ha(ppm, soil_depth_cm, bulk_density)
    return kg_ha * 2.20462

# --- MODULE 2: Ideal Value Comparison ---
IDEAL_VALUES_KG_HA = {
    'nitrogen': 80,
    'phosphorus': 40,
    'potassium': 60
}

def compare_nutrient(nutrient, actual_kg_ha):
    ideal = IDEAL_VALUES_KG_HA.get(nutrient)
    if ideal is None:
        return "Unknown nutrient"
    if actual_kg_ha < 0.7 * ideal:
        return "Deficient"
    elif actual_kg_ha > 1.3 * ideal:
        return "Excessive"
    else:
        return "Optimal"

# --- MODULE 3: Fertilizer Recommendation ---
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

def recommend_fertilizer(nutrient, preference='natural'):
    return FERTILIZER_DB.get(nutrient, {}).get(preference, [])

# --- MODULE 4: ML Model ---
X_train = np.array([
    [20, 1], [50, 1], [90, 1],
    [30, 2], [80, 2], [110, 2],
    [40, 3], [70, 3], [130, 3]
])
y_train = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])

ml_model = DecisionTreeClassifier()
ml_model.fit(X_train, y_train)

STATUS_LABELS = {0: "Deficient", 1: "Optimal", 2: "Excessive"}

# --- Tkinter GUI Setup ---
def run_analysis():
    nutrient = nutrient_var.get().lower()
    preference = preference_var.get().lower()
    try:
        ppm = float(ppm_entry.get())
        area = float(area_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
        return

    kg_ha = ppm_to_kg_ha(ppm)
    lb_ha = ppm_to_lb_ha(ppm)

    prediction = ml_model.predict([[ppm, area]])[0]
    status = STATUS_LABELS[prediction]

    fertilizers = recommend_fertilizer(nutrient, preference)

    result = (
        f"{nutrient.title()} - {ppm} ppm\n"
        f"Converted: {kg_ha:.2f} kg/ha, {lb_ha:.2f} lb/ha\n"
        f"Status (ML): {status}\n"
        f"Recommended {preference.title()} Fertilizers: {', '.join(fertilizers) if fertilizers else 'None Found'}"
    )
    result_label.config(text=result)

# Main Window
root = tk.Tk()
root.title("Soil Fertility Recommendation System")

# GUI Layout
ttk.Label(root, text="Select Nutrient:").grid(column=0, row=0, padx=10, pady=5, sticky='e')
nutrient_var = tk.StringVar()
nutrient_dropdown = ttk.Combobox(root, textvariable=nutrient_var)
nutrient_dropdown['values'] = ('Nitrogen', 'Phosphorus', 'Potassium')
nutrient_dropdown.grid(column=1, row=0)
nutrient_dropdown.current(0)

ttk.Label(root, text="Enter PPM:").grid(column=0, row=1, padx=10, pady=5, sticky='e')
ppm_entry = ttk.Entry(root)
ppm_entry.grid(column=1, row=1)

ttk.Label(root, text="Enter Area (ha):").grid(column=0, row=2, padx=10, pady=5, sticky='e')
area_entry = ttk.Entry(root)
area_entry.grid(column=1, row=2)

ttk.Label(root, text="Fertilizer Preference:").grid(column=0, row=3, padx=10, pady=5, sticky='e')
preference_var = tk.StringVar()
preference_dropdown = ttk.Combobox(root, textvariable=preference_var)
preference_dropdown['values'] = ('Natural', 'Synthetic')
preference_dropdown.grid(column=1, row=3)
preference_dropdown.current(0)

run_button = ttk.Button(root, text="Analyze", command=run_analysis)
run_button.grid(column=0, row=4, columnspan=2, pady=10)

result_label = ttk.Label(root, text="", justify="left", foreground="darkgreen")
result_label.grid(column=0, row=5, columnspan=2, padx=10, pady=10)

root.mainloop()
