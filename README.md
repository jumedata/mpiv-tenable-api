# Pytenable

This repo will have updated versions of the functions and libraries created for MPIV using Pytenable, Navi or Tenable API's

## MPIV Libraries

Generally speaking, all API projects will be created as independent libraries, each one with unique functions that can be used according to specific needs. By using functions, we simplify the usage for customers and we can have more control on the user input, also easing code reuse for different projects.

Current status of MPIV libraries is detailed at: https://github.com/jumedata/pytenable - Only accesible to Oporto, Garcia and Meneses. 

Currently there are two libraries:

### mpiv_io_lib.py  
This library allows the usage of pytenable and Tenable.io

#### Available functions

**connect_IO():**  
This Function connects to Tenable.io using API Keys    

**show_scans():**  
Shows all scans available in T.io    

![image](images/showscansoutput.jpg "show_scans output")  


**vul_report(\*args, filename):**  
Generates a .csv report  

See [Example Vulns Report](outputfiles/Example_vulns_repo.csv)


**get_asset_list:()**  
Returns a list of dictionaries with the assets info  

**get_tag_list():**  
Returns a list of dictionaries with tags info  

**asset_report(filename):**  
Generates a csv file with the list of assets found in Tenable.io  

See [Example Assets Report](outputfiles/Example_asset_repo.csv)
 
**tag_summary()**  
Prints a summary of the tags in T.io 


### mpiv_sc_lib.py  
This library allows the usage of Tenable.sc directly from Tenable.sc API

#### Available Functions
**connect_sc():**  
Connect to Tenable.sc through a GET request on the API

**show_asset_list():**  
Print in screen all the assets lists that an user can edit

### mpiv_pyten_sc_lib.py  
This library allows the usage of Tenable.sc and pytenable

#### Available Functions

**connect_pass_sc():**  
Connect to Tenable.sc using an user and password type connection  

**connect_apik_sc():**  
Connect to Tenable.sc using API keys

**create_csv_all():**  
Allows the creation of a ststic ip lits in Tenable.sc using a .csv file only containing ips  

**show_asset_list():**  
Print in screen all the assets lists that an user can edit

**scan_details_report():**
Generates a .csv report showing: credentials, policies and assets lists configured in each scan 

See [Example Scans Details Report](outputfiles/scans_details_report.csv)

**edit_csv_al():**
Edits an existing static asset list with the IP listed in a .csv file

**al_used_in():**
Returns a dictionary cotaining the names of the queries and scans where an asset list is used.

**user_created_items():**
Returns a dictionary detailing the scans and asset lists created by each user
