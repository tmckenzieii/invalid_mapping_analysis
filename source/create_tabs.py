# Create data frame for 1A
import pandas as pd
import numpy as np

def create_tab_1a(invalid_mappings): 

    print("Creating tab 1A")
    tab_1a = invalid_mappings[~invalid_mappings['Account ID'].str.contains('ALL-ALL-ALL-ALL-ALL')].copy()
    
    if not tab_1a.empty:
        tab_1a.loc[:, 'LE'] = tab_1a['Account ID'].str.split('-', expand=True)[0]
        tab_1a.loc[:, 'LE Clean'] = tab_1a['LE'].str.split('_').str[0]
        tab_1a.loc[:, 'OG'] = tab_1a['Account ID'].str.split('-', expand=True)[1]
        tab_1a.loc[:, 'AC'] = tab_1a['Account ID'].str.split('-', expand=True)[2]
    else:
        # If it is empty, you might want to do something or just pass
        pass

    return tab_1a

def create_tab_1b(invalid_mappings):
    print("Creating tab 1B")
    # Filter the DataFrame based on 'Account ID' containing 'ALL-ALL-ALL-ALL-ALL'
    tab_1b = invalid_mappings[invalid_mappings['Account ID'].str.contains('ALL-ALL-ALL-ALL-ALL')].copy()
    
    # Check if the DataFrame is empty using .empty
    if not tab_1b.empty:
        # If not empty, split 'Account ID' and create new columns for LE, OG, and AC
        tab_1b.loc[:, 'LE'] = tab_1b['Account ID'].str.split('-', expand=True)[0]
        tab_1b.loc[:, 'OG'] = tab_1b['Account ID'].str.split('-', expand=True)[1]
        tab_1b.loc[:, 'AC'] = tab_1b['Account ID'].str.split('-', expand=True)[2]
    else:
        # If it is empty, you might want to do something or just pass
        pass

    return tab_1b

def create_ag_tab(tab, global_acc, consolidated_pre_rev, profiles, tab_name):
    print(f"Creating {tab_name} AG tab")

    # Check if 'tab' is empty at the beginning to avoid processing an empty DataFrame
    if tab.empty:
        print(f"{tab_name} is empty. Returning an empty DataFrame.")
        # You might want to return an empty version of 'tab' with specific columns if necessary
        return pd.DataFrame(columns=['AC', 'Acc Groups', 'Acc Desc', 'Grouping', 'Proposed Target from Mapping'])
    
    tab_1x_ag = tab[tab['AC'].isin(global_acc['Future State - Account'])].copy()

    tab_1x_ag['Acc Groups'] = tab_1x_ag['AC'].map(global_acc.set_index('Future State - Account')['Wesco 1A Account Grouping Exceptions'])

    tab_1x_ag['Acc Desc'] = tab_1x_ag['Acc Groups'].map(consolidated_pre_rev.set_index('Account Group')['Account Description'])

    tab_1x_ag['Grouping'] = tab_1x_ag['Acc Groups'].map(consolidated_pre_rev.set_index('Account Group')['Grouping'])

    conditions = [
        (tab_1x_ag['Grouping'] == 'LE'),
        (tab_1x_ag['Grouping'] == 'LE & OG'),
        (tab_1x_ag['Grouping'] == 'Globally')
    ]

    choices = [
        tab_1x_ag['LE'].astype(str) + '-XXXX-' + tab_1x_ag['Acc Desc'].astype(str) + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        tab_1x_ag['LE'].astype(str) + '-' + tab_1x_ag['OG'].astype(str) + '-' + tab_1x_ag['Acc Desc'].astype(str) + '-XXXX-XXXXX-XXXX-XXXX-XXXX',
        'XXXX-XXXX-' + tab_1x_ag['Acc Desc'].astype(str) + '-XXXX-XXXXX-XXXX-XXXX-XXXX'
    ]
    
    tab_1x_ag['Proposed Target from Mapping'] = np.select(conditions, choices, default='')

    # Check proposed target against profiles -> if not in profiles, replace with 'No Target'
    mask = ~(tab_1x_ag['Proposed Target from Mapping'].values[:, None] == profiles['Joined Target'].values).any(axis=1)
    tab_1x_ag.loc[mask, 'Proposed Target from Mapping'] = 'No Target'

    return tab_1x_ag

