# -*- coding: utf-8 -*-
import pandas as pd
import getopt
import sys
import json
import csv
if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "i:o:g:", ["input=", "output=", "geo="])
    input_file = None
    output_file = None
    geo_file = None
    for o, a in opts:
        if o == "-i":
            input_file = a
        if o == "-o":
            output_file = a
        if o == "-g":
            geo_file = a
    if input_file is None or output_file is None:
        print("missing argument")
        sys.exit(1)

    df = pd.read_json(input_file)
    df = df.rename(columns={"單位數目": "units", "地區": "district", "建築年份": "year_built", "層數": "storyes", "屋苑名稱": "estate", "大廈名稱": "name", "地庫層數": "basements"})
    df = df.rename(columns={"No. of Storeys": "storeys", "Year Built": "year_built", "No. of Units": "units", "Name of Building": "name", "Name of Estate": "estate", "No. of Basement": "basements", "District": "district"})
    geo_dict = {}
    df2 = pd.read_json(geo_file)
    df2 = df2.rename(columns = {"address": "address_1"})
    df3 = pd.merge(df, df2, on='address_1')
    print(df3.columns)
    df3 = df3.reindex(columns=['link_id', 'district', 'estate', 'name', 'year_built', 'basements', 
        'storyes', 'units','lat', 'lng', 'address_1', 'address_2', 'address_3', 'address_4', 'address_5', 
        'address_6', 'address_7', 'address_8', 'address_9', 'address_10', 'address_11', 'address_12', 'address_13', 
        'address_14', 'org_name_1', 'org_name_2', 'org_name_3', 'org_name_4','org_name_5', 'org_name_6', 
        'org_name_7', 'org_name_8', 'org_name_9', 'org_name_10','org_type_1', 'org_type_2', 'org_type_3', 'org_type_4', 
        'org_type_5', 'org_type_6', 'org_type_7', 'org_type_8', 'org_type_9', 'org_type_10'])
    df3.to_csv(output_file, quoting=csv.QUOTE_ALL, index=False)
