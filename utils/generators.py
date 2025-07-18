"""This module contains functions to generate various blocks of text
for a ship stability analysis based on user input from a GUI.
"""
import os

def resolve_output_directory(custom_path: str) -> str:
    """Resolves the output directory for generated files."""
    if custom_path:
        output_dir = custom_path
    else:
        output_dir = os.path.join(os.getcwd(), "generated")

    os.makedirs(output_dir, exist_ok=True)
    return output_dir



#Initial Weights Block Generator
def generate_initial_weights_block(initial_weights):
    """Generates the initial weights at the time of survey into run file"""
    block = ""
    grouped = {"LB": [], "LT": []}

    for row in initial_weights:
        action = row["action"].get().strip().upper()
        item = row["item"].get().strip()
        weight = row["weight"].get().strip()
        units = row["units"].get().strip().upper()
        lcg = row["initial_wt_lcg"].get().strip()
        tcg = row["initial_wt_tcg"].get().strip()
        vcg = row["initial_wt_vcg"].get().strip()

        if not action or not item or not weight or not lcg or not tcg or not vcg or units not in grouped:
            continue

        weight_str = weight
        if action == "ADD" and not weight_str.startswith("-"):
            weight_str = f"-{weight_str}"
        elif action == "REMOVE":
            weight_str = weight_str.lstrip("-")

        grouped[units].append((item, weight_str, lcg, tcg, vcg))

    for unit, rows in grouped.items():
        if rows:
            block += f"UNITS {unit}\n"
            for item, weight, lcg, tcg, vcg in rows:
                block += f'ADD "{item}" {weight} {lcg} {tcg} {vcg}\n'
    return block.strip()


# Initial Tanks Block Generator
def generate_initial_tanks_block(initial_tanks):
    """Generates the initial tanks block inserted into run file"""
    block = ""

    for tank in initial_tanks:
        tank_name = tank["name"].get().strip()
        sg = tank["sg"].get().strip()
        load = tank["load"].get().strip()

        if not tank_name or not sg or not load:
            continue

        block += f"TANK {tank_name}\n"
        block += f"CONTENTS {sg}\n"
        block += f"LOAD ({tank_name}) {load}\n\n"

    return block.strip()


# Additional Weights Block Generator
def generate_additional_weights_block(add_weights):
    """Generates the every time weights block inserted into run file"""
    block = ""
    grouped_by_units = {"LB": [], "LT": []}

    for row in add_weights:
        item = row["item"].get().strip()
        weight = row["weight"].get().strip()
        units = row["units"].get().strip().upper()
        lcg = row["lcg"].get().strip()
        tcg = row["tcg"].get().strip()
        vcg = row["vcg"].get().strip()

        if not item or not weight or not lcg or not tcg or not vcg or units not in grouped_by_units:
            continue

        grouped_by_units[units].append((item, weight, lcg, tcg, vcg))

    for unit, rows in grouped_by_units.items():
        if rows:
            block += f"UNITS {unit}\n"
            for item, weight, lcg, tcg, vcg in rows:
                block += f'ADD "{item}" {weight} {lcg} {tcg} {vcg}\n'

    return block.strip()


# Macro Tanks Block Generator
def generate_macro_tanks_block(load_patterns, load_tanks):
    """Generates the macro for tanks based on load case and tank data."""
    macro_block = ""
    for stage in ["Departure", "Midway", "Arrival"]:
        info = load_patterns.get(stage, {})
        macro_block += f"`-----{stage} Tanks-----\n"
        macro_block += f"{info.get('default', '')}\n"
        macro_block += "`LOAD (TANK) %\n"
        for t in load_tanks:
            name = t["name_widget"].get().strip()
            contents = t["contents_var"].get()
            pct = info.get("load", {}).get(contents, "")
            macro_block += f"LOAD ({name}) {pct}\n"
        macro_block += "/\n"
    return macro_block



def generate_critical_points_block(critical_points):
    """Generates the critical points from the GUI."""
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

    return crit_block

# Damage Stability Block Generator
def generate_damage_stability_block(damage_widgets):
    """Generates the damage stability string of compartments"""
    c_value = damage_widgets["compartment_standard_var"].get()
    oldt_value = "set OLDT = Yes" if damage_widgets["oldt_var"].get() else ""

    dcconditions_block = ""
    macroperm_block = ""
    for i, row in enumerate(damage_widgets["subdivisions"], start=1):
        comp_name = row["entry"].get().strip()
        perm = row["perm_entry"].get().strip()
        if comp_name:
            dcconditions_block += (
                f"variable(string) DC{i}\n"
                f'SET DC{i} = "{comp_name}"\n'
            )
            macroperm_block += f'PERM ("{comp_name}") "{perm}"\n'

    return c_value, oldt_value, dcconditions_block, macroperm_block


# Pontoon Replacements Generator
def generate_pontoon_replacements(pontoon_widgets):
    """Generates the replacements for pontoon data."""
    pontoon_replacements = {}
    head_lcg_val = ""
    head_tcg_val = ""

    if pontoon_widgets:
        for table in (pontoon_widgets["crowd2"], pontoon_widgets["crowd5"]):
            for row in table:
                code = row["code"]
                lcg_val = row["lcg"].get().strip()
                tcg_val = row["tcg"].get().strip()
                head_val = "1" if row["head"].get() else "0"

                pontoon_replacements[f"{{{{lcg{code}}}}}"] = lcg_val
                pontoon_replacements[f"{{{{tcg{code}}}}}"] = tcg_val
                pontoon_replacements[f"{{{{head{code}}}}}"] = head_val

        head_lcg_val = pontoon_widgets["headlcg_entry"].get().strip()
        head_tcg_val = pontoon_widgets["headtcg_entry"].get().strip()

    pontoon_replacements["{{headlcg}}"] = head_lcg_val
    pontoon_replacements["{{headtcg}}"] = head_tcg_val

    return pontoon_replacements
