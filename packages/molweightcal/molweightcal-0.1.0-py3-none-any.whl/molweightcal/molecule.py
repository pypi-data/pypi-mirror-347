import re
from collections import defaultdict

ATOMIC_WEIGHTS = {
    'H': 1.008, 'He': 4.0026, 'Li': 6.94, 'Be': 9.0122, 'B': 10.81,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.085, 'P': 30.974,
    'S': 32.06, 'Cl': 35.45, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Sc': 44.956, 'Ti': 47.867, 'V': 50.942, 'Cr': 51.996, 'Mn': 54.938,
    'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693, 'Cu': 63.546, 'Zn': 65.38,
    'Ga': 69.723, 'Ge': 72.630, 'As': 74.922, 'Se': 78.971, 'Br': 79.904,
    'Kr': 83.798, 'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224,
    'Nb': 92.906, 'Mo': 95.95, 'Tc': 98.0, 'Ru': 101.07, 'Rh': 102.91,
    'Pd': 106.42, 'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71,
    'Sb': 121.76, 'Te': 127.60, 'I': 126.90, 'Xe': 131.29, 'Cs': 132.91,
    'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91, 'Nd': 144.24,
    'Pm': 145.0, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25, 'Tb': 158.93,
    'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93, 'Yb': 173.05,
    'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84, 'Re': 186.21,
    'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97, 'Hg': 200.59,
    'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209.0, 'At': 210.0,
    'Rn': 222.0, 'Fr': 223.0, 'Ra': 226.0, 'Ac': 227.0, 'Th': 232.04,
    'Pa': 231.04, 'U': 238.03, 'Np': 237.0, 'Pu': 244.0, 'Am': 243.0,
    'Cm': 247.0, 'Bk': 247.0, 'Cf': 251.0, 'Es': 252.0, 'Fm': 257.0,
    'Md': 258.0, 'No': 259.0, 'Lr': 262.0, 'Rf': 267.0, 'Db': 270.0,
    'Sg': 271.0, 'Bh': 270.0, 'Hs': 277.0, 'Mt': 276.0, 'Ds': 281.0,
    'Rg': 282.0, 'Cn': 285.0, 'Nh': 286.0, 'Fl': 289.0, 'Mc': 290.0,
    'Lv': 293.0, 'Ts': 294.0, 'Og': 294.0
}

def parse_formula(formula):
    stack = []
    current = defaultdict(int)
    i = 0
    n = len(formula)
    while i < n:
        if formula[i] == '(':
            stack.append(current)
            current = defaultdict(int)
            i += 1
        elif formula[i] == ')':
            i += 1
            multiplier = 0
            while i < n and formula[i].isdigit():
                multiplier = multiplier * 10 + int(formula[i])
                i += 1
            multiplier = multiplier if multiplier else 1
            parent = stack.pop()
            for elem, count in current.items():
                parent[elem] += count * multiplier
            current = parent
        else:
            if not formula[i].isupper():
                raise ValueError(f"Invalid element symbol at position {i}")
            element = formula[i]
            i += 1
            if i < n and formula[i].islower():
                element += formula[i]
                i += 1
            if element not in ATOMIC_WEIGHTS:
                raise ValueError(f"Unknown element: {element}")
            count = 0
            while i < n and formula[i].isdigit():
                count = count * 10 + int(formula[i])
                i += 1
            count = count if count else 1
            current[element] += count
    if stack:
        raise ValueError("Unmatched opening parenthesis")
    return dict(current)

def calculate_weight(formula):
    elements = parse_formula(formula)
    details = [f"{el}({cnt}) × {ATOMIC_WEIGHTS[el]} = {round(cnt * ATOMIC_WEIGHTS[el], 4)}"
               for el, cnt in elements.items()]
    total = round(sum(ATOMIC_WEIGHTS[el] * cnt for el, cnt in elements.items()), 4)
    return f"Molecular weight of {formula}: {total}\nDetails:\n" + "\n".join(details)

def main(formula):
    try:
        return calculate_weight(formula)
    except ValueError as e:
        return f"Invalid formula: {e}"