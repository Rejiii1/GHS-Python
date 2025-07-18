"""GHS_Stability_Generator
   A tool to generate GHS run files for stability analysis
   Version: 1.0.1
   Updated: 07-16-2025
   Created by: Trip Jackson
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os


#GUI
#tabs
from tabs.tab_report import create_report_tab
from tabs.tab_lightship import create_lightship_tab
from tabs.tab_loads import create_loads_tab
from tabs.tab_intact import create_intact_tab
from tabs.tab_pontoon import build_pontoon_tab
from tabs.tab_damage import create_damage_tab
#Generators
 #  Generators

from utils.generators import (
    resolve_output_directory,           #  Report Tab
    generate_initial_weights_block,     #  Lightship Tab
    generate_initial_tanks_block,
    generate_additional_weights_block,  #  Loads Tab
    generate_macro_tanks_block,
    generate_critical_points_block,     #  Intact Stability Tab
    generate_pontoon_replacements,      #  Pontoon Tab
    generate_damage_stability_block,    #  Damage Stability Tab
    )
#Constants
from utils.constants import load_patterns


def load_template_file(filename):
    """Loads a template file from the templates directory."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    path = os.path.join(template_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_document():
    """Generates the GHS run files based on user input from the GUI."""
    global add_weights
 #Report Tab =======================================================================================
 # Widgets
    hull = report_widgets["name_entry"].get().strip()
    sg_value = report_widgets["sg_label_to_value"].get(report_widgets["sg_var"].get(), "")
    unit_length = report_widgets["length_label_to_value"].get(report_widgets["length_var"].get(), "")
    unit_weight = report_widgets["weight_label_to_value"].get(report_widgets["weight_var"].get(), "")
    fwd_draft = report_widgets["fwd_draft_entry"].get().strip()
    mid_draft = report_widgets["mid_draft_entry"].get().strip()
    aft_draft = report_widgets["aft_draft_entry"].get().strip()

 #  Resolve output directory
    custom_path = report_widgets["file_location_entry"].get().strip()
    output_dir = resolve_output_directory(custom_path)

 #Lightship Tab ====================================================================================
 #  Widgets
        # Preset survey options in case not used
    excel_data = ""
    vert_value = "1"
    gmmt_value = "1"
    disp = ltsh_lcg = ltsh_tcg = ltsh_vcg = ""
    survey_label = lightship_widgets["survey_var"].get().strip()
    survey_value = lightship_widgets["survey_label_to_value"].get(survey_label, "")
    if survey_label in ["Deadweight Survey", "Inclining Experiment"]:
        excel_data = lightship_widgets["excel_text"].get("1.0", tk.END).strip()
    if survey_label == "Deadweight Survey":
        vert_value = lightship_widgets["vert_entry"].get().strip()
    if survey_label == "Inclining Experiment":
        gmmt_value = lightship_widgets["gmmt_entry"].get().strip()
    if survey_label == "User Defined Lightship":
        disp = lightship_widgets["disp_entry"].get().strip()
        ltsh_lcg = lightship_widgets["ltsh_lcg_entry"].get().strip()
        ltsh_tcg = lightship_widgets["ltsh_tcg_entry"].get().strip()
        ltsh_vcg = lightship_widgets["ltsh_vcg_entry"].get().strip()
    unit_value = f'UNITS {
        lightship_widgets["unit_var"].get()}' if survey_label == "User Defined Lightship" else ""

 # Prepare Initial Weights Block
     # Safe defaults in case there are no initial weights
    initial_wt_lcg = ""
    initial_wt_tcg = ""
    initial_wt_vcg = ""
    initial_weights_block = generate_initial_weights_block(lightship_widgets["initial_weights"])
 # Prepare Initial Tanks Block
    initial_tanks_block = generate_initial_tanks_block(lightship_widgets["initial_tanks"])
 #Loads Tab ========================================================================================
 #  Widgets - not yet widgets
    # === PASSENGER INFO ===
    paxct   = loads_widgets["pax_count_entry"].get().strip()
    paxwt   = loads_widgets["pax_weight_entry"].get().strip()
    paxlcg  = loads_widgets["pax_lcg_entry"].get().strip()
    paxtcg  = loads_widgets["pax_tcg_entry"].get().strip()
    paxvcg  = loads_widgets["pax_vcg_entry"].get().strip()

 #  Additional Weights Block
    addstuff_block = generate_additional_weights_block(loads_widgets["add_weights"])
 #  Macro Tanks Sections
    macro_block = generate_macro_tanks_block(load_patterns, loads_widgets["load_tanks"])
 # Create the FSM list of real Tanks
    fsm_tanks_list = [
        t["name_widget"].get().strip()
        for t in loads_widgets["load_tanks"]
        if t["name_widget"].get().strip()
    ]
    fsm_tanks = " ".join(fsm_tanks_list)
 #  FSM for Manual Tank Entry
    if not loads_widgets["tank_model_var"].get():
        notanksfs = loads_widgets["fs_entry"].get().strip()
    else:
        notanksfs = "0"


 #Intact Stability Tab =============================================================================
 #  Widgets
    selected_label = route_var.get().strip()
    route_value = route_label_to_value.get(selected_label, "")
    beam = intact_widgets["beam_entry"].get().strip()
    length = intact_widgets["length_entry"].get().strip()
    vessel_label = vessel_var.get().strip()
    vessel_value = vessel_label_to_value.get(vessel_label, "")
 # Wind Area and Arm Manual
    if not intact_widgets["profile_var"].get():
        wind_area = intact_widgets["wind_area_entry"].get().strip()
        wind_arm = intact_widgets["wind_arm_entry"].get().strip()
    else:
        wind_area = "0"
        wind_arm  = "0"
 # Critical Points Block
    crit_block = generate_critical_points_block(intact_widgets["critical_points"])



 #Damage Stability Tab =============================================================================
 #  Damage stability logic
    c_value, oldt_value, dcconditions_block, macroperm_block = generate_damage_stability_block(
        damage_widgets)
 #Pontoon Tab ======================================================================================
 # PONTOON-SPECIFIC DATA EXTRACTION (DO THIS ONCE, BEFORE THE TEMPLATE LOOP)
    pontoon_replacements = generate_pontoon_replacements(pontoon_widgets)

 #fill in these fields error message - tabbed out b/c annoying
 #   if not hull or not survey_value:
 #       messagebox.showwarning("Missing info",
 #                              "Please fill in all fields and select valid options.")
 #       return


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
            template = load_template_file(template_file)
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
            .replace("{{macroperm}}", macroperm_block.strip())
        )

       # Apply pontoon-specific replacements IF this is the pontoon template
        if template_file == "pontoon_temp.txt":
            for placeholder, value in pontoon_replacements.items():
                filled_text = filled_text.replace(placeholder, value)

        output_path = os.path.join(output_dir, output_file)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filled_text)

    messagebox.showinfo("Success", f"All files saved in:\n{output_dir}")
    root.destroy()

