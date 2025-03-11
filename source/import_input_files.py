import os
import warnings
import pandas as pd
from tkinter.filedialog import askopenfilename

path_consolidated = os.getenv('path_consolidated')
path_global_accounting = os.getenv('path_global_accounting')

consolidated_pre_rev = pd.read_csv(path_consolidated)
global_acc = pd.read_csv(path_global_accounting)
global_acc['Future State - Account'] = global_acc['Future State - Account'].astype(str).str.strip()


def import_invalid_mappings_no_prior(): 

    print("Import the Invalid Mappings export as an .xlsx")
    invalid_mappings_sheet = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    invalid_mappings = pd.read_excel(invalid_mappings_sheet, engine='openpyxl')

    print("Import the FCCS maps export as a .csv") 
    fccs_maps_sheet = askopenfilename(filetypes=[("Excel files", "*.csv")])
    fccs_maps = pd.read_csv(fccs_maps_sheet, usecols=[0, 1])
    fccs_maps = fccs_maps[fccs_maps.iloc[:, 0].str.startswith('LE')]
    fccs_maps.columns = ['String', 'Target'] + list(fccs_maps.columns[2:])

    print("Import the Profiles export as a .csv") 
    profiles_sheet = askopenfilename(filetypes=[("Excel files", "*.csv")])
    profiles = pd.read_csv(profiles_sheet, usecols=[0,1,2,3,4,5,6,7,28])
    profiles = profiles.rename(columns={'Profile Segment 1': 'LE', 'Profile Segment 2': 'OG', 
                                        'Profile Segment 3': 'AC', 'Profile Segment 4': 'DT', 
                                        'Profile Segment 5': 'ST', 'Profile Segment 6': 'PJ', 
                                        'Profile Segment 7': 'F1', 'Profile Segment 8': 'F2'})
    profiles['DT'] = profiles['DT'].replace('0', '0000')
    profiles['OG'] = profiles['OG'].replace('0', '0000')
    profiles['PJ'] = profiles['PJ'].replace({'0': '0000', '12': '0012'})
    profiles['Joined Target'] = profiles[['LE', 'OG', 'AC', 'DT', 'ST', 'PJ', 'F1', 'F2']].astype(str).agg('-'.join, axis=1)
    
    print("Import the Role Assignment report as a .csv")
    role_assignment_sheet = askopenfilename(filetypes=[("Excel files", ".csv")])
    role_assignment = pd.read_csv(role_assignment_sheet)

    return invalid_mappings, global_acc, consolidated_pre_rev, fccs_maps, profiles, role_assignment
