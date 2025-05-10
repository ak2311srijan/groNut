import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.tree import DecisionTreeClassifier

# --- ML Model Training ---
X_train = np.array([
    [20, 1], [50, 1], [90, 1],
    [30, 2], [80, 2], [110, 2],
    [40, 3], [70, 3], [130, 3]
])
y_train = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])

ml_model = DecisionTreeClassifier()
ml_model.fit(X_train, y_train)

STATUS_LABELS = {0: "Deficient", 1: "Optimal", 2: "Excessive"}

# Conversion Functions
def ppm_to_kg_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    return ppm * soil_depth_cm * bulk_density * 0.1

def ppm_to_lb_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    kg_ha = ppm_to_kg_ha(ppm, soil_depth_cm, bulk_density)
    return kg_ha * 2.20462

# GUI Function
def run_analysis():
    try:
        area = float(area_entry.get())
        ppm = 70  # Simulated fixed PPM value
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid numeric area value.")
        return

    kg_ha = ppm_to_kg_ha(ppm)
    lb_ha = ppm_to_lb_ha(ppm)
    prediction = ml_model.predict([[ppm, area]])[0]
    status = STATUS_LABELS[prediction]

    report_text = (
        f"🧪 Soil Fertility Report\n"
        f"-----------------------------\n"
        f"🔸 PPM (Simulated): {ppm} ppm\n"
        f"🔸 Area: {area} hectare\n\n"
        f"📊 Converted:\n"
        f"   ➤ {kg_ha:.2f} kg/ha\n"
        f"   ➤ {lb_ha:.2f} lb/ha\n\n"
        f"🌱 Fertility Status: {status}"
    )

    report_label.config(text=report_text)

# GUI Setup
root = tk.Tk()
root.title("🌿 Advanced Soil Fertility System")
root.geometry("650x450")
root.configure(bg="#ecf7f3")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Helvetica", 12), background="#ecf7f3")
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=8)
style.configure("TEntry", padding=6)

title = tk.Label(root, text="🌾 Soil Fertility Recommendation System", font=("Helvetica", 18, "bold"),
                 bg="#4caf50", fg="white", pady=10)
title.pack(fill="x")

input_frame = tk.Frame(root, bg="#ecf7f3", pady=20)
input_frame.pack(padx=20, fill="x")

tk.Label(input_frame, text="Enter Area (in hectares):", bg="#ecf7f3", font=("Helvetica", 13)).grid(row=0, column=0, sticky='e')
area_entry = ttk.Entry(input_frame, width=30)
area_entry.grid(row=0, column=1, padx=10, pady=10)

ttk.Button(input_frame, text="Analyze", command=run_analysis).grid(row=1, column=0, columnspan=2, pady=15)

report_frame = tk.LabelFrame(root, text="📄 Report", bg="#ffffff", font=("Helvetica", 13, "bold"), padx=15, pady=15)
report_frame.pack(padx=20, pady=10, fill="both", expand=True)

report_label = tk.Label(report_frame, text="", font=("Consolas", 11), justify="left", anchor="nw", bg="white")
report_label.pack(fill="both", expand=True)

root.mainloop()
