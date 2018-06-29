import xlrd
import pandas
import csv


def main():
    # read device
        # get primaryDI, brandName, versionModelNumber, companyName,
        # deviceDescription
    cols = [0, 5, 6, 8, 10]
    device_sh_df = pandas.read_excel("deviceInfo.xlsx",
                                     "device",
                                     usecols=cols)
    # read deviceSizes
    # get sizeText
    col = 4
    deviceSizes_sh_df = pandas.read_excel("deviceInfo.xlsx",
                                          "deviceSizes",
                                          usecols=col)
    # read productCodes
    # get productCode
    col = 1
    productCodes_sh_df = pandas.read_excel("deviceInfo.xlsx",
                                           "productCodes",
                                           usecols=col)
    # read identifiers
    # get deviceID
    col = 1
    indentifiers_sh_df = pandas.read_excel("deviceInfo.xlsx",
                                           "identifiers",
                                           usecols=col)
    # read gmdnTerms
    # get gmdnPTName, gmdnPTDefinition?
    cols = [1, 2]
    gmdnTerms_sh_df = pandas.read_excel("deviceInfo.xlsx",
                                        "gmdnTerms",
                                        usecols=cols)

    # print(type(device_sh_df[['PrimaryDI']]))
    # print(type(deviceSizes_sh_df[['sizeText']]))
    # print(type(productCodes_sh_df[['productCodes']]))
    # print(type(deviceSizes_sh_df[['sizeText']]))

    joined_df = (device_sh_df[["PrimaryDI",
                              "brandName",
                              "versionModelNumber",
                              "companyName",
                              "deviceDescription"]]
                              .join(deviceSizes_sh_df[['sizeText']])
                              .join(productCodes_sh_df[['productCodes']])
                              .join(indentifiers_sh_df[['identifiers']])
                              .join(gmdnTerms_sh_df[['gmdnPTName', 'gmdnPTDefinition']]))

    joined_df.to_csv("rel_cols.csv",
                     sep=",")


if __name__ == '__main__':
    main()
