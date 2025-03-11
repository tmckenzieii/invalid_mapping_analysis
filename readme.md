### Invalid Mappings Analysis Documentation

This script processes invalid mappings and generates various reports to assist in data validation and analysis. Below is a detailed explanation of the script, its functions, and how to use it.

#### Table of Contents
1. Overview
2. Functions
    - import_invalid_mappings_no_prior
    - import_invalid_mappings_prior
    - create_tab_1a
    - create_tab_1b
    - acc_group_assessment
    - create_ag_tab
    - prep_fccs_maps
    - create_tab_1a_non_ag
    - create_tab_1a_need_details
    - create_tab_1b_need_details
    - save_invalid_mappings
    - create_accounting_groups_tab
    - create_new_profile_wf_details
    - create_user_confirmations
    - create_need_details
    - save_files_to_ship
3. Usage

### Overview
This script is designed to process invalid mappings and generate various reports for data validation and analysis. It reads data from multiple CSV and Excel files, processes the data, and saves the results into new Excel files.

### Functions

#### `import_invalid_mappings_no_prior`
Imports invalid mappings and FCCS files without considering prior mappings.

#### `import_invalid_mappings_prior`
Imports invalid mappings and FCCS files, removing prior mappings from the new file.

#### `create_tab_1a`
Creates a DataFrame for tab 1A by filtering and processing invalid mappings.

#### `create_tab_1b`
Creates a DataFrame for tab 1B by filtering and processing invalid mappings.

#### `acc_group_assessment`
Validates accounting group within tab 1A or 1B by checking against global accounting data.

#### `create_ag_tab`
Creates an AG (Account Group) DataFrame by mapping and processing data from global accounting and consolidated preparers and reviewers.

#### `prep_fccs_maps`
Cleans and processes the FCCS mappings file.

#### `create_tab_1a_non_ag`
Creates a DataFrame for tab 1A Non AG by filtering and processing invalid mappings that are not part of the accounting group.

#### `create_tab_1a_need_details`
Creates a DataFrame for tab 1A Need Details by filtering and processing invalid mappings that need further details.

#### `create_tab_1b_need_details`
Creates a DataFrame for tab 1B Need Details by filtering and processing invalid mappings that need further details.

#### `save_invalid_mappings`
Combines various DataFrames and saves them as a single Excel file.

#### `create_accounting_groups_tab`
Creates an accounting groups sheet by mapping and processing data from profiles and role assignments.

#### `create_new_profile_wf_details`
Creates a new profiles - need workflow details sheet by processing data from tab 1A and 1B AG.

#### `create_user_confirmations`
Creates a user confirmations sheet by processing data from tab 1A Non AG.

#### `create_need_details`
Creates a need details sheet by processing data from tab 1A and 1B Need Details.

#### `save_files_to_ship`
Saves various processed DataFrames into separate Excel files for shipping.

### Usage
1. **Pre-load Data Files**:
   Ensure the paths to the consolidated preparers and reviewers, global accounting group, and key accounts CSV files are correctly set.

2. **Run the Script**:
   Execute the script to process the data and generate the reports. The script will prompt you to select files and directories as needed.

3. **Review the Output**:
   The script will save the processed data into Excel files in the selected directory. Review these files for data validation and analysis.

### Example
```python
# Run the script
python main.py
```

This documentation provides an overview of the script's functionality and usage. If you have any questions or need further assistance, feel free to ask!
