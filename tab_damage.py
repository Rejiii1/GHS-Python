import tkinter as tk
from tkinter import ttk

def create_damage_tab(notebook):
    tab_damage = tk.Frame(notebook)
    notebook.add(tab_damage, text="Damage Stability")

    # === General Options ===
    general_frame = tk.Frame(tab_damage)
    general_frame.pack(pady=10)

    ttk.Label(general_frame, text="Compartment Standard:", font=("Arial", 10)).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="e")
    compartment_standard_var = tk.StringVar(value="1")
    compartment_dropdown = ttk.Combobox(general_frame, textvariable=compartment_standard_var, values=["1", "2"], state="readonly", width=5)
    compartment_dropdown.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")

    oldt_var = tk.BooleanVar(value=False)
    oldt_check = ttk.Checkbutton(general_frame, text="Old T", variable=oldt_var)
    oldt_check.grid(row=0, column=2, padx=(10, 5), pady=5, sticky="w")

    # === Subdivisions Section Header ===
    ttk.Label(tab_damage, text="Floodable Subdivisions", font=("Arial", 11, "bold")).pack(pady=(15, 5))

    subdivisions_container = tk.Frame(tab_damage)
    subdivisions_container.pack()

    # === Table Headers ===
    header_frame = tk.Frame(subdivisions_container)
    header_frame.grid(row=0, column=0, columnspan=4)
    headers = ["#", "Compartment Name", "Permeability", ""]
    for col, text in enumerate(headers):
        ttk.Label(header_frame, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=10, pady=(0, 5), sticky="w")

    subdivisions_frame = tk.Frame(subdivisions_container)
    subdivisions_frame.grid(row=1, column=0, columnspan=4)

    subdivision_rows = []
    row_counter = 1

    def reposition_add_button():
        add_button.grid(row=row_counter + 2, column=0, columnspan=4, pady=10)

    def add_subdivision_row():
        nonlocal row_counter
        row_number = len(subdivision_rows) + 1

        number_label = ttk.Label(subdivisions_frame, text=str(row_number))
        name_entry = ttk.Entry(subdivisions_frame, width=30)
        permeability_entry = ttk.Entry(subdivisions_frame, width=10)
        permeability_entry.insert(0, "0.95")

        def delete_row():
            number_label.destroy()
            name_entry.destroy()
            permeability_entry.destroy()
            delete_button.destroy()
            subdivision_rows.remove(row_data)
            refresh_row_numbers()
            reposition_add_button()

        delete_button = tk.Button(subdivisions_frame, text="❌", command=delete_row, fg="red")

        number_label.grid(row=row_counter, column=0, padx=5, pady=2, sticky="w")
        name_entry.grid(row=row_counter, column=1, padx=5, pady=2, sticky="w")
        permeability_entry.grid(row=row_counter, column=2, padx=5, pady=2, sticky="w")
        delete_button.grid(row=row_counter, column=3, padx=5, pady=2, sticky="w")

        row_data = {
            "label": number_label,
            "entry": name_entry,
            "perm_entry": permeability_entry,
            "delete_button": delete_button
        }

        subdivision_rows.append(row_data)
        row_counter += 1
        reposition_add_button()

    def refresh_row_numbers():
        for i, row in enumerate(subdivision_rows, start=1):
            row["label"].config(text=str(i))

    # Add button at bottom
    add_button = tk.Button(subdivisions_container, text="➕ Add Floodable Subdivision", command=add_subdivision_row, bg="#f0f0f0")
    reposition_add_button()

    return {
        "tab": tab_damage,
        "compartment_standard_var": compartment_standard_var,
        "oldt_var": oldt_var,
        "subdivisions": subdivision_rows
    }
