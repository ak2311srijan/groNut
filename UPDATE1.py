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

    report_text = (
        f"📌 Soil Nutrient Report\n"
        f"---------------------------\n"
        f"🔸 Nutrient: {nutrient.title()}\n"
        f"🔸 PPM Value: {ppm} ppm\n"
        f"🔸 Area: {area} hectare\n\n"
        f"📈 Converted Values:\n"
        f"   ➤ {kg_ha:.2f} kg/ha\n"
        f"   ➤ {lb_ha:.2f} lb/ha\n\n"
        f"📊 Fertility Status: {status}\n\n"
        f"🌱 Recommended ({preference.title()}) Fertilizers:\n"
        f"   ➤ " + (", ".join(fertilizers) if fertilizers else "No recommendations found")
    )

    report_label.config(text=report_text)

# --- Main Window ---
root = tk.Tk()
root.title("🌾 Soil Fertility Recommendation System")
root.geometry("600x500")
root.resizable(False, False)

style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
style.configure("TCombobox", padding=4)

# --- Input Frame ---
input_frame = ttk.LabelFrame(root, text="Input Section", padding=15)
input_frame.pack(padx=20, pady=15, fill="x")

ttk.Label(input_frame, text="Select Nutrient:").grid(row=0, column=0, sticky='e', pady=5)
nutrient_var = tk.StringVar()
nutrient_dropdown = ttk.Combobox(input_frame, textvariable=nutrient_var, width=25)
nutrient_dropdown['values'] = ('Nitrogen', 'Phosphorus', 'Potassium')
nutrient_dropdown.grid(row=0, column=1, pady=5)
nutrient_dropdown.current(0)

ttk.Label(input_frame, text="Enter PPM:").grid(row=1, column=0, sticky='e', pady=5)
ppm_entry = ttk.Entry(input_frame, width=28)
ppm_entry.grid(row=1, column=1, pady=5)

ttk.Label(input_frame, text="Enter Area (ha):").grid(row=2, column=0, sticky='e', pady=5)
area_entry = ttk.Entry(input_frame, width=28)
area_entry.grid(row=2, column=1, pady=5)

ttk.Label(input_frame, text="Fertilizer Type:").grid(row=3, column=0, sticky='e', pady=5)
preference_var = tk.StringVar()
preference_dropdown = ttk.Combobox(input_frame, textvariable=preference_var, width=25)
preference_dropdown['values'] = ('Natural', 'Synthetic')
preference_dropdown.grid(row=3, column=1, pady=5)
preference_dropdown.current(0)

ttk.Button(input_frame, text="Generate Report", command=run_analysis).grid(row=4, column=0, columnspan=2, pady=15)

# --- Report Frame ---
report_frame = ttk.LabelFrame(root, text="📄 Report", padding=15)
report_frame.pack(padx=20, pady=10, fill="both", expand=True)

report_label = ttk.Label(report_frame, text="", font=("Segoe UI", 10), justify="left", anchor="w")
report_label.pack(fill="both", expand=True)

root.mainloop()
