# Pytenable

This repo will have updated versions of the functions and libraries created for MPIV using Pytenable, Navi or Tenable API's

## MPIV Library

Generally speaking, all API projects will be created as functions that can be used according to specific needs. By using functions, we simplify the usage for customers and we can have more control on the user input, also easing code reuse for different projects.

Current status of MPIV library is at: https://github.com/jumedata/pytenable - Only accesible to Oporto, Garcia and me:

### Current available functions

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

