import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

# Load the template
def load_template():
    with open("ls_temp.txt", "r") as f:
        return f.read()

# content‑to‑percent for each macro tank stage
load_patterns = {
    "Departure": {"default": "MACRO TANK1",
                  "load": {"Gasoline":0.95, "Diesel":0.95, "Fresh Water":0.95, "Bait":0.95, "Sewage":0.10}},
    "Midway":    {"default": "MACRO TANK2",
                  "load": {"Gasoline":0.50, "Diesel":0.50, "Fresh Water":0.50, "Bait":0.50, "Sewage":0.50}},
    "Arrival":   {"default": "MACRO TANK3",
                  "load": {"Gasoline":0.10, "Diesel":0.10, "Fresh Water":0.10, "Bait":0.10, "Sewage":0.95}}
}


def generate_document():
    hull = name_entry.get().strip()
    sg_value = sg_label_to_value.get(sg_var.get(), "")
    unit_length = length_label_to_value.get(length_var.get(), "")
    unit_weight = weight_label_to_value.get(weight_var.get(), "")
    selected_label = route_var.get().strip()
    route_value = route_label_to_value.get(selected_label, "")
    fwd_draft = fwd_draft_entry.get().strip()
    mid_draft = mid_draft_entry.get().strip()
    aft_draft = aft_draft_entry.get().strip()
    global initial_weights, add_weights


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

    # Safe defaults in case there are no initial weights
    initial_wt_lcg = ""
    initial_wt_tcg = ""
    initial_wt_vcg = ""


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
        initial_wt_lcg = row["initial_wt_lcg"].get().strip()
        initial_wt_tcg = row["initial_wt_tcg"].get().strip()
        initial_wt_vcg = row["initial_wt_vcg"].get().strip()

        if not action or not item or not weight or not initial_wt_lcg or not initial_wt_tcg or not initial_wt_vcg or units not in grouped_by_units:
            continue

        # Negate weight for ADD, leave it for REMOVE
        try:
            weight_str = weight.strip()
            if action == "ADD":
                if not weight_str.startswith("-"):
                    weight_str = f"-{weight_str}"
            else:
                weight_str = weight_str.lstrip("-")
        except ValueError:
            continue  # skip invalid weight input

        grouped_by_units[units].append((item, weight_str, initial_wt_lcg, initial_wt_tcg, initial_wt_vcg))

    # Build output
    for unit, rows in grouped_by_units.items():
        if rows:
            initial_weights_block += f"UNITS {unit}\n"
            for item, weight, initial_wt_lcg, initial_wt_tcg, initial_wt_vcg in rows:
                initial_weights_block += f'ADD "{item}" {weight} {initial_wt_lcg} {initial_wt_tcg} {initial_wt_vcg}\n'

    # === Prepare Initial Tanks Block ===
    initial_tanks_block = ""

    for tank in initial_tanks:
        tank_name = tank["name"].get().strip()
        contents = tank["contents"].get().strip()
        sg = tank["sg"].get().strip()
        load = tank["load"].get().strip()

        initial_tanks_block += f"TANK {tank_name}\n"
        initial_tanks_block += f"CONTENTS {sg}\n"
        initial_tanks_block += f"LOAD ({tank_name}) {load}\n\n"

# === PASSENGER INFO ===
    paxct = pax_count_entry.get().strip()
    paxwt = pax_weight_entry.get().strip()
    paxlcg = pax_lcg_entry.get().strip()
    paxtcg = pax_tcg_entry.get().strip()
    paxvcg = pax_vcg_entry.get().strip()

    # === ADDITIONAL WEIGHTS BLOCK ===
    addstuff_block = ""
    grouped_add_by_units = {"LB": [], "LT": []}

    for row in add_weights:
        item = row["item"].get().strip()
        weight = row["weight"].get().strip()
        units = row["units"].get().strip().upper()
        lcg = row["lcg"].get().strip()
        tcg = row["tcg"].get().strip()
        vcg = row["vcg"].get().strip()

        if not item or not weight or not lcg or not tcg or not vcg or units not in grouped_add_by_units:
            continue

        try:
            weight_str = weight.strip()
        except ValueError:
            continue  # skip invalid

        grouped_add_by_units[units].append((item, weight_str, lcg, tcg, vcg))

    # Format grouped
    for unit, rows in grouped_add_by_units.items():
        if rows:
            addstuff_block += f"UNITS {unit}\n"
            for item, weight, lcg, tcg, vcg in rows:
                addstuff_block += f'ADD "{item}" {weight} {lcg} {tcg} {vcg}\n'

