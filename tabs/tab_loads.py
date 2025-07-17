"""This module creates the Loads tab in the GHS Stability Generator GUI."""
# tab_loads.py
import tkinter as tk
from tkinter import ttk

initial_weights = []
add_weights = []
fsm_tanks_list = []
add_header_created = False

def create_loads_tab(notebook):
    """Creates the Loads tab in the main GUI."""
    tab_loads = tk.Frame(notebook)
    notebook.add(tab_loads, text="Loads")

    # === PASSENGERS SECTION ===
    tk.Label(tab_loads, text="Passengers:", font=("Arial", 10, "bold")).pack(pady=(20, 5))

    # Number of Passengers
    tk.Label(tab_loads, text="Number of Passengers:").pack()
    pax_count_entry = tk.Entry(tab_loads, width=10)
    pax_count_entry.pack()

    # Passenger Weight
    tk.Label(tab_loads, text="Weight per Passenger (lbs):").pack()
    pax_weight_entry = tk.Entry(tab_loads, width=10)
    pax_weight_entry.insert(0, "185")
    pax_weight_entry.pack()

    # Passenger Location (LCG, TCG, VCG)
    tk.Label(tab_loads, text="Passenger Location:").pack(pady=(10, 0))
    pax_loc_frame = tk.Frame(tab_loads)
    pax_loc_frame.pack(pady=(0, 10))

    tk.Label(pax_loc_frame, text="LCG").grid(row=0, column=0, padx=10)
    tk.Label(pax_loc_frame, text="TCG").grid(row=0, column=1, padx=10)
    tk.Label(pax_loc_frame, text="VCG").grid(row=0, column=2, padx=10)

    pax_lcg_entry = tk.Entry(pax_loc_frame, width=10)
    pax_tcg_entry = tk.Entry(pax_loc_frame, width=10)
    pax_vcg_entry = tk.Entry(pax_loc_frame, width=10)

    pax_lcg_entry.grid(row=1, column=0, padx=10)
    pax_tcg_entry.grid(row=1, column=1, padx=10)
    pax_vcg_entry.grid(row=1, column=2, padx=10)


    # === ADDITIONAL WEIGHTS SECTION ===
    tk.Label(tab_loads, text="Additional Weights in Every Loadcase:",
            font=("Arial", 10, "bold")).pack(pady=(20, 5))

    add_weights_frame = tk.Frame(tab_loads)
    add_weights_frame.pack()

    def reposition_add_load_button():
        """Repositions the 'Add Weight' button based on the number of weights."""
        row_idx = len(add_weights) + 1
        add_load_button.grid_forget()
        add_load_button.grid(row=row_idx, column=0, columnspan=6, pady=5)

    def add_load_row():
        """Adds a new row for additional weights."""
        global add_header_created

        if not add_header_created:
            headers = ["Item Name", "Weight", "Units", "LCG", "TCG", "VCG"]
            for col, label in enumerate(headers):
                tk.Label(add_weights_frame, text=label,
                        font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
            add_header_created = True

        row_idx = len(add_weights) + 1

        row_data = {
            "item": tk.Entry(add_weights_frame, width=12),
            "weight": tk.Entry(add_weights_frame, width=8),
            "units": ttk.Combobox(add_weights_frame, values=["LB", "LT"],
                                  width=6, state="readonly"),
            "lcg": tk.Entry(add_weights_frame, width=8),
            "tcg": tk.Entry(add_weights_frame, width=8),
            "vcg": tk.Entry(add_weights_frame, width=8)
        }
        row_data["units"].set("LB")

        row_data["item"].grid(row=row_idx, column=0, padx=2)
        row_data["weight"].grid(row=row_idx, column=1, padx=2)
        row_data["units"].grid(row=row_idx, column=2, padx=2)
        row_data["lcg"].grid(row=row_idx, column=3, padx=2)
        row_data["tcg"].grid(row=row_idx, column=4, padx=2)
        row_data["vcg"].grid(row=row_idx, column=5, padx=2)

        def delete_load_row():
            for widget in row_data.values():
                widget.grid_forget()
            delete_btn.grid_forget()
            add_weights.remove(row_data)
            reposition_add_load_button()

        delete_btn = tk.Button(add_weights_frame, text="❌", command=delete_load_row, fg="red")
        delete_btn.grid(row=row_idx, column=6, padx=2)
        row_data["delete_btn"] = delete_btn

        add_weights.append(row_data)
        reposition_add_load_button()

    add_load_button = tk.Button(add_weights_frame, text="➕ Add Weight", command=add_load_row)
    add_load_button.grid(row=1, column=0, columnspan=6, pady=5)

    # === TANKS SECTION ===
    tk.Label(tab_loads, text="Tanks:", font=("Arial",10,"bold")).pack(pady=(20,5))
    load_tanks_frame = tk.Frame(tab_loads)
    load_tanks_frame.pack()

    load_tanks = []
    fsm_tanks_list = []

    def reposition_load_tank_button():
        """Repositions the 'Add Tank' button based on the number of tanks."""
        idx = len(load_tanks) + 1
        load_tank_button.grid_forget()
        load_tank_button.grid(row=idx, column=0, columnspan=2, pady=5)

    def load_add_tank_row():
        """Adds a new tank row to the Loads tab."""
        if len(load_tanks) == 0:
            tk.Label(load_tanks_frame, text="Name",
                    font=("Arial",10,"bold")).grid(row=0, column=0, padx=5)
            tk.Label(load_tanks_frame, text="Contents",
                    font=("Arial",10,"bold")).grid(row=0, column=1, padx=5)

        row = len(load_tanks) + 1
        name_ent = tk.Entry(load_tanks_frame, width=15)
        contents_var = tk.StringVar(value="Gasoline")
        contents_dd  = ttk.Combobox(
            load_tanks_frame, textvariable=contents_var,
            values=["Gasoline","Diesel","Fresh Water","Sewage","Bait"],
            state="readonly", width=12
        )

        name_ent.grid(row=row, column=0, padx=5)
        contents_dd.grid(row=row, column=1, padx=5)

        def delete_tank():
            name_ent.grid_forget()
            contents_dd.grid_forget()
            delete_btn.grid_forget()
            # find and remove
            for i, t in enumerate(load_tanks):
                if t["name_widget"] is name_ent:
                    load_tanks.pop(i)
                    fsm_tanks_list.pop(i)
                    break
            reposition_load_tank_button()

        delete_btn = tk.Button(load_tanks_frame, text="❌", command=delete_tank, fg="red")
        delete_btn.grid(row=row, column=2, padx=5)

        load_tanks.append({"name_widget": name_ent, "contents_var": contents_var})
        fsm_tanks_list.append(name_ent.get().strip() or f"TANK{row}")
        reposition_load_tank_button()

    load_tank_button = tk.Button(load_tanks_frame, text="➕ Add Tank", command=load_add_tank_row)
    load_tank_button.grid(row=1, column=0, columnspan=2, pady=5)

    # === TANK MODEL TOGGLE ===
    # BooleanVar default True (checked)
    tank_model_var = tk.BooleanVar(value=True)

    def toggle_tank_model_field():
        """Show the Free Surface Moment field only when unchecked."""
        if not tank_model_var.get():
            tank_model_frame.pack(pady=(5, 0))
        else:
            tank_model_frame.pack_forget()   # <-- use pack_forget()

    # Checkbutton itself
    tank_chk = tk.Checkbutton(
        tab_loads,
        text="Vessel has tank model",
        variable=tank_model_var,
        command=toggle_tank_model_field
    )
    tank_chk.pack(pady=(20, 5))

    # Frame for the Free Surface Moment input (hidden by default)
    tank_model_frame = tk.Frame(tab_loads)

    tk.Label(tank_model_frame, text="Free Surface Moment:").grid(row=0, column=0, padx=10)
    fs_entry = tk.Entry(tank_model_frame, width=12)
    fs_entry.grid(row=1, column=0, padx=10)

    # Initialize visibility correctly
    toggle_tank_model_field()

    return tab_loads, {
    #Passegers
    "pax_count_entry": pax_count_entry,
    "pax_weight_entry": pax_weight_entry,
    "pax_lcg_entry": pax_lcg_entry,
    "pax_tcg_entry": pax_tcg_entry,
    "pax_vcg_entry": pax_vcg_entry,
    #additional weights
    "add_weights": add_weights,
    #Tanks
    "load_tanks": load_tanks,
    "fsm_tanks_list": fsm_tanks_list,
    #FSM
    "tank_model_var": tank_model_var,
    "fs_entry": fs_entry
}
