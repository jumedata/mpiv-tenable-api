# Why this repository?

This repository will have updated versions of the functions and libraries created for MPIV using Tenable API's or Navi. Old pytenable based functions are kept for historic records.

# Why not using pytenable?

Pytenable is an interestig ongoing Tenable project, but sometimes, some of the functionalities requested by our customers cannot be covered if we use pytenable (eg. in Tenable.sc Reports and Dashboards), thus we prefer to use directly the Tenable API to fulfill those specific requests.

## MPIV Libraries

Currently we have developed four libraries:

**mpiv_sc_lib:** This library uses the oficial Tenable.sc API to retrieve information and create new elements in Tenable.sc. It is the one receiving all the attetion as has acces to all elements.

**mpiv_io_lib:** This library uses the oficial Tenable.io API to retrieve information and create new elements in Tenable.io. It is the one receiving all the attetion as has acces to all elements.

**mpiv_io_lib:**  This library uses pytenable to retrieve information and create new elements in Tenable.io. It is the only one created so far for Tenable.io, but will not receive any further updates as all the features will be redesigned to use the official API

**mpiv_pyten_sc_lib and mpiv_pyten_io_lib:** These were the first libraries created to interact with Tenable.sc and Tenable.io, but as some functionalities are not avaialble through pytenable, we decided to use thhe Tenable API's directly, thus since january 2023, these libraries are not receiving further updates.



### mpiv_io_lib.py  
This library allows the usage of Tenable.io directly from Tenable API

#### Available functions

**get_io():**  
Performs a HTTP GET request to Tenable.io using the API

**post_io():**  
Performs a HTTP POST request to Tenable.io using the API

**put_io():**  
Performs a HTTP PUT request to Tenable.io using the API   

**show_scans():**  
Shows all scans available in T.io and returns a csv file with a report. The same report is printed in screen 


### mpiv_sc_lib.py  
This library allows the usage of Tenable.sc directly from Tenable API

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


### mpiv_pyten_sc_lib.py  and mpiv_pyten_io_lib.py  
These libraries allows interacting with Tenable.sc and Tenable.io through pytenable. These were the first versions of MPIV libraries kept for historic records. To see details of the functions, please check the .py files of each library.



