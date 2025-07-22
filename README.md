# RSAP-Analysis
The core analysis conducted for the RSAP is the exposure of Minimum Categories and Assets GIS data to coastal flood hazards representing future flooding conditions based on scenarios described in the California Sea Level Rise Guidance (2024). This regional exposure analysis is used to inform subregional Vulnerability Assessments. Other analysis scripts helped process the data to common jurisdictional extents or conducted specialty analysis for displaying data in the RSAP Atlas. GIS data was initially processed to a common
projection (NAD83 UTM Zone 10N), intersected with jurisdiction types, and clipped to the RSAP Analysis Area (i.e. OLU based primary, contributing watershed, and bayland units). Individual GIS datasets were additionally processed to combine relevant data inputs (i.e. DTSC and WB contaminated sites), clean data (i.e. remove elevated transportation segments), and create a legible symbology.The goal of this git is to provide access to example analysis scripts for major RSAP data analysis, however not all steps were processed through a scripting framework. 

For a full description of data analysis methods, please see the RSAP Data Sources and Analytical Methodology Report. URLXXXXX.....

Data analysis scripts are example python and R scripts used for relevant RSAP analysis steps. They reference specific datasets, though don't reference all RSAP topic data. Example scripts include:
1. Coastal Flood Hazard Data Creation (Python script used to combine coastal flood hazard data sources for use in the RSAP) - Available in separate github repo....
2. RSAP Exposure + Jurisdiction Intersection (Python script to run basic RSAP exposure and jurisdictional intersections, where applicable they also calculate the SRP field)
3. RSAP Jurisdiction Intersection (Python script used for data that just need jurisdiction intersections, i.e. no exposure analysis)
4. RSAP Jurisdiction Cleanup (Python script used to address city misspellings and ensure consistent formatting of jurisdiction fields)
5. Multijurisdiction Analysis (Python script used to identify jurisdictions that overlap with common Operational Landscape Units and concatenate those values in a new field for city/CDP, county, and OLU boundary data, to facilitate multijurisdictional planning)
6. CBO Directory Jurisdiction Analysis (Python script used to add city, county, and OLU names to CBO Directory dataset)
7. RSAP Planning Progress Excel to Web (Python script used to convert RSAP Planning Progress excel to spatial file for RSAP Atlas)
8. RSAP Housing and Jobs Parcel Analysis (R script to analysis housing and job spaces exposure to coastal flood hazards, using methodology developed by BCDC and MTC for the SLR Funding and Investment Strategy and adopted for use by the RSAP)
9. RSAP Housing and Jobs Summaries (Python scripts used to summarize housing and jobs analaysis for city, county, OLU, and transportation analysis zone units)

Data outputs are available via the RSAP Open Data Portal https://rsap-open-data-bcdc.hub.arcgis.com/.

Please contact GIS@bcdc.ca.gov if you have questions.