# Create data frame for 1A Non AG
def create_tab_1a_non_ag(tab_1a, fccs_maps):
    print("Creating tab 1A Non AG")
    tab_1a_non_ag = tab_1a[tab_1a['Acc Group?'] == False].copy()
    tab_1a_non_ag.drop('Acc Group?', axis=1, inplace=True)

    for col in ['LE', 'OG', 'AC']:
        tab_1a_non_ag[col] = tab_1a_non_ag[col].str.strip().str.upper()

    tab_1a_non_ag['LE-OG-AC'] = tab_1a_non_ag['LE'] + '-' + tab_1a_non_ag['OG'] + '-' + tab_1a_non_ag['AC']

    tab_1a_non_ag['Proposed Target from Mapping'] = tab_1a_non_ag['LE-OG-AC'].apply(lambda x: fccs_maps.loc[fccs_maps['LE-OG-AC'] == x, 'Target'].values[0] if x in fccs_maps['LE-OG-AC'].values else "No Target")
    tab_1a_non_ag = tab_1a_non_ag.drop(columns=['LE', 'LE Clean', 'OG', 'AC']) 
    
    try:
        tab_1a_errored_rows = tab_1a_non_ag[~tab_1a_non_ag['Proposed Target from Mapping'].str.endswith('XXXX')
                                        & (tab_1a_non_ag['Proposed Target from Mapping'] != 'No Target')]
        tab_1a_errored_rows = tab_1a_errored_rows.drop(columns=['LE-OG-AC', 'Proposed Target from Mapping'])
        
        tab_1a_non_ag = tab_1a_non_ag.drop(tab_1a_errored_rows)
        
        print(tab_1a_non_ag)
        
        if not tab_1a_errored_rows.empty:
            tab_1a_non_ag = tab_1a_non_ag[~tab_1a_non_ag['Account ID'].isin(tab_1a_errored_rows['Account ID'])]
    
    except KeyError as e:
        print(f"Error: {e} column not found in data frame")
    
    return tab_1a_non_ag, tab_1a_errored_rows

# Create column to determine existing targets in tab AG tab from profiles
def tab_1x_ag_target(tab_1x_ag, profiles):

    print("Finding tab targets")
    for index, row in tab_1x_ag.iterrows():
        proposed_target = row['Proposed Target from Mapping']
        matching_row = profiles[profiles['Joined Target'] == proposed_target]
        if not matching_row.empty:
            existing_target = matching_row.iloc[0]['Joined Target']
            tab_1x_ag.at[index, 'Existing Target from Profiles'] = existing_target
        else:
            tab_1x_ag.at[index, 'Existing Target from Profiles'] = "No Target"

    return tab_1x_ag

# Create data frame for 1A Need Details
def create_tab_1a_need_details(tab_1a_non_ag, tab_1a_errored_rows): # add tab_1a_errored_rows variable for cases where Proposed Target != end in XXXX

    print("Creating tab 1A Need Details")
    tab_1a_need_details = tab_1a_non_ag[tab_1a_non_ag['Proposed Target from Mapping'] == 'No Target']
    tab_1a_need_details = tab_1a_need_details.drop(columns=['LE-OG-AC', 'Proposed Target from Mapping']) # Check later
    
    tab_1a_need_details = pd.concat([tab_1a_need_details, tab_1a_errored_rows], ignore_index=True)
    tab_1a_need_details.reset_index(drop=True, inplace=True)

    return tab_1a_need_details

def create_tab_1b_need_details(tab_1b):
    print("Creating tab 1B Need Details")
    
    # Check if 'tab_1b' is empty at the beginning
    if tab_1b.empty:
        print("tab 1B is empty. Returning an empty DataFrame with the original structure.")
        # Assuming you want to return a DataFrame with the same structure minus the dropped columns
        # If the columns to be dropped are known ahead of time, remove them from this list
        return pd.DataFrame(columns=[col for col in tab_1b.columns if col not in ['LE', 'OG', 'AC', 'Acc Group?']])
    
    tab_1b_need_details = tab_1b[tab_1b['Acc Group?'] == False]
    tab_1b_need_details = tab_1b_need_details.drop(columns=['LE', 'OG', 'AC', 'Acc Group?'])

    return tab_1b_need_details

