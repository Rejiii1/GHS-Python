import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# Load the template
def load_template():
    with open("ls_temp.txt", "r") as f:
        return f.read()

def generate_document():
    hull = name_entry.get().strip()
    sg_value = sg_label_to_value.get(sg_var.get(), "")
    unit_length = length_label_to_value.get(length_var.get(), "")
    unit_weight = weight_label_to_value.get(weight_var.get(), "")
    selected_label = route_var.get().strip()
    route_value = route_label_to_value.get(selected_label, "")
    
    vessel_label = vessel_var.get().strip()
    vessel_value = vessel_label_to_value.get(vessel_label, "")

    survey_label = survey_var.get().strip()
    survey_value = survey_label_to_value.get(survey_label, "")

    if not hull or not route_value or not vessel_value or not survey_value:
        messagebox.showwarning("Missing info", "Please fill in all fields and select valid options.")
        return

    # These will be optionally filled
    excel_data = ""
    vert_value = "1"
    gmmt_value = "1"
    disp = ltsh_lcg = ltsh_tcg = ltsh_vcg = ""
    lcg = tcg = vcg = ""

    if survey_label in ["Deadweight Survey", "Inclining Experiment"]:
        excel_data = excel_text.get("1.0", tk.END).strip()

    if survey_label == "Deadweight Survey":
        vert_value = vert_entry.get().strip()

    if survey_label == "Inclining Experiment":
        gmmt_value = gmmt_entry.get().strip()

    if survey_label == "User Defined Lightship":
        disp = disp_entry.get().strip()
        ltsh_lcg = ltsh_lcg_entry.get().strip()
        ltsh_tcg = ltsh_tcg_entry.get().strip()
        ltsh_vcg = ltsh_vcg_entry.get().strip()

    unit_value = f"UNITS {unit_var.get()}" if survey_label == "User Defined Lightship" else ""


    output_dir = os.path.join(os.getcwd(), "generated")
    os.makedirs(output_dir, exist_ok=True)

# Prepare the initial weights block
    initial_weights_block = ""
    grouped_by_units = {"LB": [], "LT": []}

    for row in initial_weights:
        action = row["action"].get().strip().upper()
        item = row["item"].get().strip()
        weight = row["weight"].get().strip()
        units = row["units"].get().strip().upper()
        lcg = row["lcg"].get().strip()
        tcg = row["tcg"].get().strip()
        vcg = row["vcg"].get().strip()

        if not action or not item or not weight or not lcg or not tcg or not vcg or units not in grouped_by_units:
            continue

        # Negate weight for ADD, leave it for REMOVE
        try:
            weight_value = float(weight)
            if action == "ADD":
                weight_value = -abs(weight_value)
            else:
                weight_value = abs(weight_value)
            weight_str = f"{weight_value:.2f}"
        except ValueError:
            continue  # skip invalid weight input

        grouped_by_units[units].append((item, weight_str, lcg, tcg, vcg))

    # Build output
    for unit, rows in grouped_by_units.items():
        if rows:
            initial_weights_block += f"UNITS {unit}\n"
            for item, weight, lcg, tcg, vcg in rows:
                initial_weights_block += f'ADD "{item}" {weight} {lcg} {tcg} {vcg}\n'




    # Define your templates and output filenames
    templates = {
        "ls_temp.txt": "ls.rf",
        "load_temp.txt": "load.rf",
        "int_temp.txt": "int.rf",
        "dam_temp.txt": "dam.rf"
    }

    for template_file, output_file in templates.items():
        try:
            with open(template_file, "r") as f:
                template = f.read()
        except FileNotFoundError:
            messagebox.showerror("Template Error", f"Template not found: {template_file}")
            continue

        filled_text = (
            template
            .replace("{{hull}}", hull)
            .replace("{{sg}}", sg_value)
            .replace("{{unit_length}}", unit_length)
            .replace("{{unit_weight}}", unit_weight)
            .replace("{{route}}", route_value)
            .replace("{{vessel}}", vessel_value)
            .replace("{{option}}", survey_value)
            .replace("{{excel_paste}}", excel_data)
            .replace("{{vert}}", vert_value)
            .replace("{{gmmt}}", gmmt_value)
            .replace("{{disp}}", f"WEIGHT {disp}" if disp else "")
            .replace("{{user_lightship_units}}", unit_value)
            .replace("{{ltsh_lcg}}", ltsh_lcg)
            .replace("{{ltsh_tcg}}", ltsh_tcg)
            .replace("{{ltsh_vcg}}", ltsh_vcg)
            .replace("{{lcg}}", lcg)
            .replace("{{tcg}}", tcg)
            .replace("{{vcg}}", vcg)
            .replace("{{initial_weights}}", initial_weights_block.strip())
        )



        output_path = os.path.join(output_dir, output_file)
        with open(output_path, "w") as f:
            f.write(filled_text)

    messagebox.showinfo("Success", f"All files saved in:\n{output_dir}")
    root.destroy()