# === FSM Tanks List ===
    fsm_tanks_list = [
        t["name_widget"].get().strip()
        for t in load_tanks
        if t["name_widget"].get().strip()
    ]
    fsm_tanks = " ".join(fsm_tanks_list)

    # === Macro Tanks Sections ===
    macro_block = ""
    for stage in ["Departure", "Midway", "Arrival"]:
        info = load_patterns[stage]
        macro_block += f"`-----{stage} Tanks-----\n"
        macro_block += f"{info['default']}\n"
        macro_block += "`LOAD (TANK) %\n"
        # pair up name widgets and contents
        for t in load_tanks:
            name = t["name_widget"].get().strip()
            contents = t["contents_var"].get()
            pct = info["load"][contents]
            macro_block += f"LOAD ({name}) {pct}\n"
        macro_block += "/\n"

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
            .replace("{{fwddrloc}}", fwd_draft)
            .replace("{{middrloc}}", mid_draft)
            .replace("{{aftdrloc}}", aft_draft)
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
            .replace("{{initial_wt_lcg}}", initial_wt_lcg)
            .replace("{{initial_wt_tcg}}", initial_wt_tcg)
            .replace("{{initial_wt_vcg}}", initial_wt_vcg)
            .replace("{{initial_weights}}", initial_weights_block.strip())
            .replace("{{initial_tanks}}", initial_tanks_block.strip())
            .replace("{{paxct}}", paxct)
            .replace("{{paxwt}}", paxwt)
            .replace("{{paxlcg}}", paxlcg)
            .replace("{{paxtcg}}", paxtcg)
            .replace("{{paxvcg}}", paxvcg)
            .replace("{{addstuff}}", addstuff_block.strip())
            .replace("{{fsm_tanks}}", fsm_tanks)
            .replace("{{tank_macros}}", macro_block)
        )



        output_path = os.path.join(output_dir, output_file)
        with open(output_path, "w") as f:
            f.write(filled_text)

    messagebox.showinfo("Success", f"All files saved in:\n{output_dir}")
    root.destroy()

initial_weights = []
add_weights = []
fsm_tanks_list = []


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

# Report Units
tk.Label(tab_report, text="Report Units", font=("Arial", 10, "bold")).pack(pady=(20, 0))

units_frame = tk.Frame(tab_report)
units_frame.pack(pady=5)

# Length Units
tk.Label(units_frame, text="Length:").grid(row=0, column=0, padx=10)
length_var = tk.StringVar(value="Feet")
length_label_to_value = {
    "Feet": "F",
    "Meters": "M"
}
length_dropdown = ttk.Combobox(units_frame, textvariable=length_var, values=list(length_label_to_value.keys()), state="readonly", width=10)
length_dropdown.grid(row=1, column=0, padx=10)

# Weight Units
tk.Label(units_frame, text="Weight:").grid(row=0, column=1, padx=10)
weight_var = tk.StringVar(value="Long Tons")
weight_label_to_value = {
    "Pounds": "LB",
    "Long Tons": "LT"
}
weight_dropdown = ttk.Combobox(units_frame, textvariable=weight_var, values=list(weight_label_to_value.keys()), state="readonly", width=10)
weight_dropdown.grid(row=1, column=1, padx=10)


# === DRAFT LOCATIONS ===
tk.Label(tab_report, text="Draft Locations", font=("Arial", 10, "bold")).pack(pady=(20, 5))

draft_frame = tk.Frame(tab_report)
draft_frame.pack()

tk.Label(draft_frame, text="Forward").grid(row=0, column=0, padx=10)
tk.Label(draft_frame, text="Midships").grid(row=0, column=1, padx=10)
tk.Label(draft_frame, text="Aft").grid(row=0, column=2, padx=10)

fwd_draft_entry = tk.Entry(draft_frame, width=12)
mid_draft_entry = tk.Entry(draft_frame, width=12)
aft_draft_entry = tk.Entry(draft_frame, width=12)

fwd_draft_entry.grid(row=1, column=0, padx=10)
mid_draft_entry.grid(row=1, column=1, padx=10)
aft_draft_entry.grid(row=1, column=2, padx=10)


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
        "initial_wt_lcg": tk.Entry(weights_frame, width=8),
        "initial_wt_tcg": tk.Entry(weights_frame, width=8),
        "initial_wt_vcg": tk.Entry(weights_frame, width=8)
    }
    row_data["action"].set("ADD")
    row_data["units"].set("LB")

    row_data["action"].grid(row=row_idx, column=0, padx=2)
    row_data["item"].grid(row=row_idx, column=1, padx=2)
    row_data["weight"].grid(row=row_idx, column=2, padx=2)
    row_data["units"].grid(row=row_idx, column=3, padx=2)
    row_data["initial_wt_lcg"].grid(row=row_idx, column=4, padx=2)
    row_data["initial_wt_tcg"].grid(row=row_idx, column=5, padx=2)
    row_data["initial_wt_vcg"].grid(row=row_idx, column=6, padx=2)

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

