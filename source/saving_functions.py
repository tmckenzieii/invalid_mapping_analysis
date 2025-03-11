import os
from datetime import datetime
import pandas as pd
from tkinter import filedialog

# Function to combine data frames and save them as a single Excel file
def save_invalid_mappings(invalid_mappings, tab_1a, tab_1a_ag, tab_1a_non_ag, tab_1a_need_details, tab_1b, tab_1b_ag, tab_1b_need_details):

    print("Select a folder to save 'Invalid Mapping Analysis' file: ")
    # Create a Pandas Excel writer using XlsxWriter as the engine
    now = datetime.now().strftime("%y-%m-%d")
    folder_selected = filedialog.askdirectory()

    if folder_selected:
        writer = pd.ExcelWriter(os.path.join(folder_selected, f'Invalid Mapping Analysis {now}.xlsx'), engine='xlsxwriter')

        invalid_mappings.to_excel(writer, sheet_name='Invalid Mappings', index=False)
        tab_1a.to_excel(writer, sheet_name='1A', index=False)
        tab_1a_ag.to_excel(writer, sheet_name='1A AG', index=False)
        tab_1a_non_ag.to_excel(writer, sheet_name='1A Non AG', index=False)
        tab_1a_need_details.to_excel(writer, sheet_name='1A Need Details', index=False)
        tab_1b.to_excel(writer, sheet_name='1B', index=False)
        tab_1b_ag.to_excel(writer, sheet_name='1B AG', index=False)
        tab_1b_need_details.to_excel(writer, sheet_name='1B Need Details', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Invalid Mappings']

        writer._save()

        print(f"The file has been saved in {folder_selected}.")
    else:
        print("No folder selected.")

    return folder_selected

# 
def save_files_to_ship(accounting_groups_1a, accounting_groups_1b, new_profile_need_wf_details, need_details,
                                    need_details_na, need_details_cala, need_details_apac, need_details_emea, user_confirmations, folder_selected): # import folder_selected
    
    print("Saving files to ship to previously selected folder : ")
    
    now = datetime.now().strftime("%y-%m-%d")

    if folder_selected:
        writer_accounting_groups = pd.ExcelWriter(os.path.join(folder_selected, f'Accounting Groups {now}.xlsx'), engine='xlsxwriter')
        writer_new_profile_need_wf_details = pd.ExcelWriter(os.path.join(folder_selected, f'New Profile - Need Workflow Details {now}.xlsx'), engine='xlsxwriter')
        writer_user_confirmations = pd.ExcelWriter(os.path.join(folder_selected, f'User Confirmations {now}.xlsx'), engine='xlsxwriter')
        writer_need_details = pd.ExcelWriter(os.path.join(folder_selected, f'Need Details {now}.xlsx'), engine='xlsxwriter')
        
        accounting_groups_1a.to_excel(writer_accounting_groups, sheet_name='1A Confirmations', index=False)
        accounting_groups_1b.to_excel(writer_accounting_groups, sheet_name='1B Confirmations', index=False)
        
        new_profile_need_wf_details.to_excel(writer_new_profile_need_wf_details, sheet_name='New Profiles', index=False)
        
        need_details.to_excel(writer_need_details, sheet_name='Invalid Mappings', index=False)
        need_details_na.to_excel(writer_need_details, sheet_name='NA', index=False)
        need_details_cala.to_excel(writer_need_details, sheet_name='CALA', index=False)
        need_details_apac.to_excel(writer_need_details, sheet_name='APAC', index=False)
        need_details_emea.to_excel(writer_need_details, sheet_name='EMEA', index=False)
        
        user_confirmations.to_excel(writer_user_confirmations, sheet_name='1A Invalid Mappings', index=False) 
        
        writer_accounting_groups._save()
        writer_new_profile_need_wf_details._save()
        writer_user_confirmations._save()
        writer_need_details._save()
        
        accounting_groups_count = len(accounting_groups_1a) + len(accounting_groups_1b)
        new_profile_need_wf_details_count = len(new_profile_need_wf_details)
        need_details_count = len(need_details)
        user_confirmations_count = len(user_confirmations)
        total_count = sum([accounting_groups_count, new_profile_need_wf_details_count, need_details_count, user_confirmations_count])
        
        print(f"The files have been saved in {folder_selected}.")
    else:
        print("No folder selected.")
        
    return accounting_groups_count, new_profile_need_wf_details_count, need_details_count, user_confirmations_count, total_count