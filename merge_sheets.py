import pandas as pd
from functools import reduce


def merge_sheets(file):
    sheets_dict = pd.read_excel(file, sheet_name=None)
    rel_cols = {}

    rel_cols["device"] = sheets_dict["device"][["PrimaryDI",
                                                "brandName",
                                                "versionModelNumber",
                                                "catalogNumber",
                                                "companyName",
                                                "deviceDescription"]]
    rel_cols["device_sizes"] = sheets_dict["deviceSizes"][["PrimaryDI", "sizeText"]]
    rel_cols["product_codes"] = sheets_dict["productCodes"][["PrimaryDI", "productCode"]]
    rel_cols["identifiers"] = sheets_dict["identifiers"][["PrimaryDI", "deviceId"]]
    rel_cols["gmdn_terms"] = sheets_dict["gmdnTerms"][["PrimaryDI", "gmdnPTName", "gmdnPTDefinition"]]

    dfs = []
    for _key, value in rel_cols.items():
        dfs.append(value)

    df_final = reduce(lambda left, right: pd.merge(left, right, on="PrimaryDI", how="outer"), dfs)
    return df_final


if __name__ == '__main__':
    df_final = merge_sheets("../2 Data/deviceInfo.xlsx")
    df_final.to_csv(open("../2 Data/rel_cols.csv", "w"), sep=",", float_format="%.2f")
