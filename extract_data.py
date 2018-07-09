import pandas as pd
import numpy as np
from ast import literal_eval

### WANT TO KNOW
#   - brand name
#   - style
#   - filling
#   - manufacturer
#   - product code
#   - profile
#   - shape
#   - shell
#   - shell surface

# classifications
# PrimaryDI | manufacturer | brand | style | filling | profile | shape | shell | shell surface | product code |

# annotations
# PrimaryDI | versionModelNumber | catalogNumber | deviceID (GUDID) | 


def extract_manufacturer(company_name):
    company_name = company_name.lower()

    if "mentor" in company_name:
        return "Mentor"
    elif "allergan" in company_name:
        return "Allergan"
    elif "ideal" in company_name:
        return "Ideal Implant"
    elif "sientra" in company_name:
        return "Sientra"
    else:
        return "UNKNOWN MANUFACTURER NAME"

def extract_filling(brand_name, product_code):
    if product_code == "FWM":   # IDEAL IMPLANT
        return "saline filling"

    brand_name = brand_name.lower()
    if "memorygel" in brand_name:
        return "MENTOR MemoryGel silicone filling"                   # MENTOR
    elif "memoryshape" in brand_name:
        return "MENTOR MemoryShape silicone filling"
    elif "inspira softtouch" in brand_name:
        return "NATRELLE INSPIRA SoftTouch silicone filling"         # NATRELLE
    elif "inspira cohesive" in brand_name:
        return "NATRELLE INSPIRA Cohesive silicone filling"
    elif "inspira" in brand_name:
        return "NATRELLE INSPIRA silicone filling"
    elif "410 highly cohesive" in brand_name:
        return "NATRELLE 410 Highly Cohesive silicone filling"
    elif "natrelle silicone-filled" in brand_name:
        return "NATRELLE Silicone Gel silicone filling"
    elif "sientra" in brand_name:
        return "SIENTRA Silicone Gel silicone filling"               # SIENTRA
    else:
        raise ValueError(f"UNKNOWN BRAND NAME: {brand_name}")

def extract_profile_shape_surface_mentor(dev_desc, product_code, brand):
    info = {
        "profile": "",
        "shape"  : "",
        "surface": ""
    }
    profiles = ["moderate classic", "moderate plus",        # moderate plus must be in front of moderate
                "moderate", "moderate plus profile xtra",
                "high", "high profile xtra", "ultra high"]
    # shapes = ["round", "teardrop"]
    # surfaces = ["smooth", "siltex"]
    dev_desc = dev_desc.lower()
    brand = brand.lower()

    error_str = "Unknown"
    if product_code == "FTR":
        for p in profiles:
            if p in dev_desc:
                info["profile"] =  "MENTOR " + p + (" profile" if not "profile" in p else "")
        if info["profile"] == "":
            error_str += f" profile: {dev_desc},"
        if "memorygel" in brand or "memorygel xtra" in brand:
            info["shape"] = "round shape"
            if "smooth" in dev_desc:
                info["surface"] = "smooth shell surface"
            elif "siltex" in dev_desc:
                info["surface"] = "MENTOR SILTEX textured shell surface"
            else:
                error_str += f" surface: {dev_desc}"
        elif "memoryshape" in brand:
            info["shape"] = "MENTOR teardrop shape"
            info["surface"] = "MENTOR SILTEX textured shell surface"
        else:
            error_str += f" shape: {brand}, surface: {dev_desc},"
    elif product_code == "FWM":
        for p in profiles:
            if p in brand:
                info["profile"] =  "MENTOR " + p + (" profile" if not "profile" in p else "")

        # source: http://www.mentorwwllc.com/Documents/saline_spectrum_ppi.pdf
        if "spectrum" in brand:
            if "round" in brand:
                info["profile"] = "MENTOR moderate profile"
            elif "contour profile" in brand:
                info["profile"] = "MENTOR high profile"
                
        if info["profile"] == "":
            error_str += f" profile: {dev_desc},"

        if "round" in brand:
            info["shape"] = "round shape"
        elif "contour profile" in brand:
            info["shape"] = "MENTOR CONTOUR PROFILE shape"
        else:
            error_str += f" shape: {brand}"

        if "smooth" in brand:
                info["surface"] = "smooth shell surface"
        elif "siltex" in brand:
            info["surface"] = "MENTOR SILTEX textured shell surface"
        else:
            error_str += f" surface: {brand}"
    else:
        error_str += f" product code: {product_code}"

    if error_str != "Unknown":
        raise ValueError(error_str)
    
    return info