# Create accounting groups sheet
def create_accounting_groups_tab(tab_1a_ag, tab_1b_ag, profiles, role_assignment):
    
    columns_to_drop = ['LE', 'LE Clean', 'OG', 'AC', 'Acc Group?', 'Acc Desc', 'Acc Groups', 'Grouping']
    
    accounting_groups_1a = tab_1a_ag[tab_1a_ag['Proposed Target from Mapping'] != 'No Target']
    accounting_groups_1a = accounting_groups_1a.drop(columns=columns_to_drop, errors='ignore')
    accounting_groups_1a.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    accounting_groups_1a['User ID'] = accounting_groups_1a['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(zip(role_assignment['User Login'], role_assignment['Email']))
    accounting_groups_1a['User Email'] = accounting_groups_1a['User ID'].map(role_assignment_mapping_dict)

    accounting_groups_1b = tab_1b_ag[tab_1b_ag['Proposed Target from Mapping'] != 'No Target']
    accounting_groups_1b = accounting_groups_1b.drop(columns=columns_to_drop, errors='ignore')
    accounting_groups_1b.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    accounting_groups_1b['User ID'] = accounting_groups_1b['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(zip(role_assignment['User Login'], role_assignment['Email']))
    accounting_groups_1b['User Email'] = accounting_groups_1b['User ID'].map(role_assignment_mapping_dict)
    
    return accounting_groups_1a, accounting_groups_1b

# Create new profiles - need workflow details sheet
def create_new_profile_wf_details(tab_1a_ag, tab_1b_ag):
    
    columns_to_drop = ['LE', 'LE Clean', 'OG', 'AC', 'Acc Group?', 'Acc Desc', 'Acc Groups', 
                        'Grouping', 'Proposed Target from Mapping']
    columns_to_add  = ['Preparer','Preparer Email','Reviewer 1','Reviewer 1 Email',
                        'Reviewer 2','Reviewer 2 Email','Preparer User ID','Reviewer 1 User ID',
                        'Reviewer 2 User ID']
    
    new_profile_need_wf_details_1a = tab_1a_ag[tab_1a_ag['Proposed Target from Mapping'] == 'No Target']
    
    new_profile_need_wf_details_1b = tab_1b_ag[tab_1b_ag['Proposed Target from Mapping'] == 'No Target']
    
    new_profile_need_wf_details = pd.concat([new_profile_need_wf_details_1a, new_profile_need_wf_details_1b], axis=0)
    new_profile_need_wf_details = new_profile_need_wf_details.drop(columns=columns_to_drop, errors='ignore')
    new_profile_need_wf_details.reset_index(drop=True, inplace=True)
    
    for col_name in columns_to_add:
        new_profile_need_wf_details[col_name] = pd.NA
    
    return new_profile_need_wf_details

# Create user confirmations sheet
def create_user_confirmations(tab_1a_non_ag, profiles, role_assignment):
    
    columns_to_drop = ['LE-OG-AC']
    
    user_confirmations = tab_1a_non_ag[tab_1a_non_ag['Proposed Target from Mapping'].str.endswith('XXXX')]
    user_confirmations = user_confirmations.drop(columns=columns_to_drop, errors='ignore')
    user_confirmations.reset_index(drop=True, inplace=True)
    
    profiles_mapping_dict = dict(zip(profiles['Joined Target'], profiles['Preparer']))
    user_confirmations['User ID'] = user_confirmations['Proposed Target from Mapping'].map(profiles_mapping_dict)
    
    role_assignment_mapping_dict = dict(zip(role_assignment['User Login'], role_assignment['Email']))
    user_confirmations['User Email'] = user_confirmations['User ID'].map(role_assignment_mapping_dict)
    
    return user_confirmations

# Create need details sheet
def create_need_details(tab_1a_need_details, tab_1b_need_details):
    
    headers_to_add = ['Group/Individual','Existing group (Yes/No/NA)','Existing Group Name','New Group Name','Override Frequency','Frequency','Risk rating','Preparer User ID', 'Reviewer 1 User ID','Reviewer 2 User ID']
    
    need_details = pd.concat([tab_1a_need_details, tab_1b_need_details], axis=0, ignore_index=True)
    
    need_details_na = need_details[need_details['Account ID'].str.startswith(('1', '2'))]
    need_details_cala = need_details[need_details['Account ID'].str.startswith('3')]
    need_details_apac = need_details[need_details['Account ID'].str.startswith('4')]
    need_details_emea = need_details[need_details['Account ID'].str.startswith('5')]
    
    def add_headers(df):
        new_columns = {header: pd.NA for header in headers_to_add}
        return df.assign(**new_columns)
    
    need_details_na = add_headers(need_details_na)
    need_details_cala = add_headers(need_details_cala)
    need_details_apac = add_headers(need_details_apac)
    need_details_emea = add_headers(need_details_emea)
    
    return need_details, need_details_na, need_details_cala, need_details_apac, need_details_emea 