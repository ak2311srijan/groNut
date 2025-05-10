# Soil Fertility Recommendation System Prototype (Python)

# --- MODULE 1: Conversion from PPM to kg/ha and lb/ha ---
def ppm_to_kg_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    """Convert PPM to kilograms per hectare."""
    return ppm * soil_depth_cm * bulk_density * 0.1

def ppm_to_lb_ha(ppm, soil_depth_cm=15, bulk_density=1.3):
    """Convert PPM to pounds per hectare."""
    kg_ha = ppm_to_kg_ha(ppm, soil_depth_cm, bulk_density)
    return kg_ha * 2.20462

# --- MODULE 2: Ideal Value Comparison ---
IDEAL_VALUES_KG_HA = {
    'nitrogen': 80,   # for example, 80 kg/ha is ideal for a crop
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
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pickle

# Sample training data (ppm, area in ha) and labels
# Label: 0 = Deficient, 1 = Optimal, 2 = Excessive
X_train = np.array([
    [20, 1], [50, 1], [90, 1],
    [30, 2], [80, 2], [110, 2],
    [40, 3], [70, 3], [130, 3]
])
y_train = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])

ml_model = DecisionTreeClassifier()
ml_model.fit(X_train, y_train)

STATUS_LABELS = {0: "Deficient", 1: "Optimal", 2: "Excessive"}

# --- EXAMPLE USAGE ---
import net_ppm
if __name__ == "__main__":
    nutrient = input("Enter nutrient (nitrogen/phosphorus/potassium): ").strip().lower()
    try:
        ppm = net_ppm.expected_avg_nitrogen_ppm
        area = float(input("Enter area in hectares: "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        exit()

    kg_ha = ppm_to_kg_ha(ppm)
    lb_ha = ppm_to_lb_ha(ppm)

    # ML prediction
    prediction = ml_model.predict([[ppm, area]])[0]
    status = STATUS_LABELS[prediction]

    # Fertilizer recommendation
    fertilizers = recommend_fertilizer(nutrient, 'natural')

    print(f"\n{nutrient.title()} - {ppm} ppm")
    print(f"Converted: {kg_ha:.2f} kg/ha, {lb_ha:.2f} lb/ha")
    print(f"Status (ML): {status}")
    print(f"Recommended Natural Fertilizers: {', '.join(fertilizers)}")
