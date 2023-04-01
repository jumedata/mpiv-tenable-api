# Why this repository?

This repository will have updated versions of the functions and libraries created for MPIV using Tenable API's or Navi. Old pytenable based functions are kept for historic records.

## MPIV Libraries

Currently we are actively using two libraries:

### mpiv_sc_lib 
This library uses the oficial Tenable.sc API to retrieve information and create new elements in Tenable.sc. Uses the tenable API as we found some limitations to access dashboards and reports using pytenable

#### Available Functions

**get_sc():**  
Performs a HTTP GET request to Tenable.sc using the API

**post_sc():**  
Performs a HTTP POST request to Tenable.sc using the API

**patch_sc():**  
Performs a HTTP PATCH request to Tenable.sc using the API

**show_asset_list():**  
Crates a csv report with the details of all assets list. If in detail mode, the information is also printed in screen. The functions always returns a list containig the id's of the assets lists

See [Example Asset List Report](outputfiles/asset_list_report.csv)

**create_csv_all():**  
Allows the creation of a static ip list in Tenable.sc using a .csv file only containing ips

**scan_details_report():**
Generates a .csv report showing: credentials, policies and assets lists configured in each scan 

See [Example Scans Details Report](outputfiles/scans_details_report.csv)

**edit_csv_al():**
Edits an existing static asset list with the IP listed in a .csv file

**al_used_in():**
Returns a dictionary cotaining the names of the queries and scans where an asset list is used.

**user_created_items():**
Returns a csv file and dictionary detailing all the items created in Tenable.sc by an user

See [Example User Created items Report](outputfiles/user_items.csv)

### mpiv_pyten_io_lib
This library uses pytenable to interact with Tenable.io. We are not using the API for Tenable.io as we see that pytenable has access two almost all Tenable.io features, so we do not need to reinvent the wheel.

#### Available functions

**connect_io():**  
Creates a connection to Tenable.io using API keys. The keys are read from a file called IO_API_Keys.txt 

**show_scans():**  
Shows all scans available in T.io and returns a csv file with a report. The same report is printed in screen.

See [T.io Scans Report](outputfiles/tio_scans_report.csv)

**vuln_report():** 
Creates a vulnerabilities csv report. The filename is a string that should be provided always without specifying the format.

**get_asset_list():**
Connects to Tenable.io, returns a list of dictionaries with the assets info

**get_tag_list():**
Connects to Tenable.io, returns a list of dictionaries with the tags info

**asset_report():**
Generates a csv file with the list of assets found in Tenable.io.
See [T.io Assets Report](outputfiles/io_assets_report.csv)

**tag_summary():**
Prints in screen an generates a csv report with the list of tags avaialble in T.io


### Other libraries

**mpiv_pyten_sc_lib**: interact with Tenable.sc through pytenable. Is not receiveing frequent updates and is kept for historic records or if it is required again in the future. To see details of the functions, please check the library .py file.

**mpiv_io_lib:**: interact with Tenable.io through the official API. Is not receiveing frequent updates and is kept for historic records or if it is required again in the future. To see details of the functions, please check the library .py file.
