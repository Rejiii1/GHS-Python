# This file is part of the GHS Stability Generator project.
import os

def resolve_output_directory(custom_path: str) -> str:
    if custom_path:
        output_dir = custom_path
    else:
        output_dir = os.path.join(os.getcwd(), "generated")

    os.makedirs(output_dir, exist_ok=True)
    return output_dir



#Initial Weights Block Generator
# It generates the initial weights block based on user input from the GUI.
def generate_initial_weights_block(initial_weights):
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
# It generates the initial tanks block based on user input from the GUI.
def generate_initial_tanks_block(initial_tanks):
    block = ""

    for tank in initial_tanks:
        tank_name = tank["name"].get().strip()
        contents = tank["contents"].get().strip()
        sg = tank["sg"].get().strip()
        load = tank["load"].get().strip()

        if not tank_name or not sg or not load:
            continue

        block += f"TANK {tank_name}\n"
        block += f"CONTENTS {sg}\n"
        block += f"LOAD ({tank_name}) {load}\n\n"

    return block.strip()


# Additional Weights Block Generator
# It generates an every time load case weights block based on user input from the GUI.
def generate_additional_weights_block(add_weights):
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
# It generates a macro block for tanks based on load patterns and tank data.
def generate_macro_tanks_block(load_patterns, load_tanks):
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
# It generates the damage stability Info based on user input from the GUI.
def generate_damage_stability_block(damage_widgets):
    c_value = damage_widgets["compartment_standard_var"].get()
    oldt_value = "set OLDT = Yes" if damage_widgets["oldt_var"].get() else ""

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

    return c_value, oldt_value, dcconditions_block


# Pontoon Replacements Generator
# It generates replacements for pontoon data based on user input from the GUI.
def generate_pontoon_replacements(pontoon_tab):
    pontoon_replacements = {}
    head_lcg_val = ""
    head_tcg_val = ""

    if pontoon_tab:
        for table in (pontoon_tab.crowd2, pontoon_tab.crowd5):
            for row in table:
                code = row["code"]
                lcg_val = row["lcg"].get().strip()
                tcg_val = row["tcg"].get().strip()
                head_val = "1" if row["head"].get() else "0"

                pontoon_replacements[f"{{{{lcg{code}}}}}"] = lcg_val
                pontoon_replacements[f"{{{{tcg{code}}}}}"] = tcg_val
                pontoon_replacements[f"{{{{head{code}}}}}"] = head_val

        if hasattr(pontoon_tab, 'headlcg_entry') and pontoon_tab.headlcg_entry.get().strip():
            head_lcg_val = pontoon_tab.headlcg_entry.get().strip()
        if hasattr(pontoon_tab, 'headtcg_entry') and pontoon_tab.headtcg_entry.get().strip():
            head_tcg_val = pontoon_tab.headtcg_entry.get().strip()

    pontoon_replacements["{{headlcg}}"] = head_lcg_val
    pontoon_replacements["{{headtcg}}"] = head_tcg_val

    return pontoon_replacements