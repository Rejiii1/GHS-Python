#   GHS Stability Generator
#   A tool to generate GHS run files for stability analysis
#   Version: 1.0.1
#   Updated: 07-14-2025
#   Created by: Trip Jackson

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os


#GUI
#tabs
from tab_damage import create_damage_tab



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
    beam = beam_entry.get().strip()
    length = length_entry.get().strip()

    if not tank_model_var.get():
        notanksfs = fs_entry.get().strip()
    else:
        notanksfs = "0"


    if not profile_var.get():
        wind_area = wind_area_entry.get().strip()
        wind_arm  = wind_arm_entry.get().strip()
    else:
        wind_area = "0"
        wind_arm  = "0"

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


    custom_path = file_location_entry.get().strip()
    if custom_path:
        output_dir = custom_path
    else:
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

    # === CRITICAL POINTS BLOCK ===
    crit_block = ""
    for er in critical_points:
        num   = er["num_lbl"].cget("text")
        name  = er["name_ent"].get().strip()
        lon   = er["long_ent"].get().strip()
        tra   = er["trans_ent"].get().strip()
        ver   = er["vert_ent"].get().strip()
        if not name or not lon or not tra or not ver:
            continue
        crit_block += f'CRIT ({num}) "{name}" {lon} {tra} {ver}/flood/symmetrical\n'

    # --- PONTOON-SPECIFIC DATA EXTRACTION (DO THIS ONCE, BEFORE THE TEMPLATE LOOP) ---
    pontoon_replacements = {}
    head_lcg_val = ""
    head_tcg_val = ""

    if pontoon_tab: # Check if pontoon_tab exists
        for table in (pontoon_tab.crowd2, pontoon_tab.crowd5):
            for row in table:
                code     = row["code"]                    # e.g. "105"
                lcg_val  = row["lcg"].get().strip()
                tcg_val  = row["tcg"].get().strip()
                head_val = "1" if row["head"].get() else "0"

                pontoon_replacements[f"{{{{lcg{code}}}}}"] = lcg_val
                pontoon_replacements[f"{{{{tcg{code}}}}}"] = tcg_val
                pontoon_replacements[f"{{{{head{code}}}}}"] = head_val
        
        # Retrieve head LCG and TCG only if the pontoon tab exists and entries are populated
        if hasattr(pontoon_tab, 'headlcg_entry') and pontoon_tab.headlcg_entry.get().strip():
            head_lcg_val = pontoon_tab.headlcg_entry.get().strip()
        if hasattr(pontoon_tab, 'headtcg_entry') and pontoon_tab.headtcg_entry.get().strip():
            head_tcg_val = pontoon_tab.headtcg_entry.get().strip()
    
    # Add head LCG/TCG to replacements
    pontoon_replacements["{{headlcg}}"] = head_lcg_val
    pontoon_replacements["{{headtcg}}"] = head_tcg_val

    #damage stability logic
    # Compartment standard
    c_value = damage_widgets["compartment_standard_var"].get()

    # Old T checkbox value
    oldt_value = "set OLDT = Yes" if damage_widgets["oldt_var"].get() else ""

    # Floodable Subdivisions logic
    dcconditions_block = ""
    for i, row in enumerate(damage_widgets["subdivisions"], start=1):
        comp_name = row["entry"].get().strip()
        perm = row["perm_entry"].get().strip()

        if comp_name:
            dcconditions_block += (
                f"variable(string) DC{i}\n"
                f'SET DC{i} = "{comp_name}"\n'
                f'PERM ("{comp_name}") "{perm}"\n\n'
            )


    

    # Define your templates and output filenames
    templates = {
        "ls_temp.txt": "ls.rf",
        "load_temp.txt": "load.rf",
        "int_temp.txt": "int.rf",
        "dam_temp.txt": "dam.rf",
        "pontoon_temp.txt": "pontoon.lib",
        "macro_temp.txt": "macro.lib"
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
            .replace("{{beam}}", beam)
            .replace("{{length}}", length)
            .replace("{{critical_points}}", crit_block.strip())
            .replace("{{wind_area}}", wind_area)
            .replace("{{wind_arm}}",  wind_arm)
            .replace("{{notanksfs}}", notanksfs)
            .replace("{{c}}", c_value)
            .replace("{{oldt}}", oldt_value)
            .replace("{{dcconditions}}", dcconditions_block.strip())
        )

       # Apply pontoon-specific replacements IF this is the pontoon template
        if template_file == "pontoon_temp.txt":
            for placeholder, value in pontoon_replacements.items():
                filled_text = filled_text.replace(placeholder, value)

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

