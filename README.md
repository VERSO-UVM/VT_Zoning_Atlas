[![license-MIT](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://github.com/VERSO-UVM/VT_Zoning_Atlas/blob/main/LICENSE) [![DOI](https://zenodo.org/badge/688699704.svg)](https://zenodo.org/doi/10.5281/zenodo.11508693)


# Vermont Zoning Atlas

The [Vermont Zoning Atlas](https://www.zoningatlas.org/vermont) is a web-based geospatial interface that visualizes zoning code distributions across all of Vermont. Zoning rules can present barriers to effective city planning, impairing our ability to achieve important policy objectives like community desegregation, climate change resiliency, transportation access, homelessness relief, and affordable housing development. The Vermont Zoning Atlas seeks to democratize researchers', policymakers', advocates', and everyday citizens' understanding of zoning regulations and enable apples-to-apples cross-jurisdiction comparisons through a methodology developed by our partner, the [National Zoning Atlas](https://www.zoningatlas.org/).
Without this tool, one would have to read thousands of pages of dense legal code to answer simple questions - this is why we believe our tool will democratize zoning policy and make it possible for advocates and researchers to identify barriers to things like affordable housing development, climate resiliency, and community desegregation more quickly.

In the News: 
[Housing Forward Virginia - Zoning Atlases Across the Map: Vermont, August 24, 2023](https://housingforwardva.org/news/fwd-g25-vermont-zoning-atlas/)

UVM

## Progress
At this point all areas have been mapped and we are working towards publishing the whole dataset.

## Data
Data uploaded to the National Zoning Atlas can be found in the "ZoningAtlas" folder as follows:
* .csv files with zoning regulations broken by district
  - (https://github.com/VERSO-UVM/VT_Zoning_Atlas/tree/main/ZoningAtlas/districts)
* Jurisdiction footprints (TIGER files)
  - (https://github.com/VERSO-UVM/VT_Zoning_Atlas/tree/main/ZoningAtlas/jxtn_footprints)
* Completed zoning district geoJSONs
  - (https://github.com/VERSO-UVM/VT_Zoning_Atlas/tree/main/ZoningAtlas/districts_gis) 

## Join the Effort
This effort is a collection of teams which includes volunteers, interns, and students getting course credit. Please reach out in Discussions to see if you can join the effort!

## Partnerships
The project is in collaboration with the following
* [Vermont state Agency of Commerce and Community Development (ACCD)](https://accd.vermont.gov/)
* [Department of Housing and Community Development (DHCD)](https://accd.vermont.gov/housing)
* [Vermont Association of Planning and Development Agencies (VAPDA)](https://www.vapda.org/)
* [Vermont Center for Geographic Information (VCGI)](https://vcgi.vermont.gov/)
* [Vermont Housing Finance Agency (VHFA)](https://www.vhfa.org/)
* [Champlain Valley Office of Economic Opportunity (CVOEO)](https://www.cvoeo.org/)
* [Fair Housing Project](https://www.cvoeo.org/get-help/fair-housing-and-discrimination)
* [Vermont Affordable Housing Coalition (VAHC)](https://www.vtaffordablehousing.org/)
* [UVM’s Open Source Program Office (VERSO)](https://verso.w3.uvm.edu/)
* [University of Vermont Gund Institute](https://www.uvm.edu/gund)
* [Middlebury College Geography Department](https://www.middlebury.edu/college/academics/geography)

## Roles and Tasks

The Zoning Code Analyst team:
* Reviews and compares zoning by-laws and land use rules for each jurisdiction (town, village, city, or gore) in Vermont
* Catalogues the attributes of each district’s rules according to the National Zoning Atlas methodology:
* Dimensional standards (e.g., minimum lot size, maximum building height)
* Process requirements (e.g., whether a public hearing is required for residential development approval, whether mobile home parks are permitted)
* Jurisdictional information (e.g., number of pages in zoning code, type of municipality)
* District information (e.g., allowed land use, base or overlay, full and abbreviated name)
* Enters data into the National Zoning Atlas Editor workspace for review and joining with GIS file
* Reports up any complications, problems, or questions to the Project Director for technical assistance

The GIS Specialist team:
* Accesses open-source zoning district geoJSONs
* Performs topology checks to find and correct invalid geometries and boundary issues (e.g., overlapping base districts, polygons drawn outside jurisdictional boundaries, gaps/slivers between base districts)
* Merges non-continuous district polygons into multi-polygons
* Georeferences an existing geoJSON against the official zoning map .pdf to ensure accuracy of district boundaries
* Manually creates zoning district files where none exist
* Updates attribute tables with required columns according to the National Zoning Atlas methodology
* Reports up any complications, problems, or questions to the Project Director for technical assistance
* Uploads completed files to the National Zoning Atlas Editor workspace for review and publication

## Set Up
* [Git](https://www.git-scm.com/downloads) 
* [GitHub Desktop](https://desktop.github.com/)
* [Visual Studio Code](https://code.visualstudio.com/)
* [ArcGIS](https://uvm.maps.arcgis.com/sharing/rest/oauth2/authorize)
