# plt2latex/units.py

_UNIT_TO_PT = {
    "pt": 1.0,
    "bp": 1.00375,
    "in": 72.27,
    "cm": 28.45,
    "mm": 2.845,
}

def parse_unit(s: str, to: str = "pt") -> float:
    """
    Преобразует строку с единицей измерения (например, "12cm", "14pt", "1.5in")
    в числовое значение в указанных единицах (`to = 'pt'` или `to = 'in'`).
    """
    if isinstance(s, (int, float)):
        return float(s)

    import re
    match = re.fullmatch(r"\s*([0-9.]+)\s*([a-zA-Z]+)\s*", s)
    if not match:
        raise ValueError(f"Invalid unit format: '{s}'")

    value, unit = match.groups()
    value = float(value)
    unit = unit.lower()

    if unit not in _UNIT_TO_PT:
        raise ValueError(f"Unsupported unit '{unit}'")

    pt = value * _UNIT_TO_PT[unit]

    if to == "pt":
        return pt
    elif to == "in":
        return pt / _UNIT_TO_PT["in"]
    else:
        raise ValueError(f"Unsupported conversion target: '{to}'")