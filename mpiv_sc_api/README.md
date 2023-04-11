# Available functions/methods by class

## Scans

**details_report():** Generates a .csv report showing: credentials, policies and assets lists configured in each scan 

See [Example Scans Details Report](mpiv_sc_api/output_files/sc_scans_details_repo.csv)

## Assets Lists

**used_in():** Returns a dictionary cotaining the names of the queries and scans where an asset list is used.

**show_list():** Creates a csv report with the details of all assets list. If in detail mode, the information is also printed in screen. The functions always returns a list containig the id's of the assets lists

See [Example Asset List Report](mpiv_sc_api/output_files/sc_asset_list_report.csv)

**create_from_csv():**  Allows the creation of a static ip list in Tenable.sc using a .csv file only containing a list of IP's

**edit_from_csv():** Edits an existing static asset list with the IP's listed in a .csv file. The method has the option to add the additional IP's keeping the current configuration or simply delete de old configuration

## Users

**created_items():** Returns a csv file detailing all the items created by an user in Tenable.sc

See [Example User Created items Report](mpiv_sc_api/output_files/sc_user_created_items.csv)