"""This module collects data from various GUI widgets and generates GHS run files.
It includes functions to gather data from report, lightship, loads, intact, damage & pontoon tabs.
Used in the Generate Document functionality of the GHS Stability Generator application.
"""
from utils.generators import (
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

def collect_report_data(report_widgets):
    """Collects data from the report tab widgets."""
    hull = report_widgets["name_entry"].get().strip()
    sg_value = report_widgets["sg_label_to_value"].get(report_widgets["sg_var"].get(), "")
    unit_length = report_widgets["length_label_to_value"].get(report_widgets["length_var"].get(), "")
    unit_weight = report_widgets["weight_label_to_value"].get(report_widgets["weight_var"].get(), "")
    fwd_draft = report_widgets["fwd_draft_entry"].get().strip()
    mid_draft = report_widgets["mid_draft_entry"].get().strip()
    aft_draft = report_widgets["aft_draft_entry"].get().strip()
    custom_path = report_widgets["file_location_entry"].get().strip()

    return {
        "hull": hull,
        "sg_value": sg_value,
        "unit_length": unit_length,
        "unit_weight": unit_weight,
        "fwd_draft": fwd_draft,
        "mid_draft": mid_draft,
        "aft_draft": aft_draft,
        "custom_path": custom_path,
    }


def collect_lightship_data(lightship_widgets):
    """Collects data from the lightship tab widgets."""
    excel_data = ""
    vert_value = "1"
    gmmt_value = "1"
    disp = ltsh_lcg = ltsh_tcg = ltsh_vcg = ""
    survey_label = lightship_widgets["survey_var"].get().strip()
    survey_value = lightship_widgets["survey_label_to_value"].get(survey_label, "")

    if survey_label in ["Deadweight Survey", "Inclining Experiment"]:
        excel_data = lightship_widgets["excel_text"].get("1.0", "end").strip()
    if survey_label == "Deadweight Survey":
        vert_value = lightship_widgets["vert_entry"].get().strip()
    if survey_label == "Inclining Experiment":
        gmmt_value = lightship_widgets["gmmt_entry"].get().strip()
    if survey_label == "User Defined Lightship":
        disp = lightship_widgets["disp_entry"].get().strip()
        ltsh_lcg = lightship_widgets["ltsh_lcg_entry"].get().strip()
        ltsh_tcg = lightship_widgets["ltsh_tcg_entry"].get().strip()
        ltsh_vcg = lightship_widgets["ltsh_vcg_entry"].get().strip()
    unit_value = f'UNITS {lightship_widgets["unit_var"].get()}' if survey_label == "User Defined Lightship" else ""

    initial_weights_block = generate_initial_weights_block(lightship_widgets["initial_weights"])
    initial_tanks_block = generate_initial_tanks_block(lightship_widgets["initial_tanks"])

    return {
        "excel_data": excel_data,
        "vert_value": vert_value,
        "gmmt_value": gmmt_value,
        "disp": disp,
        "ltsh_lcg": ltsh_lcg,
        "ltsh_tcg": ltsh_tcg,
        "ltsh_vcg": ltsh_vcg,
        "survey_value": survey_value,
        "unit_value": unit_value,
        "initial_weights_block": initial_weights_block,
        "initial_tanks_block": initial_tanks_block,
    }


def collect_loads_data(loads_widgets):
    """Collects data from the loads tab widgets."""   
    def replace_empty_with_zero(value):
        return value if value else "0" 
    paxct = replace_empty_with_zero(loads_widgets["pax_count_entry"].get().strip())
    paxwt = loads_widgets["pax_weight_entry"].get().strip()
    paxlcg = replace_empty_with_zero(loads_widgets["pax_lcg_entry"].get().strip())
    paxtcg = replace_empty_with_zero(loads_widgets["pax_tcg_entry"].get().strip())
    paxvcg = replace_empty_with_zero(loads_widgets["pax_vcg_entry"].get().strip())

    addstuff_block = generate_additional_weights_block(loads_widgets["add_weights"])
    macro_block = generate_macro_tanks_block(load_patterns, loads_widgets["load_tanks"])

    fsm_tanks_list = [
        t["name_widget"].get().strip()
        for t in loads_widgets["load_tanks"]
        if t["name_widget"].get().strip()
    ]
    fsm_tanks = " ".join(fsm_tanks_list)

    if not loads_widgets["tank_model_var"].get():
        notanksfs = loads_widgets["fs_entry"].get().strip()
    else:
        notanksfs = "0"

    return {
        "paxct": paxct,
        "paxwt": paxwt,
        "paxlcg": paxlcg,
        "paxtcg": paxtcg,
        "paxvcg": paxvcg,
        "addstuff_block": addstuff_block,
        "macro_block": macro_block,
        "fsm_tanks": fsm_tanks,
        "notanksfs": notanksfs,
    }


def collect_intact_data(
        intact_widgets, route_var, route_label_to_value,
        vessel_var, vessel_label_to_value):
    """Collects data from the intact stability tab widgets."""
    selected_label = route_var.get().strip()
    route_value = route_label_to_value.get(selected_label, "")
    beam = intact_widgets["beam_entry"].get().strip()
    length = intact_widgets["length_entry"].get().strip()
    vessel_label = vessel_var.get().strip()
    vessel_value = vessel_label_to_value.get(vessel_label, "")

    if not intact_widgets["profile_var"].get():
        wind_area = intact_widgets["wind_area_entry"].get().strip()
        wind_arm = intact_widgets["wind_arm_entry"].get().strip()
    else:
        wind_area = "0"
        wind_arm = "0"

    crit_block = generate_critical_points_block(intact_widgets["critical_points"])

    return {
        "route_value": route_value,
        "beam": beam,
        "length": length,
        "vessel_value": vessel_value,
        "wind_area": wind_area,
        "wind_arm": wind_arm,
        "crit_block": crit_block,
    }


def collect_damage_data(damage_widgets):
    """Collects data from the damage stability tab widgets."""
    c_value, oldt_value, dcconditions_block, macroperm_block = generate_damage_stability_block(damage_widgets)
    return {
        "c_value": c_value,
        "oldt_value": oldt_value,
        "dcconditions_block": dcconditions_block,
        "macroperm_block": macroperm_block,
    }


def collect_pontoon_data(pontoon_widgets):
    pontoon_replacements = generate_pontoon_replacements(pontoon_widgets)
    return pontoon_replacements
