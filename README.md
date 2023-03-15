++Acknowledgements++

Special thanks to Denise Warzel (NIH/NCI) [E] and Smita Hastak (NIH/NCI) [Samvit Solutions] for guidance and feedback.

Special thanks to Kevin Armengol (https://github.com/kevon217/data-dictionary-cui-mapping) and Henry Ogoe from BRICS (https://brics.cit.nih.gov/)
and Sofia Syed [Samvit Solutions] for developing the scripts.

The MetaMap API code included is from Will J Roger's repository --> https://github.com/lhncbc/skr_web_python_api

Special thanks to Francois Lang (NIH/NLM/LHC) for providing the help and guidance on use of UMLS MetaMap (https://www.nlm.nih.gov/research/umls/implementation_resources/metamap.html)
and for answering our multiple questions.

Special thnaks to Wendy Ver Hoef, (NIH/NCI) [Samvit Solutions] for developing the technique of retrieving the NCIt concept lineage from NCI Thesaurus Download file (https://evs.nci.nih.gov/evs-download/thesaurus-downloads)

++ Requirements++
The scripts were tested under Anaconda Navigator (Anaconda 3) 

Tools:
Anaconda distribution, JupyterLab, Jupyter Notebooks

Modules used:
The modules needed to run the above three scripts include the following:

Pandas
Numpy
OS
treelib
Tree(from treelib)
pathlib
Path(from Path)
shutil
glob
tkinter
filedialog(from tkinter)
json
pprint
openpyxl
requests

To use the MetaMap python API requires to build it on your local the Python-based API 
created for the Indexing Initiative Scheduler facility (NLM) used to provide users with the ability to programmatically submit jobs to 
the Scheduler Batch and Interactive facilities. Available at https://github.com/lhncbc/skr_web_python_api

Anaconda environment: 
Download the environment files to use in Anaconda, to make your life easier.

The UMLS API key needed which can be found in the "My Profile" section of your account at UMLS (https://uts.nlm.nih.gov/uts/login).
