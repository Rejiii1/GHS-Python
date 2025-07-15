import tkinter as tk
from tkinter import ttk

def create_lightship_tab(notebook):
    tab_lightship = tk.Frame(notebook)
    notebook.add(tab_lightship, text="Lightship")

    survey_var = tk.StringVar(value="Select a survey type")
    survey_label_to_value = {
        "Deadweight Survey": "1",
        "Inclining Experiment": "2",
        "User Defined Lightship": "3"
    }
    survey_options = list(survey_label_to_value.keys())

    survey_dropdown = ttk.Combobox(tab_lightship, textvariable=survey_var, values=survey_options, state="readonly")
    tk.Label(tab_lightship, text="Survey Type:").pack(pady=(10, 0))
    survey_dropdown.pack()

    dynamic_frame = tk.Frame(tab_lightship)
    dynamic_frame.pack(pady=10)

    # You can keep these as function attributes so you can access them later
    create_lightship_tab.excel_text = None
    create_lightship_tab.vert_entry = None
    create_lightship_tab.gmmt_entry = None
    create_lightship_tab.disp_entry = None
    create_lightship_tab.ltsh_lcg_entry = None
    create_lightship_tab.ltsh_tcg_entry = None
    create_lightship_tab.ltsh_vcg_entry = None
    create_lightship_tab.unit_var = None

    def update_dynamic_fields(*args):
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        selection = survey_var.get()
        if selection in ["Deadweight Survey", "Inclining Experiment"]:
            tk.Label(dynamic_frame, text="Paste Excel Data:").pack()
            create_lightship_tab.excel_text = tk.Text(dynamic_frame, height=6, width=40)
            create_lightship_tab.excel_text.pack()

            if selection == "Deadweight Survey":
                tk.Label(dynamic_frame, text="Conservative VCG:").pack()
                create_lightship_tab.vert_entry = tk.Entry(dynamic_frame, width=20)
                create_lightship_tab.vert_entry.pack()

            if selection == "Inclining Experiment":
                tk.Label(dynamic_frame, text="a from MOMTAN (ft-LT):").pack()
                create_lightship_tab.gmmt_entry = tk.Entry(dynamic_frame, width=20)
                create_lightship_tab.gmmt_entry.pack()

        elif selection == "User Defined Lightship":
            entry_frame = tk.Frame(dynamic_frame)
            entry_frame.pack()

            create_lightship_tab.unit_var = tk.StringVar(value="LB")

            tk.Label(entry_frame, text="Displacement").grid(row=0, column=0)
            tk.Label(entry_frame, text="Units").grid(row=0, column=1)
            tk.Label(entry_frame, text="LCG").grid(row=0, column=2)
            tk.Label(entry_frame, text="TCG").grid(row=0, column=3)
            tk.Label(entry_frame, text="VCG").grid(row=0, column=4)

            create_lightship_tab.disp_entry = tk.Entry(entry_frame, width=10)
            unit_dropdown = ttk.Combobox(entry_frame, textvariable=create_lightship_tab.unit_var,
                                         values=["LB", "LT"], state="readonly", width=6)
            create_lightship_tab.ltsh_lcg_entry = tk.Entry(entry_frame, width=10)
            create_lightship_tab.ltsh_tcg_entry = tk.Entry(entry_frame, width=10)
            create_lightship_tab.ltsh_vcg_entry = tk.Entry(entry_frame, width=10)

            create_lightship_tab.disp_entry.grid(row=1, column=0)
            unit_dropdown.grid(row=1, column=1)
            create_lightship_tab.ltsh_lcg_entry.grid(row=1, column=2)
            create_lightship_tab.ltsh_tcg_entry.grid(row=1, column=3)
            create_lightship_tab.ltsh_vcg_entry.grid(row=1, column=4)

    survey_var.trace_add("write", update_dynamic_fields)

    # === INITIAL WEIGHTS ===
    initial_weights = []
    header_created = False
    weights_frame = tk.Frame(tab_lightship)
    weights_frame.pack()

    def reposition_add_button():
        row_idx = len(initial_weights) + 1
        add_button.grid_forget()
        add_button.grid(row=row_idx, column=0, columnspan=8, pady=5)

    def add_weight_row():
        nonlocal header_created

        if not header_created:
            header = ["Action", "Item Name", "Weight", "Units", "LCG", "TCG", "VCG", ""]
            for col, label in enumerate(header):
                tk.Label(weights_frame, text=label, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
            header_created = True

        row_idx = len(initial_weights) + 1

        row_data = {
            "action": ttk.Combobox(weights_frame, values=["ADD", "REMOVE"], width=6, state="readonly"),
            "item": tk.Entry(weights_frame, width=12),
            "weight": tk.Entry(weights_frame, width=8),
            "units": ttk.Combobox(weights_frame, values=["LB", "LT"], width=6, state="readonly"),
            "initial_wt_lcg": tk.Entry(weights_frame, width=8),
            "initial_wt_tcg": tk.Entry(weights_frame, width=8),
            "initial_wt_vcg": tk.Entry(weights_frame, width=8)
        }
        row_data["action"].set("ADD")
        row_data["units"].set("LB")

        row_data["action"].grid(row=row_idx, column=0, padx=2)
        row_data["item"].grid(row=row_idx, column=1, padx=2)
        row_data["weight"].grid(row=row_idx, column=2, padx=2)
        row_data["units"].grid(row=row_idx, column=3, padx=2)
        row_data["initial_wt_lcg"].grid(row=row_idx, column=4, padx=2)
        row_data["initial_wt_tcg"].grid(row=row_idx, column=5, padx=2)
        row_data["initial_wt_vcg"].grid(row=row_idx, column=6, padx=2)

        def delete_row():
            for widget in row_data.values():
                widget.grid_forget()
            delete_btn.grid_forget()
            initial_weights.remove(row_data)
            reposition_add_button()

        delete_btn = tk.Button(weights_frame, text="❌", command=delete_row, fg="red")
        delete_btn.grid(row=row_idx, column=7, padx=2)
        row_data["delete_btn"] = delete_btn

        initial_weights.append(row_data)
        reposition_add_button()

    add_button = tk.Button(weights_frame, text="➕ Add Initial Weight", command=add_weight_row)
    add_button.grid(row=1, column=0, columnspan=8, pady=5)

    # === INITIAL TANKS ===
    contents_to_sg = {
        "Gasoline": "0.74",
        "Fresh Water": "1.00",
        "Sewage": "1.025",
        "Diesel": "0.85",
        "Bait": "1.025"
    }

    initial_tanks = []
    tank_header_created = False
    ltsh_tanks_frame = tk.Frame(tab_lightship)
    ltsh_tanks_frame.pack(pady=(20, 0))

    def reposition_ltsh_tank_button():
        row_idx = len(initial_tanks) + 1
        ltsh_tank_button.grid_forget()
        ltsh_tank_button.grid(row=row_idx, column=0, columnspan=4, pady=5)

    def ltsh_add_tank_row():
        nonlocal tank_header_created

        if not tank_header_created:
            header = ["Tank Name", "Contents", "Specific Gravity", "Load"]
            for col, label in enumerate(header):
                tk.Label(ltsh_tanks_frame, text=label, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=4, pady=2)
            tank_header_created = True

        row_idx = len(initial_tanks) + 1

        name_entry = tk.Entry(ltsh_tanks_frame, width=15)
        contents_var = tk.StringVar()
        contents_dropdown = ttk.Combobox(ltsh_tanks_frame, textvariable=contents_var,
                                         values=list(contents_to_sg.keys()) + ["Other"], state="readonly", width=12)
        sg_entry = tk.Entry(ltsh_tanks_frame, width=10)
        load_entry = tk.Entry(ltsh_tanks_frame, width=10)

        def on_contents_change(*args):
            selected = contents_var.get()
            if selected in contents_to_sg:
                sg_entry.config(state="normal")
                sg_entry.delete(0, tk.END)
                sg_entry.insert(0, contents_to_sg[selected])
                sg_entry.config(state="disabled")
            else:
                sg_entry.config(state="normal")

        contents_var.trace_add("write", on_contents_change)
        contents_var.set("Gasoline")

        name_entry.grid(row=row_idx, column=0, padx=2)
        contents_dropdown.grid(row=row_idx, column=1, padx=2)
        sg_entry.grid(row=row_idx, column=2, padx=2)
        load_entry.grid(row=row_idx, column=3, padx=2)

        def delete_tank_row():
            for widget in (name_entry, contents_dropdown, sg_entry, load_entry, delete_btn):
                widget.grid_forget()
            initial_tanks.remove(row_data)
            reposition_ltsh_tank_button()

        delete_btn = tk.Button(ltsh_tanks_frame, text="❌", command=delete_tank_row, fg="red")
        delete_btn.grid(row=row_idx, column=4, padx=2)

        row_data = {
            "name": name_entry,
            "contents": contents_var,
            "sg": sg_entry,
            "load": load_entry,
            "delete_btn": delete_btn
        }

        initial_tanks.append(row_data)
        reposition_ltsh_tank_button()

    ltsh_tank_button = tk.Button(ltsh_tanks_frame, text="➕ Add Initial Tank", command=ltsh_add_tank_row)
    ltsh_tank_button.grid(row=1, column=0, columnspan=4, pady=5)

    # Return references to useful widgets and lists for external access
    return {
        "tab": tab_lightship,
        "survey_var": survey_var,
        "survey_label_to_value": survey_label_to_value,
        "excel_text": create_lightship_tab.excel_text,
        "vert_entry": create_lightship_tab.vert_entry,
        "gmmt_entry": create_lightship_tab.gmmt_entry,
        "disp_entry": create_lightship_tab.disp_entry,
        "ltsh_lcg_entry": create_lightship_tab.ltsh_lcg_entry,
        "ltsh_tcg_entry": create_lightship_tab.ltsh_tcg_entry,
        "ltsh_vcg_entry": create_lightship_tab.ltsh_vcg_entry,
        "unit_var": create_lightship_tab.unit_var,
        "initial_weights": initial_weights,
        "initial_tanks": initial_tanks
    }
