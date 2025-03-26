import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from source.import_input_files import import_invalid_mappings_no_prior
from source.create_tabs import create_tab_1a, create_tab_1b, create_ag_tab, create_tab_1a_non_ag, create_tab_1a_need_details
from source.create_tabs import create_tab_1b_need_details, create_accounting_groups_tab, create_need_details, create_new_profile_wf_details, create_user_confirmations
from source.helper_functions import acc_group_assessment, prep_fccs_maps
from source.saving_functions import save_invalid_mappings, save_files_to_ship

def load_environment_variables():
    load_dotenv()
    path_consolidated = os.getenv('path_consolidated')
    path_global_accounting = os.getenv('path_global_accounting')
    path_key_accounts = os.getenv('path_key_accounts')
    return path_consolidated, path_global_accounting, path_key_accounts

def load_data(path_consolidated, path_global_accounting, path_key_accounts):
    consolidated_pre_rev = pd.read_csv(path_consolidated)
    global_acc = pd.read_csv(path_global_accounting)
    global_acc['Future State - Account'] = global_acc['Future State - Account'].astype(str).str.strip()
    key_accounts = pd.read_csv(path_key_accounts)
    return consolidated_pre_rev, global_acc, key_accounts

def process_data():
    invalid_mappings, global_acc, consolidated_pre_rev, fccs_maps, profiles, role_assignment = import_invalid_mappings_no_prior()
    tab_1a = create_tab_1a(invalid_mappings)
    tab_1b = create_tab_1b(invalid_mappings)
    tab_1a = acc_group_assessment(tab_1a, global_acc, '1A')
    tab_1b = acc_group_assessment(tab_1b, global_acc, '1B')
    tab_1a_ag = create_ag_tab(tab_1a, global_acc, consolidated_pre_rev, profiles, '1A')
    tab_1b_ag = create_ag_tab(tab_1b, global_acc, consolidated_pre_rev, profiles, '1B')
    fccs_maps = prep_fccs_maps(fccs_maps)
    tab_1a_non_ag, tab_1a_errored_rows = create_tab_1a_non_ag(tab_1a, fccs_maps)
    tab_1a_need_details = create_tab_1a_need_details(tab_1a_non_ag, tab_1a_errored_rows)
    tab_1b_need_details = create_tab_1b_need_details(tab_1b)
    folder_selected = save_invalid_mappings(invalid_mappings, tab_1a, tab_1a_ag, tab_1a_non_ag, tab_1a_need_details, tab_1b, tab_1b_ag, tab_1b_need_details)
    accounting_groups_1a, accounting_groups_1b = create_accounting_groups_tab(tab_1a_ag, tab_1b_ag, profiles, role_assignment)
    new_profile_need_wf_details = create_new_profile_wf_details(tab_1a_ag, tab_1b_ag)
    user_confirmations = create_user_confirmations(tab_1a_non_ag, profiles, role_assignment)
    need_details = create_need_details(tab_1a_need_details, tab_1b_need_details) 
    accounting_groups_count, new_profile_need_wf_details_count, need_details_count, user_confirmations_count, total_count = save_files_to_ship(accounting_groups_1a, accounting_groups_1b, new_profile_need_wf_details, need_details, user_confirmations, folder_selected)

    return total_count, accounting_groups_count, new_profile_need_wf_details_count, user_confirmations_count, need_details_count

def main():
    path_consolidated, path_global_accounting, path_key_accounts = load_environment_variables()
    consolidated_pre_rev, global_acc, key_accounts = load_data(path_consolidated, path_global_accounting, path_key_accounts)
    total_count, accounting_groups_count, new_profile_need_wf_details_count, user_confirmations_count, need_details_count = process_data()
    print(f'Total invalid mappings is {total_count}')
    print(f'# of Accounting Group mappings - {accounting_groups_count}')
    print(f'# of New Profile - Need Details mappings - {new_profile_need_wf_details_count}')
    print(f'# of User Confirmation mappings - {user_confirmations_count}')
    print(f'# of Need Details mappings - {need_details_count}')

if __name__ == "__main__":
    main()