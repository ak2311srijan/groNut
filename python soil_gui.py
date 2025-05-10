import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# ML Model
X_train = np.array([
    [20, 1], [50, 1], [90, 1],
    [30, 2], [80, 2], [110, 2],
    [40, 3], [70, 3], [130, 3]
])
y_train = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
ml_model = DecisionTreeClassifier()
ml_model.fit(X_train, y_train)

STATUS_LABELS = {0: "Deficient", 1: "Optimal", 2: "Excessive"}

def ppm_to_kg_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    return ppm * soil_depth_cm * bulk_density * 0.1

def ppm_to_lb_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    kg_ha = ppm_to_kg_ha(ppm, soil_depth_cm, bulk_density)
    return kg_ha * 2.20462

def run_analysis():
    try:
        area = float(area_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid area in hectares.")
        return

    ppm = 70  # Simulated value
    kg_ha = ppm_to_kg_ha(ppm)
    lb_ha = ppm_to_lb_ha(ppm)
    prediction = ml_model.predict([[ppm, area]])[0]
    status = STATUS_LABELS[prediction]

    report = (
        f"📊 Soil Fertility Report\n"
        f"-------------------------------\n"
        f"🔹 Area: {area} hectare\n"
        f"🔹 PPM (Simulated): {ppm} ppm\n"
        f"🔹 Converted: {kg_ha:.2f} kg/ha | {lb_ha:.2f} lb/ha\n"
        f"🔹 Status: {status}"
    )
    report_label.config(text=report)

root = tk.Tk()
root.title("🌾 Enhanced Soil Fertility System")
root.geometry("600x400")
root.configure(bg="#f0f8f5")

header = tk.Label(root, text="🌱 Soil Fertility Analyzer", font=("Helvetica", 18, "bold"),
                  bg="#4caf50", fg="white", pady=10)
header.pack(fill="x")

input_frame = tk.Frame(root, bg="#f0f8f5", pady=20)
input_frame.pack(padx=20, fill="x")

tk.Label(input_frame, text="Enter Area (in hectares):", font=("Segoe UI", 12), bg="#f0f8f5").grid(row=0, column=0, sticky='e')
area_entry = ttk.Entry(input_frame, width=30)
area_entry.grid(row=0, column=1, padx=10, pady=10)

analyze_btn = ttk.Button(input_frame, text="Run Analysis", command=run_analysis)
analyze_btn.grid(row=1, column=0, columnspan=2, pady=15)

report_frame = tk.LabelFrame(root, text="📝 Report", bg="white", padx=15, pady=15,
                             font=("Segoe UI", 12, "bold"), fg="#333")
report_frame.pack(padx=20, pady=10, fill="both", expand=True)

report_label = tk.Label(report_frame, text="", font=("Consolas", 11), bg="white", justify="left", anchor="nw")
report_label.pack(fill="both", expand=True)

root.mainloop()
