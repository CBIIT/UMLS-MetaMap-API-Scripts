UMLS-MetaMap-API-Scripts
For everyday commits we use CIT/BRICS/Kevin’s repository: https://github.com/kevon217/data-dictionary-cui-mapping – which is going to have contributors from BRICS, CBIIT, NEI, etc. 
Once a month, before submitting the monthly report, we copy all relevant code from CIT/BRICS/Kevin’s repository (TBD)  to this repository 

Python Pipeline files: 
#
0. CDE to UMLS Preprocessing.zip – contains the script which does pre-processing and formatting of COVID CDE attributes to be fed to  steep 2 - API to MetaMap script.
1. UMLS-CUI_DE-PV_pipeline_ipynb_Version-1.6_TEMP-FIX_2023-01-25.zip – API to MetaMap set of scripts, created and supported by BRICS.
2. UMLS to NCI Final.zip – the script which hits API to UMLS and returns NCIt concept for each given UMLS concept for each CDE.
3. NCIt concept lineage retrieval form EVS file.xlsx - the file which contains: 1) NCIt concept lineage retrieved from NCIt EVS https://evs.nci.nih.gov/ftp1/ - refer to "NCIt Concept Code and Lineage" tab; 2) the formula which allows the concept lineage retrieval for the given NCIt CUI - refer to "Example" tab.
4. NCI Concept Lineage to Tree.zip – the script which created NCIt concept lineage with a CDE as a leaf

#
#Data:
#
COVID CDEs to SemNet New Attributes Mappings.xlsx – the huge working file with mappings of Project 5 COVID CDEs to UMLS/NCIt. In contains historic data with our very first mappings using various mapping approaches.

COVID CDE Domains with NCI with concept lineage.xlsx – the file with NCIt concept lineage documented for those  COVID CDEs, which were mapped to UMLS/NCIt concepts.
NCI Concept Tree 19 Domains.zip – a ZIP archive with NCIt concept lineage presented as a tree (with a CDE as a leaf) for those CDEs, which were mapped to UMLS/NCIt concepts (refer to #2).

MetaMap_Settings_StopWords_CheatSheet.xlsx – the latest file with stop words, MetaMap settings, cheat sheet of UMLS concepts, and other useful information.

NCI Thesaurus Download December 2022 Synonyms 1.zip – the limited list of synonyms based on Semantic types present in COVID CDE mappings, extracted from NCIt EVS file. To be used in mapping. Work in progress.

