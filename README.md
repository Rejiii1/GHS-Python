# ⚓ GHS Run File Creator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/Tkinter-GUI-lightgrey?logo=python)](https://docs.python.org/3/library/tkinter.html)
[![Status](https://img.shields.io/badge/status-alpha-orange)]()

A simple Tkinter-based GUI to help marine engineers and naval architects quickly generate run files (`.rf`) for [General Hydrostatics (GHS)](https://www.ghsport.com/) stability analysis.

---

## 🚀 Features

- **Tabbed Interface** organized by task:
  - 📄 **Report Details** – Set geometry file name and other report info.
  - ⚖️ **Lightship** – Select survey type, paste Excel data, define user lightship, and manage initial weights and tanks.
  - ⚙️ **Loads** – *(Coming soon!)*
  - 🧭 **Intact Stability** – Set vessel type and route.

- **Dynamic Fields** for each survey type:
  - Deadweight Survey
  - Inclining Experiment
  - User-Defined Lightship

- **Initial Weights Table**:
  - Add/remove rows with item name, weight, units, and center of gravity data.
  - Auto-grouped by units (`LB` or `LT`) during output.
 
- **Initial Tanks**:
  - Add/remove rows with tank name, contents, and load.

- **Template-Based Output**:
  - Reads from `.txt` templates (`ls_temp.txt`, `load_temp.txt`, etc.)
  - Generates `.rf` files and saves them to a `generated/` directory.

---

## 📸 Preview

> _(Insert a screenshot of the GUI here for max GitHub cred!)_

---

## 🧰 Requirements

- Python **3.8+**
- No external libraries required (just `tkinter`)

---

## 🔧 Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ghs-runfile-creator.git
   cd ghs-runfile-creator
