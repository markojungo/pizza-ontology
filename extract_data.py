import pandas as pd
import re

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

# Proposed Column Headers Format
# Start with classifications sheet, e.g. brandName, style, filling, and end with annotations, e.g. deviceDescription

# classifications
# PrimaryDI | manufacturer | brand | style | filling | profile | shape | shell | shell surface | product code |

# annotations
# PrimaryDI | versionModelNumber | catalogNumber | deviceID (GUDID) | 


sheet = pd.read_excel("../2 Data/formatted_cols.xlsx", sheet_name="formatted_cols")
classifications_sheet = pd.DataFrame()
annotations_sheet = pd.DataFrame()

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

def extract_filling(brand_name, gmdn_pt_name=None):
    if gmdn_pt_name and "saline" in gmdn_pt_name.lower():   # IDEAL IMPLANT
        return "saline filling"

    brand_name = brand_name.lower()
    if "memorygel" in brand_name:
        return "MENTOR MemoryGel filling"                   # MENTOR
    elif "memoryshape" in brand_name:
        return "MENTOR MemoryShape filling"
    elif "inspira softtouch" in brand_name:
        return "NATRELLE INSPIRA SoftTouch filling"         # NATRELLE
    elif "inspira cohesive" in brand_name:
        return "NATRELLE INSPIRA Cohesive filling"
    elif "inspira" in brand_name:
        return "NATRELLE INSPIRA filling"
    elif "410 highly cohesive" in brand_name:
        return "NATRELLE 410 Highly Cohesive filling"
    elif "natrelle silicone-filled" in brand_name:
        return "NATRELLE Silicone Gel filling"
    elif "sientra" in brand_name:
        return "SIENTRA Silicone Gel filling"               # SIENTRA
    else:
        raise ValueError(f"UNKNOWN BRAND NAME: {brand_name}")

def extract_profile_mentor(device_desc):
    profiles = ["moderate classic profile", "moderate profile",
                "moderate plus profile", "moderate plus profile xtra",
                "high profile", "high profile xtra", "ultra high profile"]
    
def extract_profile_allergan(style):
    profiles_dict = {
        "10" : "moderate profile",      # smooth round solutions - found in product catalog
        "15" : "midrange profile",
        "20" : "high profile"    ,
        "40" : "moderate profile",      # additional smooth round solutions
        "45" : "full profile"    ,
        "110": "moderate profile",      # BIOCELL textured round
        "115": "midrange profile",
        "120": "high profile"    ,
        "FL" : "low profile"     ,      # STYLE 410 HIGHLY COHESIVE MATRIX
        "ML" : "low profile"     ,      # CATALOG NOTES
        "LL" : "low profile"     ,      # FL = Full Height Low Projection, ML - Moderate Height Low
        "FM" : "moderate profile",      # LL = Low Height Low Projection,
        "MM" : "moderate profile",      # FM = Full Height Moderate Projection, MM = Moderate Height Moderate Projection
        "LM" : "moderate profile",      # LM = Low Height Moderate Projection,
        "FF" : "full profile"    ,      # FF = Full Height Full Projection, MF = Moderate Height Moderate Projection
        "MF" : "full profile"    ,      # LF = Low Height Full Projection
        "LF" : "full profile"    ,
    }
    
    if style in profiles_dict:
        return "NATRELLE" + profiles_dict[style]
    

