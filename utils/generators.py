

# This file is part of the GHS Stability Generator project.

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