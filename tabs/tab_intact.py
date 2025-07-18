"""Intact Stability Tab for Ship Stability Application
This module creates the Intact tab in the main application notebook.
"""
import tkinter as tk
from tkinter import ttk

def create_intact_tab(notebook, vessel_var, vessel_label_to_value, route_var, route_label_to_value):
    """Builds the Intact Stability tab UI and returns all related widgets/variables."""
    tab_stab = tk.Frame(notebook)
    notebook.add(tab_stab, text="Intact Stability")

    # === Vessel Type Dropdown ===
    ttk.Label(tab_stab, text="Vessel Type:").pack(pady=(10, 0))
    ttk.Combobox(
        tab_stab,
        textvariable=vessel_var,
        values=list(vessel_label_to_value.keys()),
        state="readonly"
    ).pack()

    # === Vessel Dimensions ===
    tk.Label(tab_stab, text="Vessel Dimensions:", font=("Arial",10,"bold")).pack(pady=(20,5))

    dim_frame = tk.Frame(tab_stab)
    dim_frame.pack()

    # Beam
    tk.Label(dim_frame, text="Beam:").grid(row=0, column=0, padx=10)
    beam_entry = tk.Entry(dim_frame, width=12)
    beam_entry.insert(0, "{WOA}")
    beam_entry.grid(row=1, column=0, padx=10)

    # Length
    tk.Label(dim_frame, text="Length:").grid(row=0, column=1, padx=10)
    length_entry = tk.Entry(dim_frame, width=12)
    length_entry.insert(0, "{LOA}")
    length_entry.grid(row=1, column=1, padx=10)


    # === Route Dropdown ===
    tk.Label(tab_stab, text="Route:").pack(pady=(10, 0))
    ttk.Combobox(
        tab_stab,
        textvariable=route_var,
        values=list(route_label_to_value.keys()),
        state="readonly"
    ).pack()

    # === CRITICAL POINTS ===
    tk.Label(tab_stab, text="Critical Points:", font=("Arial",10,"bold")).pack(pady=(20,5))

    crit_frame = tk.Frame(tab_stab)
    crit_frame.pack()

    # Table header (hidden until first add)

    critical_points = []
    crit_header_created = False

    def reposition_crit_button():
        """Reposition the critical points button based on current entries."""
        idx = len(critical_points) + 1
        crit_button.grid_forget()
        crit_button.grid(row=idx, column=0, columnspan=5, pady=5)

    def add_crit_row():
        """Add a new row for critical points."""
        nonlocal crit_header_created

        if not crit_header_created:
            headers = ["#", "Name", "Longitudinal", "Transverse", "Vertical", ""]
            for c, h in enumerate(headers):
                tk.Label(crit_frame, text=h, font=("Arial",10,"bold")).grid(row=0, column=c, padx=4)
            crit_header_created = True

        row = len(critical_points) + 1

        # Widgets
        num_lbl = tk.Label(crit_frame, text=str(row))
        name_ent = tk.Entry(crit_frame, width=15)
        long_ent = tk.Entry(crit_frame, width=10)
        trans_ent= tk.Entry(crit_frame, width=10)
        vert_ent = tk.Entry(crit_frame, width=10)

        # Layout
        num_lbl.grid(row=row, column=0, padx=2)
        name_ent.grid(row=row, column=1, padx=2)
        long_ent.grid(row=row, column=2, padx=2)
        trans_ent.grid(row=row, column=3, padx=2)
        vert_ent.grid(row=row, column=4, padx=2)

        # Delete button
        def delete_crit():
            for w in (num_lbl, name_ent, long_ent, trans_ent, vert_ent, del_btn):
                w.grid_forget()
            critical_points.remove(entry_row)
            # renumber remaining rows
            for i, er in enumerate(critical_points, start=1):
                er["num_lbl"].config(text=str(i))
            reposition_crit_button()

        del_btn = tk.Button(crit_frame, text="❌", command=delete_crit, fg="red")
        del_btn.grid(row=row, column=5, padx=2)

        entry_row = {
            "num_lbl": num_lbl,
            "name_ent": name_ent,
            "long_ent": long_ent,
            "trans_ent": trans_ent,
            "vert_ent": vert_ent,
            "del_btn": del_btn
        }
        critical_points.append(entry_row)
        reposition_crit_button()

    crit_button = tk.Button(crit_frame, text="➕ Add Critical Point", command=add_crit_row)
    crit_button.grid(row=1, column=0, columnspan=5, pady=5)

    # === PROFILE AREA TOGGLE ===
    # BooleanVar default True (checked)
    tk.Label(tab_stab, text="Wind Profile:", font=("Arial",10,"bold")).pack(pady=(20,0))
    profile_var = tk.BooleanVar(value=True)

    # Checkbutton
    chk = tk.Checkbutton(
        tab_stab,
        text="Model includes Profile Area:",
        variable=profile_var,
        command=lambda: toggle_profile_fields()
    )
    chk.pack(pady=(5, 5))

    # Frame to hold the two additional fields (hidden by default)
    profile_frame = tk.Frame(tab_stab)

    # Wind Area
    tk.Label(profile_frame, text="Wind Area:").grid(row=0, column=0, padx=10)
    wind_area_entry = tk.Entry(profile_frame, width=12)
    wind_area_entry.grid(row=1, column=0, padx=10)

    # Distance between Above/Below WL Centroids
    tk.Label(profile_frame,
            text="Distance between Above to Below WL Centroids:").grid(row=0, column=1, padx=10)
    wind_arm_entry = tk.Entry(profile_frame, width=12)
    wind_arm_entry.grid(row=1, column=1, padx=10)

    def toggle_profile_fields():
        """Show the two fields only when checkbox is UN-checked."""
        if not profile_var.get():
            profile_frame.pack(pady=(10,0))
        else:
            profile_frame.forget()

    # Ensure correct initial state
    toggle_profile_fields()

    return {
        "tab_frame": tab_stab,
        "beam_entry": beam_entry,
        "length_entry": length_entry,
        "critical_points": critical_points,
        "profile_var": profile_var,
        "wind_area_entry": wind_area_entry,
        "wind_arm_entry": wind_arm_entry
    }