def extract_profile_shape_surface_allergan(style):
    styles_dict = literal_eval(open("natrelle_style_dict.txt").read())
    info = {
        "profile": "",
        "shape"  : "",
        "surface": ""
    }

    if style in styles_dict:
        info["profile"] = "NATRELLE " + profiles_dict[style]["profile"]
        info["shape"] = "NATRELLE " + profiles_dict[style]['shape'
                           ] if 'Anatomical' in profiles_dict[style]['shape'
                           ] else profiles_dict[style]['shape']
        info['surface'] = ('NATRELLE ' + profiles_dict[style]['surface'
                           ] if 'BIOCELL' in profiles_dict[style]['surface'
                           ] else profiles_dict[style]['surface'])
    else:
        raise ValueError(f"Unknown NATRELLE style: {style}")

    return info


def extract_profile_shape_surface_sientra(dev_desc):
    info = {
        "profile": "",
        "shape"  : "",
        "surface": ""
    }
    dev_desc = dev_desc.lower()

    profiles = ["low profile", "moderate profile",
                "moderate plus profile", "moderate high profile",
                "high profile"]
    shapes = ["round", "shaped classic base", "shaped round base", "shaped oval base"]
    # surfaces = smooth, textured

    error_str = "Unknown"
    flag = False
    for p in profiles:
        if p in dev_desc:
            info["profile"] = "SIENTRA " + p
            flag = True
    if not flag:
         error_str = "profile"
    
    flag = False
    for s in shapes:
        if s in dev_desc:
            info["shape"] = "SIENTRA" + s + "shape"
            flag = True
    if not flag:
        error_str += ", shape"
    
    if "smooth" in dev_desc:
        info["surface"] = "smooth shell surface"
    elif "textured" in dev_desc:
        info["surface"] = "textured shell surface"
    else:
        error_str += ", shell surface"

    if error_str != "Unknown":
        raise ValueError(error_str + f" in dev_desc: {dev_desc}")
    
    return info


# Ideal Implant only has one "profile": high profile
# source: https://www.yorkyates.com/plastic-surgery-procedures-utah/breast-surgery-utah/breast-augmentation/ideal-implant-breast-implant/
# Ideal Implant is also only round and smooth
def extract_profile_shape_surface_ideal():
    info = {
        "profile": "high profile",
        "shape"  : "round shape",
        "surface": "smooth shell surface"
    }
    return info




sheet = pd.read_excel("formatted_cols.xlsx", sheet_name="formatted_cols")

# classification columns
p_di_col, manufacturer_col, brand_col, style_col, filling_col, profile_col, shape_col, shell_col, shell_surface_col, product_code_col, size_col = ([],)*11
# assign classification column values
for p_di, c_name, brand, p_code, dev_desc, style, size in zip(sheet['PrimaryDI'], sheet['companyName'], sheet['brandName'], sheet['productCode'], sheet['deviceDescription'], sheet['style'], sheet['sizeText']):

    p_di_col.append(p_di)
    manufacturer_col.append(extract_manufacturer(c_name))
    brand_col.append(brand)
    filling_col.append(extract_filling(brand, p_code))
    style_col.append(style)
    shell_col.append("silicone shell")

    brand = brand.lower()
    info = {}
    if "allergan" in brand:
        info = extract_profile_shape_surface_allergan(style)
    elif "mentor" in brand:
        info = extract_profile_shape_surface_mentor(dev_desc, p_code, brand)
    elif "sientra" in brand:
        info = extract_profile_shape_surface_sientra(dev_desc)
    else:
        info = extract_profile_shape_surface_ideal()

    profile_col.append(info["profile"])
    shape_col.append(info["shape"])
    shell_surface_col.append(info["surface"])

    product_code_col.append(p_code)
    size_col.append(size)

# annotation columns
vmn_col, ctg_num_col, dev_desc_col, dev_id_col = ([],)*4
# assign annotation column values
for vmn, ctg_num, dev_desc, dev_id in zip(sheet["versionModelNumber"], sheet["catalogNumber"], sheet["deviceDescription"], sheet["deviceId"]):
    vmn_col.append(vmn)
    ctg_num_col.append(ctg_num)
    dev_desc_col.append(dev_desc)
    dev_id_col.append(dev_id)

classifications_sheet = pd.DataFrame(np.column_stack([p_di_col, manufacturer_col, brand_col, style_col, filling_col, profile_col, size_col, shape_col, shell_col, shell_surface_col, product_code_col]), \
                                     columns=['primary_di', 'manufacturer', 'brand', 'style', 'filling', 'profile', 'size', 'shape', 'shell', 'shell surface', 'product_code'])
annotations_sheet = pd.DataFrame(np.column_stack([p_di_col, vmn_col, ctg_num_col, dev_desc_col, dev_id_col]), \
                                 columns=['primary_di', 'version_model_number', 'catalog_number', 'device_description', 'device_id'])
