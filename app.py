import customtkinter as ctk
import tkinter as tk
import pickle
import numpy as np
import os
# Load trained model
#model = pickle.load(open("diabetes_model.pkl", "rb"))
file_path=os.path.join(os.path.dirname(__file__), "diabetes_model.pkl")
model = pickle.load(open(file_path, "rb"))

# App configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Diabetes Prediction System")
app.geometry("450x550")

# Heading
title = ctk.CTkLabel(
    app, text="Diabetes Prediction", font=("Arial", 24, "bold")
)
title.pack(pady=20)

# Input fields
entries = []

labels = [
    "Pregnancies",
    "Glucose",
    "Blood Pressure",
    "Skin Thickness",
    "Insulin",
    "BMI",
    "Diabetes Pedigree",
    "Age"
]

for label in labels:
    lbl = ctk.CTkLabel(app, text=label)
    lbl.pack()
    entry = ctk.CTkEntry(app)
    entry.pack(pady=5)
    entries.append(entry)

# Result label
result_label = ctk.CTkLabel(app, text="", font=("Arial", 16))
result_label.pack(pady=20)

# Prediction function
def predict_diabetes():
    try:
        values = [float(entry.get()) for entry in entries]
        values = np.array(values).reshape(1, -1)

        prediction = model.predict(values)

        if prediction[0] == 1:
            result_label.configure(
                text="⚠️ Person is Diabetic",
                text_color="red"
            )
        else:
            result_label.configure(
                text="✅ Person is NOT Diabetic",
                text_color="green"
            )
    except:
        result_label.configure(
            text="❌ Please enter valid inputs",
            text_color="yellow"
        )

# Predict button
predict_btn = ctk.CTkButton(
    app, text="Predict", command=predict_diabetes
)
predict_btn.pack(pady=20)

app.mainloop()
