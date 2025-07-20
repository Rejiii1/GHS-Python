# gui/update_pontoon_tab.py
def setup_pontoon_vessel_tracer(vessel_var, notebook, build_pontoon_tab):
    """Sets up the pontoon tab based on the selected vessel type."""
    pontoon_tab = {"tab": None, "widgets": None}

    def update_pontoon_tab(*args):
        """Updates the pontoon tab based on the selected vessel type."""
        if vessel_var.get() == "Pontoon Boat" and pontoon_tab["tab"] is None:
            pontoon_tab["tab"], pontoon_tab["widgets"] = build_pontoon_tab(notebook)
        elif vessel_var.get() != "Pontoon Boat" and pontoon_tab["tab"] is not None:
            notebook.forget(pontoon_tab["tab"])
            pontoon_tab["tab"] = None
            pontoon_tab["widgets"] = None

    vessel_var.trace_add("write", update_pontoon_tab)
    update_pontoon_tab()

    return pontoon_tab