# File Location (optional)
file_location_label = tk.Label(tab_report, text="File Location (optional):")
file_location_label.pack(pady=(10, 0))
file_location_entry = tk.Entry(tab_report, width=50)
file_location_entry.pack(pady=(0, 10))

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

# === TANK MODEL TOGGLE ===
# BooleanVar default True (checked)
tank_model_var = tk.BooleanVar(value=True)

def toggle_tank_model_field():
    """Show the Free Surface Moment field only when unchecked."""
    if not tank_model_var.get():
        tank_model_frame.pack(pady=(5, 0))
    else:
        tank_model_frame.pack_forget()   # <-- use pack_forget()

# Checkbutton itself
tank_chk = tk.Checkbutton(
    tab_loads,
    text="Vessel has tank model",
    variable=tank_model_var,
    command=toggle_tank_model_field
)
tank_chk.pack(pady=(20, 5))

# Frame for the Free Surface Moment input (hidden by default)
tank_model_frame = tk.Frame(tab_loads)

tk.Label(tank_model_frame, text="Free Surface Moment:").grid(row=0, column=0, padx=10)
fs_entry = tk.Entry(tank_model_frame, width=12)
fs_entry.grid(row=1, column=0, padx=10)

# Initialize visibility correctly
toggle_tank_model_field()


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
vessel_dropdown = ttk.Combobox(
    tab_stab,
    textvariable=vessel_var,
    values=list(vessel_label_to_value.keys()),
    state="readonly"
)
vessel_dropdown.pack()


def build_pontoon_content(tab):
    # 1) Passenger Crowding title
    tk.Label(tab, text="Passenger Crowding", font=("Arial", 12, "bold")) \
      .pack(pady=(10,5))

    load_cases = [
        ("Bow",         (0,1)),
        ("Port Bow",    (1,1)),
        ("Port",        (1,0)),
        ("Port Quarter",(1,2)),
        ("Stern",       (0,2)),
        ("Stbd Quarter",(2,2)),
        ("Stbd",        (2,0)),
        ("Stbd Bow",    (2,1)),
    ]

    def make_crowd_table(rows_per_passenger):
        crowd_frame = tk.Frame(tab)
        crowd_frame.pack(pady=5)
        title = f"{rows_per_passenger} sqft per Passenger"
        tk.Label(crowd_frame, text=title, font=("Arial",10,"italic")) \
          .grid(row=0, column=0, columnspan=4)

        headers = ["Crowding","LCG","TCG","Pax in Head"]
        for c, h in enumerate(headers):
            tk.Label(crowd_frame, text=h, font=("Arial",9,"bold")) \
              .grid(row=1, column=c, padx=5)

        entries = []
        for r, (name, (h_code, v_code)) in enumerate(load_cases, start=2):
            tk.Label(crowd_frame, text=name) \
              .grid(row=r, column=0, padx=5)
            e_lcg = tk.Entry(crowd_frame, width=8);  e_lcg.grid(row=r, column=1)
            e_tcg = tk.Entry(crowd_frame, width=8);  e_tcg.grid(row=r, column=2)
            b_head = tk.BooleanVar(value=False)
            tk.Checkbutton(crowd_frame, variable=b_head) \
              .grid(row=r, column=3)

            code = f"{h_code}{v_code}{2 if rows_per_passenger==2 else 5}"
            entries.append({
                "code": code,
                "lcg":  e_lcg,
                "tcg":  e_tcg,
                "head": b_head
            })
        return entries

    # build both tables
    tab.crowd2 = make_crowd_table(2)
    tab.crowd5 = make_crowd_table(5)

    # 3) Head Location
    tk.Label(tab, text="Head Location", font=("Arial", 12, "bold")) \
      .pack(pady=(15,5))
    hl_frame = tk.Frame(tab); hl_frame.pack(pady=5)
    tk.Label(hl_frame, text="LCG").grid(row=0, column=0, padx=10)
    tk.Label(hl_frame, text="TCG").grid(row=0, column=1, padx=10)
    tab.headlcg_entry = tk.Entry(hl_frame, width=10)
    tab.headlcg_entry.grid(row=1, column=0, padx=10)
    tab.headtcg_entry = tk.Entry(hl_frame, width=10)
    tab.headtcg_entry.grid(row=1, column=1, padx=10)



