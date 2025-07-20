"""
GHS_Stability_Generator
A tool to generate GHS run files for stability analysis
Version: 4.0.0
Updated: 07-19-2025
Created by: Trip Jackson
"""
import tkinter as tk
# main.py
from gui.setup_gui import setup_gui
from gui.update_tabs import setup_pontoon_vessel_tracer
from logic.generators import generate_document



def main():
    """Main function to set up the GUI and handle the generation of GHS run files."""
    gui_state = setup_gui()

    pontoon_info = setup_pontoon_vessel_tracer(
        gui_state["vessel_var"],
        gui_state["notebook"],
        gui_state["build_pontoon_tab"]
    )

    def on_generate():
        generate_document(
            gui_state["report_widgets"],
            gui_state["lightship_widgets"],
            gui_state["loads_widgets"],
            gui_state["intact_widgets"],
            gui_state["route_var"],
            gui_state["route_label_to_value"],
            gui_state["vessel_var"],
            gui_state["vessel_label_to_value"],
            gui_state["damage_widgets"],
            pontoon_info["widgets"],
            gui_state["root"]
        )

    # Add Generate Button
    generate_btn = tk.Button(gui_state["root"], text="Generate Run File", command=on_generate)
    generate_btn.pack(pady=10)

    gui_state["root"].mainloop()

if __name__ == "__main__":
    main()
