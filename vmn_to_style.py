import pandas as pd
import re


def format_allergan(vmn):
    try:
        return vmn[:vmn.index('-')]
    except ValueError as e:
        pass


def format_ideal(vmn):
    return str(vmn)[:3]


def format_mentor(vmn):
    return str(vmn)[:4]


def format_sientra(vmn):
    try:
        return vmn[:vmn.index('-')] + vmn[re.search("[a-zA-Z]", vmn).start():]
    except ValueError as e:
        pass


sheet = pd.read_excel("rel_cols.xlsx", sheet_name="rel_cols")

# remove diaphragm or injection dome rows
anomalies = [i for i, bn in zip(sheet.index.values, sheet.brandName) if bn.find("Diaphragm Valve") != -1 or bn.find("Injection Domes") != -1]
sheet = sheet.drop(anomalies)

style_col = []
for pdi, vmn, cn in zip(sheet["PrimaryDI"], sheet["versionModelNumber"], sheet["companyName"]):
    if cn == "Allergan, Inc.":
        style_col.append(format_allergan(vmn))
    elif cn == "IDEAL IMPLANT INCORPORATED":
        style_col.append(format_ideal(vmn))
    elif cn == "MENTOR TEXAS L.P.":
        style_col.append(format_mentor(vmn))
    elif cn == "Sientra, Inc.":
        style_col.append(format_sientra(vmn))
    else:
        raise ValueError(f"Improperly formatted column found at PrimaryDI: {pdi}")

sheet.insert(loc=3, column="style", value=style_col)
