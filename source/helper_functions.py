def acc_group_assessment(tab, global_acc, tab_name):
    print(f"Accessing {tab_name}'s accounting group values")
    if not tab.empty:
        tab = tab.copy()
        tab['Acc Group?'] = tab['AC'].isin(global_acc['Future State - Account'])
    else:
        print(f"{tab_name} is empty, skipping processing.")
    return tab

# Cleaning and data manipulation functions for FCCS mappings file
def prep_fccs_maps(fccs_maps):

    print("Cleaning FCCS mappings file")
    fccs_maps['LE'] = fccs_maps['String'].apply(lambda x: x.split('-')[0].strip())
    fccs_maps['LE'] = fccs_maps['LE'].str.replace('LE_', '')
    fccs_maps['OG'] = fccs_maps['String'].apply(lambda x: x.split('-')[1].strip())
    fccs_maps['OG'] = fccs_maps['OG'].str.replace('OG_', '')
    fccs_maps['AC'] = fccs_maps['String'].apply(lambda x: x.split('-')[2].strip())
    fccs_maps['AC'] = fccs_maps['AC'].str.replace('AC_', '')

    fccs_maps['LE-OG-AC'] = fccs_maps['LE'].astype(str) + '-' + fccs_maps['OG'].astype(str) + '-' + fccs_maps['AC'].astype(str)
    for col in ['LE', 'OG', 'AC']:
        fccs_maps[col] = fccs_maps[col].str.strip().str.upper()

    return fccs_maps

