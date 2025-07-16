


# content‑to‑percent for each macro tank stage
load_patterns = {
    "Departure": {"default": "MACRO TANK1",
                  "load": {"Gasoline":0.95, "Diesel":0.95, "Fresh Water":0.95, "Bait":0.95, "Sewage":0.10}},
    "Midway":    {"default": "MACRO TANK2",
                  "load": {"Gasoline":0.50, "Diesel":0.50, "Fresh Water":0.50, "Bait":0.50, "Sewage":0.50}},
    "Arrival":   {"default": "MACRO TANK3",
                  "load": {"Gasoline":0.10, "Diesel":0.10, "Fresh Water":0.10, "Bait":0.10, "Sewage":0.95}}
}

# Content types and their default specific gravity
contents_to_sg = {
    "Gasoline": "0.74",
    "Fresh Water": "1.00",
    "Sewage": "1.025",
    "Diesel": "0.85",
    "Bait": "1.025"
}