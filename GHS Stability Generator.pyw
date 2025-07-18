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

from utils.generators import resolve_output_directory

# Input Collector
from utils.input_collector import (
    collect_report_data,
    collect_lightship_data,
    collect_loads_data,
    collect_intact_data,
    collect_damage_data,
    collect_pontoon_data
)

def load_template_file(filename):
    """Loads a template file from the templates directory."""
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    path = os.path.join(template_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_document():
    """Collects data from all tabs and generates GHS run files."""
    report_data = collect_report_data(report_widgets)
    lightship_data = collect_lightship_data(lightship_widgets)
    loads_data = collect_loads_data(loads_widgets)
    intact_data = collect_intact_data(
        intact_widgets,
        route_var,
        route_label_to_value,
        vessel_var,
        vessel_label_to_value
    )
    damage_data = collect_damage_data(damage_widgets)
    pontoon_replacements = collect_pontoon_data(pontoon_widgets)

    # Resolve output directory
    output_dir = resolve_output_directory(report_data["custom_path"])

    # Prepare template-to-output mapping
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

        # Replace placeholders in template with collected data
        filled_text = (
            template
            .replace("{{hull}}", report_data["hull"])
            .replace("{{sg}}", report_data["sg_value"])
            .replace("{{unit_length}}", report_data["unit_length"])
            .replace("{{unit_weight}}", report_data["unit_weight"])
            .replace("{{fwddrloc}}", report_data["fwd_draft"])
            .replace("{{middrloc}}", report_data["mid_draft"])
            .replace("{{aftdrloc}}", report_data["aft_draft"])
            .replace("{{route}}", intact_data["route_value"])
            .replace("{{vessel}}", intact_data["vessel_value"])
            .replace("{{option}}", lightship_data["survey_value"])
            .replace("{{excel_paste}}", lightship_data["excel_data"])
            .replace("{{vert}}", lightship_data["vert_value"])
            .replace("{{gmmt}}", lightship_data["gmmt_value"])
            .replace("{{disp}}", f"WEIGHT {lightship_data['disp']}" if lightship_data["disp"] else "")
            .replace("{{user_lightship_units}}", lightship_data["unit_value"])
            .replace("{{ltsh_lcg}}", lightship_data["ltsh_lcg"])
            .replace("{{ltsh_tcg}}", lightship_data["ltsh_tcg"])
            .replace("{{ltsh_vcg}}", lightship_data["ltsh_vcg"])
            .replace("{{initial_weights}}", lightship_data["initial_weights_block"].strip())
            .replace("{{initial_tanks}}", lightship_data["initial_tanks_block"].strip())
            .replace("{{paxct}}", loads_data["paxct"])
            .replace("{{paxwt}}", loads_data["paxwt"])
            .replace("{{paxlcg}}", loads_data["paxlcg"])
            .replace("{{paxtcg}}", loads_data["paxtcg"])
            .replace("{{paxvcg}}", loads_data["paxvcg"])
            .replace("{{addstuff}}", loads_data["addstuff_block"].strip())
            .replace("{{fsm_tanks}}", loads_data["fsm_tanks"])
            .replace("{{tank_macros}}", loads_data["macro_block"])
            .replace("{{beam}}", intact_data["beam"])
            .replace("{{length}}", intact_data["length"])
            .replace("{{critical_points}}", intact_data["crit_block"].strip())
            .replace("{{wind_area}}", intact_data["wind_area"])
            .replace("{{wind_arm}}", intact_data["wind_arm"])
            .replace("{{notanksfs}}", loads_data["notanksfs"])
            .replace("{{c}}", damage_data["c_value"])
            .replace("{{oldt}}", damage_data["oldt_value"])
            .replace("{{dcconditions}}", damage_data["dcconditions_block"].strip())
            .replace("{{macroperm}}", damage_data["macroperm_block"].strip())
        )

        # Pontoon-specific replacements
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
