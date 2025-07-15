import tkinter as tk
from tkinter import ttk

def create_report_tab(notebook):
    tab_report = tk.Frame(notebook)
    notebook.add(tab_report, text="Report Details")

    widgets = {}

    # File Location
    file_location_label = tk.Label(tab_report, text="File Location (optional):")
    file_location_label.pack(pady=(10, 0))

    file_location_entry = tk.Entry(tab_report, width=50)
    file_location_entry.pack(pady=(0, 10))
    widgets["file_location_entry"] = file_location_entry

    # Geometry File Name
    tk.Label(tab_report, text="Geometry File Name:").pack(pady=(10, 0))
    name_entry = tk.Entry(tab_report, width=30)
    name_entry.pack()
    widgets["name_entry"] = name_entry

    # Specific Gravity
    widgets["sg_var"] = tk.StringVar(value="Salt Water")
    sg_label_to_value = {
        "Fresh Water": "1.000",
        "Salt Water": "1.025"
    }
    widgets["sg_label_to_value"] = sg_label_to_value

    tk.Label(tab_report, text="Specific Gravity:").pack(pady=(10, 0))
    sg_dropdown = ttk.Combobox(tab_report, textvariable=widgets["sg_var"],
                                values=list(sg_label_to_value.keys()), state="readonly")
    sg_dropdown.pack()

    # Report Units
    tk.Label(tab_report, text="Report Units", font=("Arial", 10, "bold")).pack(pady=(20, 0))

    units_frame = tk.Frame(tab_report)
    units_frame.pack(pady=5)

    # Length
    tk.Label(units_frame, text="Length:").grid(row=0, column=0, padx=10)
    widgets["length_var"] = tk.StringVar(value="Feet")
    length_label_to_value = {
        "Feet": "F",
        "Meters": "M"
    }
    widgets["length_label_to_value"] = length_label_to_value

    length_dropdown = ttk.Combobox(units_frame, textvariable=widgets["length_var"],
                                   values=list(length_label_to_value.keys()), state="readonly", width=10)
    length_dropdown.grid(row=1, column=0, padx=10)

    # Weight
    tk.Label(units_frame, text="Weight:").grid(row=0, column=1, padx=10)
    widgets["weight_var"] = tk.StringVar(value="Long Tons")
    weight_label_to_value = {
        "Pounds": "LB",
        "Long Tons": "LT"
    }
    widgets["weight_label_to_value"] = weight_label_to_value

    weight_dropdown = ttk.Combobox(units_frame, textvariable=widgets["weight_var"],
                                   values=list(weight_label_to_value.keys()), state="readonly", width=10)
    weight_dropdown.grid(row=1, column=1, padx=10)

    # === Draft Locations ===
    tk.Label(tab_report, text="Draft Locations", font=("Arial", 10, "bold")).pack(pady=(20, 5))

    draft_frame = tk.Frame(tab_report)
    draft_frame.pack()

    tk.Label(draft_frame, text="Forward").grid(row=0, column=0, padx=10)
    tk.Label(draft_frame, text="Midships").grid(row=0, column=1, padx=10)
    tk.Label(draft_frame, text="Aft").grid(row=0, column=2, padx=10)

    widgets["fwd_draft_entry"] = tk.Entry(draft_frame, width=12)
    widgets["mid_draft_entry"] = tk.Entry(draft_frame, width=12)
    widgets["aft_draft_entry"] = tk.Entry(draft_frame, width=12)

    widgets["fwd_draft_entry"].grid(row=1, column=0, padx=10)
    widgets["mid_draft_entry"].grid(row=1, column=1, padx=10)
    widgets["aft_draft_entry"].grid(row=1, column=2, padx=10)

    return widgets
