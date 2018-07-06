import pandas as pd
import re

# FORMAT VERSION MODEL NUMBER
def format_allergan(vmn):
    try:
        return vmn[:vmn.index('-')], vmn[vmn.index('-'):]
    except ValueError as e:
        raise ValueError("Allergan versionModelNumber format unknown: ", e)

def format_ideal(vmn):
    return str(vmn)[:3], str(vmn)[3:]

def format_mentor(vmn):
    return (vmn[:3] + vmn[7:], vmn[3:7]) if not re.search("[A-Z]{4}", vmn) \
           else (re.search("[A-Z]{4}", vmn).group(), vmn.replace(re.search("[A-Z]{4}", vmn).group(), ""))

def format_sientra(vmn):
    try:
        return vmn[:vmn.index('-')] + vmn[re.search("[a-zA-Z]", vmn).start():], \
               vmn[vmn.index('-'):re.search("[a-zA-Z]", vmn).start()]
    except ValueError as e:
        raise ValueError("Sientra versionModelNumber format unknown: ", e)

# FORMAT SIZE TEXT
def format_mentor_st(dev_desc):
    st = re.search(r"\d{3,}[c]{2}", str(dev_desc)) # search pattern: "###cc" (at least three #s)
    return st.group()[:3] + " " + st.group()[3:] if st else ""

# def format_allergan_st(st):
#     return st

def format_ideal_st(size_text):
    st = re.search(r"\d{3,}\s[c]{2}", str(size_text)) # search pattern "### cc" (at least three #s)
    return st.group() if st else ""

def format_sientra_st(size_text):
    st = re.search(r"\d{3,}\s[c]{2}", str(size_text)) # search pattern "### cc" (at least three #s)
    return st.group() if st else ""

# MAIN FUNCTION
def formatted_data(df):
    sheet = df

    # remove diaphragm or injection dome rows
    anomalies = [i for i, bn in zip(sheet.index.values, sheet.brandName) if bn.find("Diaphragm Valve") != -1 or bn.find("Injection Domes") != -1]
    sheet = sheet.drop(anomalies)

    style_col = []
    rest_col = []

    # take versionModelNumbers and extract main style (determined from looking at catalogs)
    for pdi, vmn, cn in zip(sheet["PrimaryDI"], sheet["versionModelNumber"], sheet["companyName"]):
        vmn = str(vmn) # convert all #'s to strings

        if cn == "MENTOR TEXAS L.P.":
            style, rest = format_mentor(vmn)
            style_col.append(style)
            rest_col.append(rest)
        elif cn == "Allergan, Inc.":
            style, rest = format_allergan(vmn)
            style_col.append(style)
            rest_col.append(rest)
        elif cn == "Sientra, Inc.":
            style, rest = format_sientra(vmn)
            style_col.append(style)
            rest_col.append(rest)
        elif cn == "IDEAL IMPLANT INCORPORATED":
            style, rest = format_ideal(vmn)
            style_col.append(style)
            rest_col.append(rest)
        else:
            raise ValueError(f"Unknown companyName found at PrimaryDI: {pdi}")

    # insert columns
    sheet.insert(loc=3, column="style", value=style_col)
    sheet.insert(loc=4, column="rest", value=rest_col)

    new_st_col = []
    for cn, size_text, dev_desc in zip(sheet["companyName"], sheet["sizeText"], sheet["deviceDescription"]):
        if cn == "MENTOR TEXAS L.P.":
            new_st_col.append(format_mentor_st(dev_desc))
        elif cn == "Allergan, Inc.":
            new_st_col.append(size_text) # already properly formatted
        elif cn == "Sientra, Inc.":
            new_st_col.append(format_sientra_st(size_text))
        elif cn == "IDEAL IMPLANT INCORPORATED":
            new_st_col.append(format_ideal_st(size_text))
        else:
            raise ValueError(f"""Improperly formatted text.\n 
                                cn: {cn}\n
                                size_text: {size_text}\n
                                dev_desc: {dev_desc}""")

    # replace column
    sheet["sizeText"] = new_st_col
    return sheet


if __name__ == "__main__":
    df = pd.read_excel("../2 Data/rel_cols.xlsx", sheet_name="rel_cols")
    sheet = formatted_data(df)
    sheet.to_csv("formatted_cols.csv", sep=",")
