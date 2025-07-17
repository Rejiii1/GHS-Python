# tab_pontoon.py

import tkinter as tk

def build_pontoon_tab(notebook):
    """
    Adds the Pontoon tab to the notebook and returns the tab widget and associated data.
    """
    pontoon_tab = tk.Frame(notebook)
    notebook.add(pontoon_tab, text="Pontoon")

    # === PASSENGER CROWDING ===
    tk.Label(pontoon_tab, text="Passenger Crowding", font=("Arial", 12, "bold")) \
        .pack(pady=(10, 5))

    load_cases = [
        ("Bow",         (0, 1)),
        ("Port Bow",    (1, 1)),
        ("Port",        (1, 0)),
        ("Port Quarter",(1, 2)),
        ("Stern",       (0, 2)),
        ("Stbd Quarter",(2, 2)),
        ("Stbd",        (2, 0)),
        ("Stbd Bow",    (2, 1)),
    ]

    def make_crowd_table(rows_per_passenger):
        crowd_frame = tk.Frame(pontoon_tab)
        crowd_frame.pack(pady=5)
        title = f"{rows_per_passenger} sqft per Passenger"
        tk.Label(crowd_frame, text=title, font=("Arial", 10, "italic")) \
            .grid(row=0, column=0, columnspan=4)

        headers = ["Crowding", "LCG", "TCG", "Pax in Head"]
        for c, h in enumerate(headers):
            tk.Label(crowd_frame, text=h, font=("Arial", 9, "bold")) \
                .grid(row=1, column=c, padx=5)

        entries = []
        for r, (name, (h_code, v_code)) in enumerate(load_cases, start=2):
            tk.Label(crowd_frame, text=name).grid(row=r, column=0, padx=5)
            e_lcg = tk.Entry(crowd_frame, width=8)
            e_lcg.grid(row=r, column=1)
            e_tcg = tk.Entry(crowd_frame, width=8)
            e_tcg.grid(row=r, column=2)
            b_head = tk.BooleanVar(value=False)
            tk.Checkbutton(crowd_frame, variable=b_head).grid(row=r, column=3)

            code = f"{h_code}{v_code}{2 if rows_per_passenger == 2 else 5}"
            entries.append({
                "code": code,
                "lcg": e_lcg,
                "tcg": e_tcg,
                "head": b_head
            })
        return entries

    crowd2_entries = make_crowd_table(2)
    crowd5_entries = make_crowd_table(5)

    # === HEAD LOCATION ===
    tk.Label(pontoon_tab, text="Head Location", font=("Arial", 12, "bold")) \
        .pack(pady=(15, 5))
    hl_frame = tk.Frame(pontoon_tab)
    hl_frame.pack(pady=5)
    tk.Label(hl_frame, text="LCG").grid(row=0, column=0, padx=10)
    tk.Label(hl_frame, text="TCG").grid(row=0, column=1, padx=10)
    headlcg_entry = tk.Entry(hl_frame, width=10)
    headlcg_entry.grid(row=1, column=0, padx=10)
    headtcg_entry = tk.Entry(hl_frame, width=10)
    headtcg_entry.grid(row=1, column=1, padx=10)

    # Return the tab and any widgets you want to access later
    return pontoon_tab, {
        "crowd2": crowd2_entries,
        "crowd5": crowd5_entries,
        "headlcg_entry": headlcg_entry,
        "headtcg_entry": headtcg_entry
    }