# === INITIAL TANKS ===
# Content types and their default specific gravity
contents_to_sg = {
    "Gasoline": "0.74",
    "Fresh Water": "1.00",
    "Sewage": "1.025",
    "Diesel": "0.85",
    "Bait": "1.025"
}


initial_tanks = []
tank_header_created = False
ltsh_tanks_frame = tk.Frame(tab_lightship)
ltsh_tanks_frame.pack(pady=(20, 0))

def reposition_ltsh_tank_button():
    row_idx = len(initial_tanks) + 1
    ltsh_tank_button.grid_forget()
    ltsh_tank_button.grid(row=row_idx, column=0, columnspan=4, pady=5)

def ltsh_add_tank_row():
    global tank_header_created

    if not tank_header_created:
        header = ["Tank Name", "Contents", "Specific Gravity", "Load"]
        for col, label in enumerate(header):
            tk.Label(ltsh_tanks_frame, text=label, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
        tank_header_created = True

    row_idx = len(initial_tanks) + 1

    name_entry = tk.Entry(ltsh_tanks_frame, width=15)
    contents_var = tk.StringVar()
    contents_dropdown = ttk.Combobox(ltsh_tanks_frame, textvariable=contents_var,
                                     values=list(contents_to_sg.keys()) + ["Other"], state="readonly", width=12)
    sg_entry = tk.Entry(ltsh_tanks_frame, width=10)
    load_entry = tk.Entry(ltsh_tanks_frame, width=10)

    def on_contents_change(*args):
        selected = contents_var.get()
        if selected in contents_to_sg:
            sg_entry.config(state="normal")  # Temporarily enable to update text
            sg_entry.delete(0, tk.END)
            sg_entry.insert(0, contents_to_sg[selected])
            sg_entry.config(state="disabled")  # Lock it again
        else:
            sg_entry.config(state="normal")  # Allow manual entry

    contents_var.trace_add("write", on_contents_change)
    contents_var.set("Gasoline")

    name_entry.grid(row=row_idx, column=0, padx=2)
    contents_dropdown.grid(row=row_idx, column=1, padx=2)
    sg_entry.grid(row=row_idx, column=2, padx=2)
    load_entry.grid(row=row_idx, column=3, padx=2)

    def delete_tank_row():
        for widget in (name_entry, contents_dropdown, sg_entry, load_entry, delete_btn):
            widget.grid_forget()
        initial_tanks.remove(row_data)
        reposition_ltsh_tank_button()

    delete_btn = tk.Button(ltsh_tanks_frame, text="❌", command=delete_tank_row, fg="red")
    delete_btn.grid(row=row_idx, column=4, padx=2)

    row_data = {
        "name": name_entry,
        "contents": contents_var,
        "sg": sg_entry,
        "load": load_entry,
        "delete_btn": delete_btn
    }

    initial_tanks.append(row_data)
    reposition_ltsh_tank_button()


ltsh_tank_button = tk.Button(ltsh_tanks_frame, text="➕ Add Initial Tank", command=ltsh_add_tank_row)
ltsh_tank_button.grid(row=1, column=0, columnspan=4, pady=5)



# === TAB 3: Loads ===
tab_loads = tk.Frame(notebook)
notebook.add(tab_loads, text="Loads")

# === PASSENGERS SECTION ===
tk.Label(tab_loads, text="Passengers:", font=("Arial", 10, "bold")).pack(pady=(20, 5))

# Number of Passengers
tk.Label(tab_loads, text="Number of Passengers:").pack()
pax_count_entry = tk.Entry(tab_loads, width=10)
pax_count_entry.pack()

# Passenger Weight
tk.Label(tab_loads, text="Weight per Passenger (lbs):").pack()
pax_weight_entry = tk.Entry(tab_loads, width=10)
pax_weight_entry.insert(0, "185")
pax_weight_entry.pack()

# Passenger Location (LCG, TCG, VCG)
tk.Label(tab_loads, text="Passenger Location:").pack(pady=(10, 0))
pax_loc_frame = tk.Frame(tab_loads)
pax_loc_frame.pack(pady=(0, 10))

tk.Label(pax_loc_frame, text="LCG").grid(row=0, column=0, padx=10)
tk.Label(pax_loc_frame, text="TCG").grid(row=0, column=1, padx=10)
tk.Label(pax_loc_frame, text="VCG").grid(row=0, column=2, padx=10)

pax_lcg_entry = tk.Entry(pax_loc_frame, width=10)
pax_tcg_entry = tk.Entry(pax_loc_frame, width=10)
pax_vcg_entry = tk.Entry(pax_loc_frame, width=10)

pax_lcg_entry.grid(row=1, column=0, padx=10)
pax_tcg_entry.grid(row=1, column=1, padx=10)
pax_vcg_entry.grid(row=1, column=2, padx=10)


# === ADDITIONAL WEIGHTS SECTION ===
tk.Label(tab_loads, text="Additional Weights in Every Loadcase:", font=("Arial", 10, "bold")).pack(pady=(20, 5))

add_weights_frame = tk.Frame(tab_loads)
add_weights_frame.pack()

add_header_created = False

def reposition_add_load_button():
    row_idx = len(add_weights) + 1
    add_load_button.grid_forget()
    add_load_button.grid(row=row_idx, column=0, columnspan=6, pady=5)

def add_load_row():
    global add_header_created

    if not add_header_created:
        headers = ["Item Name", "Weight", "Units", "LCG", "TCG", "VCG"]
        for col, label in enumerate(headers):
            tk.Label(add_weights_frame, text=label, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
        add_header_created = True

    row_idx = len(add_weights) + 1

    row_data = {
        "item": tk.Entry(add_weights_frame, width=12),
        "weight": tk.Entry(add_weights_frame, width=8),
        "units": ttk.Combobox(add_weights_frame, values=["LB", "LT"], width=6, state="readonly"),
        "lcg": tk.Entry(add_weights_frame, width=8),
        "tcg": tk.Entry(add_weights_frame, width=8),
        "vcg": tk.Entry(add_weights_frame, width=8)
    }
    row_data["units"].set("LT")

    row_data["item"].grid(row=row_idx, column=0, padx=2)
    row_data["weight"].grid(row=row_idx, column=1, padx=2)
    row_data["units"].grid(row=row_idx, column=2, padx=2)
    row_data["lcg"].grid(row=row_idx, column=3, padx=2)
    row_data["tcg"].grid(row=row_idx, column=4, padx=2)
    row_data["vcg"].grid(row=row_idx, column=5, padx=2)

    def delete_load_row():
        for widget in row_data.values():
            widget.grid_forget()
        delete_btn.grid_forget()
        add_weights.remove(row_data)
        reposition_add_load_button()

    delete_btn = tk.Button(add_weights_frame, text="❌", command=delete_load_row, fg="red")
    delete_btn.grid(row=row_idx, column=6, padx=2)
    row_data["delete_btn"] = delete_btn

    add_weights.append(row_data)
    reposition_add_load_button()

add_load_button = tk.Button(add_weights_frame, text="➕ Add Weight", command=add_load_row)
add_load_button.grid(row=1, column=0, columnspan=6, pady=5)

# === TANKS SECTION ===
tk.Label(tab_loads, text="Tanks:", font=("Arial",10,"bold")).pack(pady=(20,5))
load_tanks_frame = tk.Frame(tab_loads)
load_tanks_frame.pack()

load_tanks = []
fsm_tanks_list = []

def reposition_load_tank_button():
    idx = len(load_tanks) + 1
    load_tank_button.grid_forget()
    load_tank_button.grid(row=idx, column=0, columnspan=2, pady=5)

def load_add_tank_row():
    if len(load_tanks) == 0:
        tk.Label(load_tanks_frame, text="Name",    font=("Arial",10,"bold")).grid(row=0, column=0, padx=5)
        tk.Label(load_tanks_frame, text="Contents",font=("Arial",10,"bold")).grid(row=0, column=1, padx=5)

    row = len(load_tanks) + 1
    name_ent = tk.Entry(load_tanks_frame, width=15)
    contents_var = tk.StringVar(value="Gasoline")
    contents_dd  = ttk.Combobox(
        load_tanks_frame, textvariable=contents_var,
        values=["Gasoline","Diesel","Fresh Water","Sewage","Bait"],
        state="readonly", width=12
    )

    name_ent.grid(row=row, column=0, padx=5)
    contents_dd.grid(row=row, column=1, padx=5)

    def delete_tank():
        name_ent.grid_forget()
        contents_dd.grid_forget()
        delete_btn.grid_forget()
        # find and remove
        for i, t in enumerate(load_tanks):
            if t["name_widget"] is name_ent:
                load_tanks.pop(i)
                fsm_tanks_list.pop(i)
                break
        reposition_load_tank_button()

    delete_btn = tk.Button(load_tanks_frame, text="❌", command=delete_tank, fg="red")
    delete_btn.grid(row=row, column=2, padx=5)

    load_tanks.append({"name_widget": name_ent, "contents_var": contents_var})
    fsm_tanks_list.append(name_ent.get().strip() or f"TANK{row}")
    reposition_load_tank_button()

load_tank_button = tk.Button(load_tanks_frame, text="➕ Add Tank", command=load_add_tank_row)
load_tank_button.grid(row=1, column=0, columnspan=2, pady=5)

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