# GUI setup
# === SETUP ROOT ===
root = tk.Tk()
root.title("GHS Run File Creator")
root.geometry("600x800")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# === TAB 1: Report Details ===
report_widgets = create_report_tab(notebook)

# === TAB 2: Lightship ===
lightship_frame, lightship_widgets = create_lightship_tab(notebook)

# === TAB 3: Loads ===
loads_tab, loads_widgets = create_loads_tab(notebook)
# === TAB 4: Intact Stability ===
vessel_var = tk.StringVar(value="Select a vessel type")
vessel_label_to_value = {
    "Power Boat": "POWER",
    "Pontoon Boat": "PONTOON",
    "RHIB": "RHIB",
    "Monohull Sailboat": "MONOSAIL",
    "Catamaran Sailboat": "CATSAIL"
}
route_var = tk.StringVar(value="Select a route")
route_label_to_value = {
    "Protected Waters": "PROTECT",
    "Partially Protected Waters": "PARTIAL",
    "Exposed Waters": "EXPOSED"
}

intact_widgets = create_intact_tab(
    notebook, vessel_var, vessel_label_to_value, route_var, route_label_to_value
)
# === TAB 4.5: Pontoon Stability ==
pontoon_tab = None
pontoon_widgets = None  # To hold crowd/head entries if you want later

def update_pontoon_tab(*args):
    """Updates the Pontoon tab based on the selected vessel type."""
    global pontoon_tab, pontoon_widgets

    if vessel_var.get() == "Pontoon Boat" and pontoon_tab is None:
        pontoon_tab, pontoon_widgets = build_pontoon_tab(notebook)

    elif vessel_var.get() != "Pontoon Boat" and pontoon_tab is not None:
        notebook.forget(pontoon_tab)
        pontoon_tab = None
        pontoon_widgets = None


# Hook the trace *after* creating the combobox
vessel_var.trace_add("write", update_pontoon_tab)
# Call once in case default is already "Pontoon Boat"
update_pontoon_tab()





# === TAB 5: Damage Stability ===
damage_widgets = create_damage_tab(notebook)

# === Bottom Button ===
bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x")
tk.Button(bottom_frame, text="Generate Run Files", command=generate_document).pack(pady=10)

# Start GUI
root.mainloop()