# placeholder for our dynamic tab
pontoon_tab = None

def update_pontoon_tab(*args):
    global pontoon_tab
    if vessel_var.get() == "Pontoon Boat" and pontoon_tab is None:
        pontoon_tab = tk.Frame(notebook)
        notebook.add(pontoon_tab, text="Pontoon")
        # build the full pontoon UI here
        build_pontoon_content(pontoon_tab)

    elif vessel_var.get() != "Pontoon Boat" and pontoon_tab is not None:
        notebook.forget(pontoon_tab)
        pontoon_tab = None

def update_pontoon_tab(*args):
    global pontoon_tab
    if vessel_var.get() == "Pontoon Boat" and pontoon_tab is None:
        pontoon_tab = tk.Frame(notebook)
        notebook.add(pontoon_tab, text="Pontoon")
        # build the full pontoon UI here
        build_pontoon_content(pontoon_tab)

    elif vessel_var.get() != "Pontoon Boat" and pontoon_tab is not None:
        notebook.forget(pontoon_tab)
        pontoon_tab = None

# Hook the trace *after* creating the combobox
vessel_var.trace_add("write", update_pontoon_tab)
# Call once in case default is already "Pontoon Boat"
update_pontoon_tab()

# === Vessel Dimensions ===
tk.Label(tab_stab, text="Vessel Dimensions:", font=("Arial",10,"bold")).pack(pady=(20,5))

dim_frame = tk.Frame(tab_stab)
dim_frame.pack()

# Beam
tk.Label(dim_frame, text="Beam:").grid(row=0, column=0, padx=10)
beam_entry = tk.Entry(dim_frame, width=12)
beam_entry.insert(0, "{WOA}")
beam_entry.grid(row=1, column=0, padx=10)

# Length
tk.Label(dim_frame, text="Length:").grid(row=0, column=1, padx=10)
length_entry = tk.Entry(dim_frame, width=12)
length_entry.insert(0, "{LOA}")
length_entry.grid(row=1, column=1, padx=10)

# Route

route_var = tk.StringVar(value="Select a route")
route_label_to_value = {
    "Protected Waters": "PROTECT",
    "Partially Protected Waters": "PARTIAL",
    "Exposed Waters": "EXPOSED"
}
tk.Label(tab_stab, text="Route:").pack(pady=(10, 0))
ttk.Combobox(tab_stab, textvariable=route_var, values=list(route_label_to_value.keys()), state="readonly").pack()

# === CRITICAL POINTS ===
tk.Label(tab_stab, text="Critical Points:", font=("Arial",10,"bold")).pack(pady=(20,5))

crit_frame = tk.Frame(tab_stab)
crit_frame.pack()

# Table header (hidden until first add)
crit_header_created = False
critical_points = []