initial_weights = []


# GUI setup
# === SETUP ROOT ===
root = tk.Tk()
root.title("GHS Run File Creator")
root.geometry("600x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# === TAB 1: Report Details ===
tab_report = tk.Frame(notebook)
notebook.add(tab_report, text="Report Details")

# Geometry File Name
tk.Label(tab_report, text="Geometry File Name:").pack(pady=(10, 0))
name_entry = tk.Entry(tab_report, width=40)
name_entry.pack()

# Specific Gravity
sg_var = tk.StringVar(value="Salt Water")
sg_label_to_value = {
    "Fresh Water": "1.000",
    "Salt Water": "1.025"
}
tk.Label(tab_report, text="Specific Gravity:").pack(pady=(10, 0))
sg_dropdown = ttk.Combobox(tab_report, textvariable=sg_var, values=list(sg_label_to_value.keys()), state="readonly")
sg_dropdown.pack()

# Length Units
length_var = tk.StringVar(value="Feet")
length_label_to_value = {
    "Feet": "F",
    "Meters": "M"
}
tk.Label(tab_report, text="Length Units:").pack(pady=(10, 0))
length_dropdown = ttk.Combobox(tab_report, textvariable=length_var, values=list(length_label_to_value.keys()), state="readonly")
length_dropdown.pack()

# Weight Units
weight_var = tk.StringVar(value="Long Tons")
weight_label_to_value = {
    "Pounds": "LB",
    "Long Tons": "LT"
}
tk.Label(tab_report, text="Weight Units:").pack(pady=(10, 0))
weight_dropdown = ttk.Combobox(tab_report, textvariable=weight_var, values=list(weight_label_to_value.keys()), state="readonly")
weight_dropdown.pack()

# === TAB 2: Lightship ===
tab_lightship = tk.Frame(notebook)
notebook.add(tab_lightship, text="Lightship")

survey_var = tk.StringVar(value="Select a survey type")
survey_label_to_value = {
    "Deadweight Survey": "1",
    "Inclining Experiment": "2",
    "User Defined Lightship": "3"
}
survey_options = list(survey_label_to_value.keys())

survey_dropdown = ttk.Combobox(tab_lightship, textvariable=survey_var, values=survey_options, state="readonly")
tk.Label(tab_lightship, text="Survey Type:").pack(pady=(10, 0))
survey_dropdown.pack()

# === DYNAMIC SURVEY FIELDS ===
dynamic_frame = tk.Frame(tab_lightship)
dynamic_frame.pack(pady=10)

def update_dynamic_fields(*args):
    for widget in dynamic_frame.winfo_children():
        widget.destroy()

    selection = survey_var.get()
    if selection in ["Deadweight Survey", "Inclining Experiment"]:
        global excel_text
        tk.Label(dynamic_frame, text="Paste Excel Data:").pack()
        excel_text = tk.Text(dynamic_frame, height=6, width=40)
        excel_text.pack()

        if selection == "Deadweight Survey":
            global vert_entry
            tk.Label(dynamic_frame, text="Conservative VCG:").pack()
            vert_entry = tk.Entry(dynamic_frame, width=20)
            vert_entry.pack()

        if selection == "Inclining Experiment":
            global gmmt_entry
            tk.Label(dynamic_frame, text="a from MOMTAN (ft-LT):").pack()
            gmmt_entry = tk.Entry(dynamic_frame, width=20)
            gmmt_entry.pack()

    elif selection == "User Defined Lightship":
        global disp_entry, ltsh_lcg_entry, ltsh_tcg_entry, ltsh_vcg_entry, unit_var
        entry_frame = tk.Frame(dynamic_frame)
        entry_frame.pack()

        unit_var = tk.StringVar(value="LB")

        tk.Label(entry_frame, text="Displacement").grid(row=0, column=0)
        tk.Label(entry_frame, text="Units").grid(row=0, column=1)
        tk.Label(entry_frame, text="LCG").grid(row=0, column=2)
        tk.Label(entry_frame, text="TCG").grid(row=0, column=3)
        tk.Label(entry_frame, text="VCG").grid(row=0, column=4)

        disp_entry = tk.Entry(entry_frame, width=10)
        unit_dropdown = ttk.Combobox(entry_frame, textvariable=unit_var, values=["LB", "LT"], state="readonly", width=6)
        ltsh_lcg_entry = tk.Entry(entry_frame, width=10)
        ltsh_tcg_entry = tk.Entry(entry_frame, width=10)
        ltsh_vcg_entry = tk.Entry(entry_frame, width=10)

        disp_entry.grid(row=1, column=0)
        unit_dropdown.grid(row=1, column=1)
        ltsh_lcg_entry.grid(row=1, column=2)
        ltsh_tcg_entry.grid(row=1, column=3)
        ltsh_vcg_entry.grid(row=1, column=4)

survey_var.trace_add("write", update_dynamic_fields)

# === INITIAL WEIGHTS ===
initial_weights = []
header_created = False
weights_frame = tk.Frame(tab_lightship)
weights_frame.pack()

def reposition_add_button():
    row_idx = len(initial_weights) + 1
    add_button.grid_forget()
    add_button.grid(row=row_idx, column=0, columnspan=8, pady=5)

def add_weight_row():
    global header_created

    if not header_created:
        header = ["Action", "Item Name", "Weight", "Units", "LCG", "TCG", "VCG", ""]
        for col, label in enumerate(header):
            tk.Label(weights_frame, text=label, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
        header_created = True

    row_idx = len(initial_weights) + 1

    row_data = {
        "action": ttk.Combobox(weights_frame, values=["ADD", "REMOVE"], width=6, state="readonly"),
        "item": tk.Entry(weights_frame, width=12),
        "weight": tk.Entry(weights_frame, width=8),
        "units": ttk.Combobox(weights_frame, values=["LB", "LT"], width=6, state="readonly"),
        "lcg": tk.Entry(weights_frame, width=8),
        "tcg": tk.Entry(weights_frame, width=8),
        "vcg": tk.Entry(weights_frame, width=8)
    }
    row_data["action"].set("ADD")
    row_data["units"].set("LB")

    row_data["action"].grid(row=row_idx, column=0, padx=2)
    row_data["item"].grid(row=row_idx, column=1, padx=2)
    row_data["weight"].grid(row=row_idx, column=2, padx=2)
    row_data["units"].grid(row=row_idx, column=3, padx=2)
    row_data["lcg"].grid(row=row_idx, column=4, padx=2)
    row_data["tcg"].grid(row=row_idx, column=5, padx=2)
    row_data["vcg"].grid(row=row_idx, column=6, padx=2)

    def delete_row():
        for widget in row_data.values():
            widget.grid_forget()
        delete_btn.grid_forget()
        initial_weights.remove(row_data)
        reposition_add_button()

    delete_btn = tk.Button(weights_frame, text="❌", command=delete_row, fg="red")
    delete_btn.grid(row=row_idx, column=7, padx=2)
    row_data["delete_btn"] = delete_btn

    initial_weights.append(row_data)
    reposition_add_button()

add_button = tk.Button(weights_frame, text="➕ Add Initial Weight", command=add_weight_row)
add_button.grid(row=1, column=0, columnspan=8, pady=5)

# === TAB 3: Loads ===
tab_loads = tk.Frame(notebook)
notebook.add(tab_loads, text="Loads")
tk.Label(tab_loads, text="Loads tab content TBD").pack(pady=20)

# === TAB 4: Intact Stability ===
tab_stab = tk.Frame(notebook)
notebook.add(tab_stab, text="Intact Stability")

vessel_var = tk.StringVar(value="Select a vessel type")
vessel_label_to_value = {
    "Power Boat": "POWER",
    "Pontoon Boat": "PONTOON",
    "RHIB": "RHIB",
    "Monohull Sailboat": "MONOSAIL",
    "Catamaran Sailboat": "CATSAIL"
}
tk.Label(tab_stab, text="Vessel Type:").pack(pady=(10, 0))
ttk.Combobox(tab_stab, textvariable=vessel_var, values=list(vessel_label_to_value.keys()), state="readonly").pack()

route_var = tk.StringVar(value="Select a route")
route_label_to_value = {
    "Protected Waters": "PROTECT",
    "Partially Protected Waters": "PARTIAL",
    "Exposed Waters": "EXPOSED"
}
tk.Label(tab_stab, text="Route:").pack(pady=(10, 0))
ttk.Combobox(tab_stab, textvariable=route_var, values=list(route_label_to_value.keys()), state="readonly").pack()

# === Bottom Button ===
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x")
tk.Button(bottom_frame, text="Generate Run Files", command=generate_document).pack(pady=10)


# Start GUI
root.mainloop()
