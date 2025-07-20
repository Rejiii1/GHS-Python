# ⚓ GHS Run File Creator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/Tkinter-GUI-lightgrey?logo=python)](https://docs.python.org/3/library/tkinter.html)
[![Status](https://img.shields.io/badge/status-alpha-orange)]()

A Tkinter-based GUI to help marine engineers and naval architects quickly generate run files (`.rf`) for [General Hydrostatics (GHS)](https://www.ghsport.com/), a hydrostatics and stability analysis program.

---

## 🚀 Features

### 🧾 Tabbed GUI Interface
Organized into task-specific tabs:
- 📄 **Report Details** – Set hull name, beam, length, route, and other metadata.
- ⚖️ **Lightship** – Choose survey type, paste Excel output, define lightship weight and CGs.
- 🏋️‍♂️ **Initial Weights** – Add custom load items with units and CGs.
- 🛢️ **Initial Tanks** – Define tanks with contents, SG, and load percentage.
- 📦 **Loads** – Apply FSM tank lists and macros for:
  - **Departure**, **Midway**, and **Arrival**
  - Auto-loads based on tank contents (`Gasoline`, `Diesel`, `Water`, etc.)
- 🧭 **Intact Stability** – Choose vessel type and route, add passenger and additional weight data.
- 💥 **Damage Stability** – Add compartments and flooding zones to simulate damaged conditions.

### 📐 Pontoon Crowding
- Support for 2 sqft and 5 sqft per-person crowding layouts.
- Generates LCG/TCG/HEAD variables and `pontoon.lib` macro file for each zone.

### 🧰 Template-Based Output
- Uses customizable templates:  
  `ls_temp.txt`, `load_temp.txt`, `int_temp.txt`, `dam_temp.txt`, `pontoon_temp.txt`
- Auto-fills variables like `{{hull}}`, `{{fsm_tanks}}`, `{{lcg105}}` from GUI input.
- Exports `.rf` and `.lib` files to the `/generated/` folder.

---

## 🧰 Requirements

- Python **3.8+**
- No external libraries needed (uses standard library `tkinter`)

---

## 🔧 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Rejiii1/GHS-Python.git
   cd GHS-Python
   ```

2. Run the program:
   ```bash
   python main.py
   ```

3. Fill out each relevant tab.

4. Click **"Generate Run File"**  
   The final `.rf` and `.lib` files will be saved to the `generated/` folder.

---

## 🧱 File Structure

```
GHS-Python/
├── templates/         # Input templates used for each section
├── generated/         # Output folder for run files
├── gui/               # GUI layout and tab modules
├── logic/             # Logic for filling templates, loading data
├── main.py            # Entry point for launching the app
└── README.md
```

---

## 👨‍💻 About the Author

Hi! I’m [Trip Jackson](https://www.linkedin.com/in/robert-jackson-35ba4624a/), a Coast Guard engineer and naval architect.  
I built this tool to streamline GHS run file creation for internal use, and decided to make it public for anyone in the marine industry who might find it useful.

---

## 📜 License

This project is licensed under the **MIT License** – free to use, modify, and share.
