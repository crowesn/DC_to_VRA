DublinCore to VRA conversion script
-----------------------------------
Project to convert metadata from simplified Dublin Core to VRA  

**Task** - Transfer ~9000 records/images from DSpace repository to LUNAcommons.

**Content** - Cincinnati Subway and Street Improvements digital collection
>From: [Digital Resource Commons](http://drc.libraries.uc.edu/handle/2374.UC/702759)  
>To: [Luna Commons](http://digproj.libraries.uc.edu:8180/luna/servlet/univcincin~42~42)

csvpython.py contains class _easyCSV_ for parsing and building and modifying csv by column.  
RUN_DRCtoLUNA.py is an example script that code for processing and building records for this specific project.  
validate.py is a small script that validates records with linkdata file for loading to Luna  