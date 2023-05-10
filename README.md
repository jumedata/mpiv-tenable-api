# Welcome to MPIV's Tenable Libraries

We created this project to help Tenable.io and Tenable.sc customers to take advantage of the additional features and interactions available through Tenable's API's. Our goal is to provide out of the box solutions for those customers who need additional features, but have few or no resources to deep dive into Tenable developer's platform.

`This is an independent project not officially supported by Tenable`

For more details about us, please see [MPIV Site](https://mpivpartners.com/)

## mpiv_io_pyten

This library uses [pytenable](https://github.com/tenable/pyTenable) to interact with Tenable.io. We use pytenable as it has access to almost all Tenable.io features. Our library groups the methods that allows interaction with Tenable.io in classes; so far, four classes are created:_scans, assets, tags, and vulnerabilities_ 

To see the library's documentation please see: [io_pyten README](mpiv_io_pyten/README.md)

## mpiv_sc_api

This library uses the [Tenable.sc API](https://docs.tenable.com/tenablesc/api/index.htm) to interact with Tenable.sc. We use the official API rather than pytenable, as we noticed some Tenable.sc features like reports and dashboards are not yet available in pytenable. Currently our library has three main classes:_scans, users, and assets lists_ 

To see the library's documentation please see: [sc_api README](mpiv_sc_api/README.md)