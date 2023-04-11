# Why this repository?

This repository has the updated versions of the libraries created by MPIV that use Tenable API's, Pytenable or Navi, to interact with Tenable products.

## mpiv_io_pyten

This library uses pytenable to interact with Tenable.io. We are not using the API for Tenable.io as we see that pytenable has access two almost all Tenable.io features and we do not want to reinvent the wheel. So far, our library organizes the methods that allows interaction with Tenable.io in four major classes: scans, assets, tags and vulnerabilities. It also has a python file called basic_functions, with some common fucntions that methods will need to work: eg, create new connections, convert pyhton objects to other formats, etc.

### Available functions/methods

#### Scans

&nbsp;&nbsp;**show_scans():** Shows all scans available in T.io and returns a csv file with a report. The same report is printed in screen. See [T.io Scans Report](mpiv_io_pyten/output_files/io_scans_report.csv)

&nbsp;&nbsp;**get_scans_id():** Returns a python list of numbers with the scan ids

#### Assets

&nbsp;&nbsp;**asset_report():** Generates a csv file with the list of assets found in Tenable.io.
See [T.io Assets Report](mpiv_io_pyten/output_files/io_assets_report.csv)

&nbsp;&nbsp;**update_asset_tag():** Assigns tags in bulk to assets listed in a .csv file. The csv file must have two columns UUID and TAG_ID. See an example file at [Assets and Tags](mpiv_io_pyten/input_files/update_list.csv)

&nbsp;&nbsp;**get_asset_list():** Returns a python list of dictionaries with the assets info

#### Tags

&nbsp;&nbsp;**tag_summary():** Prints in screen an generates a csv report with the list of tags avaialble in T.io
See [T.io Tags Report](mpiv_io_pyten/output_files/io_tag_summary.csv)

&nbsp;&nbsp;**get_tag_list():** Returns a list of dictionaries with the tags info

#### Vulnerabilities

&nbsp;&nbsp;**vuln_report():** Creates a vulnerabilities csv report. The report can be generated for all scans or for specific scan ids. See [T.io Vulns Report](mpiv_io_pyten/output_files/io_spec_vulns.csv)


Additional to these main mehtods the base_function file, has the following functions created

**connect_io():** Creates a connection to Tenable.io using API keys. The keys are read from a file called IO_API_Keys.txt See the following file
[Assets and Tags](mpiv_io_pyten/input_files/IO_API_Keys.txt)



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



### Old libraries

**mpiv_pyten_sc_lib**: interact with Tenable.sc through pytenable. Is not receiveing frequent updates and is kept for historic records or if it is required again in the future. To see details of the functions, please check the library .py file.

**mpiv_io_lib:**: interact with Tenable.io through the official API. Is not receiveing frequent updates and is kept for historic records or if it is required again in the future. To see details of the functions, please check the library .py file.
