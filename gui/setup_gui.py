"""GUI setup file"""
import tkinter as tk
from tkinter import ttk
from tabs.tab_report import create_report_tab
from tabs.tab_lightship import create_lightship_tab
from tabs.tab_loads import create_loads_tab
from tabs.tab_intact import create_intact_tab
from tabs.tab_damage import create_damage_tab
from tabs.tab_pontoon import build_pontoon_tab

def setup_gui():
    """Sets up the main GUI for the GHS Run File Creator."""
    root = tk.Tk()
    root.title("GHS Run File Creator")
    root.geometry("600x800")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Report
    report_widgets = create_report_tab(notebook)

    # Lightship
    lightship_frame, lightship_widgets = create_lightship_tab(notebook)#IGNORE THAT 

    # Loads
    loads_tab, loads_widgets = create_loads_tab(notebook) #IGNORE THAT 

    # Vessel + Route dropdowns
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

    # Intact tab
    intact_widgets = create_intact_tab(
        notebook, vessel_var, vessel_label_to_value, route_var, route_label_to_value
    )

    # Damage
    damage_widgets = create_damage_tab(notebook)

    return {
        "root": root,
        "notebook": notebook,
        "report_widgets": report_widgets,
        "lightship_widgets": lightship_widgets,
        "loads_widgets": loads_widgets,
        "intact_widgets": intact_widgets,
        "vessel_var": vessel_var,
        "vessel_label_to_value": vessel_label_to_value,
        "route_var": route_var,
        "route_label_to_value": route_label_to_value,
        "damage_widgets": damage_widgets,
        "build_pontoon_tab": build_pontoon_tab,
    }
