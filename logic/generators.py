"""This module handles the generation of GHS run files based on user input."""
from tkinter import messagebox
import os
from pathlib import Path

from utils.block_builders import resolve_output_directory


# Input Collector
from utils.input_collector import (
    collect_report_data,
    collect_lightship_data,
    collect_loads_data,
    collect_intact_data,
    collect_damage_data,
    collect_pontoon_data
)

# Path to the templates directory
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"

def load_template_file(filename):
    """Loads a template file from the templates directory located in the project root."""
    project_root = os.path.dirname(os.path.dirname(__file__))  # One level up
    template_dir = os.path.join(project_root, "templates")
    path = os.path.join(template_dir, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Template file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_document(
    report_widgets,
    lightship_widgets,
    loads_widgets,
    intact_widgets,
    route_var,
    route_label_to_value,
    vessel_var,
    vessel_label_to_value,
    damage_widgets,
    pontoon_widgets,
    root
):
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