def reposition_crit_button():
    idx = len(critical_points) + 1
    crit_button.grid_forget()
    crit_button.grid(row=idx, column=0, columnspan=5, pady=5)

def add_crit_row():
    global crit_header_created

    if not crit_header_created:
        headers = ["#", "Name", "Longitudinal", "Transverse", "Vertical", ""]
        for c, h in enumerate(headers):
            tk.Label(crit_frame, text=h, font=("Arial",10,"bold")).grid(row=0, column=c, padx=4)
        crit_header_created = True

    row = len(critical_points) + 1

    # Widgets
    num_lbl = tk.Label(crit_frame, text=str(row))
    name_ent = tk.Entry(crit_frame, width=15)
    long_ent = tk.Entry(crit_frame, width=10)
    trans_ent= tk.Entry(crit_frame, width=10)
    vert_ent = tk.Entry(crit_frame, width=10)

    # Layout
    num_lbl.grid(row=row, column=0, padx=2)
    name_ent.grid(row=row, column=1, padx=2)
    long_ent.grid(row=row, column=2, padx=2)
    trans_ent.grid(row=row, column=3, padx=2)
    vert_ent.grid(row=row, column=4, padx=2)

    # Delete button
    def delete_crit():
        for w in (num_lbl, name_ent, long_ent, trans_ent, vert_ent, del_btn):
            w.grid_forget()
        critical_points.remove(entry_row)
        # renumber remaining rows
        for i, er in enumerate(critical_points, start=1):
            er["num_lbl"].config(text=str(i))
        reposition_crit_button()

    del_btn = tk.Button(crit_frame, text="❌", command=delete_crit, fg="red")
    del_btn.grid(row=row, column=5, padx=2)

    entry_row = {
        "num_lbl": num_lbl,
        "name_ent": name_ent,
        "long_ent": long_ent,
        "trans_ent": trans_ent,
        "vert_ent": vert_ent,
        "del_btn": del_btn
    }
    critical_points.append(entry_row)
    reposition_crit_button()

crit_button = tk.Button(crit_frame, text="➕ Add Critical Point", command=add_crit_row)
crit_button.grid(row=1, column=0, columnspan=5, pady=5)

# === PROFILE AREA TOGGLE ===
# BooleanVar default True (checked)
tk.Label(tab_stab, text="Wind Profile:", font=("Arial",10,"bold")).pack(pady=(20,0))
profile_var = tk.BooleanVar(value=True)

# Checkbutton
chk = tk.Checkbutton(
    tab_stab,
    text="Model includes Profile Area:",
    variable=profile_var,
    command=lambda: toggle_profile_fields()
)
chk.pack(pady=(5, 5))

# Frame to hold the two additional fields (hidden by default)
profile_frame = tk.Frame(tab_stab)

# Wind Area
tk.Label(profile_frame, text="Wind Area:").grid(row=0, column=0, padx=10)
wind_area_entry = tk.Entry(profile_frame, width=12)
wind_area_entry.grid(row=1, column=0, padx=10)

# Distance between Above/Below WL Centroids
tk.Label(profile_frame, text="Distance between Above to Below WL Centroids:").grid(row=0, column=1, padx=10)
wind_arm_entry = tk.Entry(profile_frame, width=12)
wind_arm_entry.grid(row=1, column=1, padx=10)

def toggle_profile_fields():
    """Show the two fields only when checkbox is UN‐checked."""
    if not profile_var.get():
        profile_frame.pack(pady=(10,0))
    else:
        profile_frame.forget()

# Ensure correct initial state
toggle_profile_fields()

# === TAB 5: Damage Stability ===
damage_widgets = create_damage_tab(notebook)



# === Bottom Button ===
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x")
tk.Button(bottom_frame, text="Generate Run Files", command=generate_document).pack(pady=10)


# Start GUI
root.mainloop()
