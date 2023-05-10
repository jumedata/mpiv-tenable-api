# Available functions/methods by class

## Scans

**report():** creates a csv report with the id, status, name and owner of a scan See [T.io Scans Report](mpiv_io_pyten/output_files/io_scans_report.csv)

**get_ids():** Returns a python list with the ids of the scans available in Tenable.io

## Assets

**report():** Generates a csv file with the UUID, IP, DNS name and assigned tags off all assets found in Tenable.io.
See [T.io Assets Report](mpiv_io_pyten/output_files/io_assets_report.csv)

**update_tags_csv():** Assigns tags in bulk to the ip's listed in a .csv file. The csv file must have two columns UUID and TAG_ID. See an example file at [Assets and Tags](mpiv_io_pyten/input_files/update_list.csv)

**get_list():** Returns a python list of dictionaries, each dict has the details of an asset in Tenable.io

## Tags

**summary():** Prints in screen an generates a csv report with the list of tags avaialble in T.io
See [T.io Tags Report](mpiv_io_pyten/output_files/io_tag_summary.csv)

**get_list():** Returns a python list of dictionaries, each dict has the details of a tag in Tenable.io

## Vulnerabilities

**report():** Creates a vulnerabilities csv report. The report can be generated for all scans or for specific scan ids. See [T.io Vulns Report](mpiv_io_pyten/output_files/io_spec_vuln.csv)