import sys, os
sys.path.insert(0, "/home/geraldo/Dropbox/Código/Languages/Python/Django/AtelieVirtual") 

from manage import DEFAULT_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", DEFAULT_SETTINGS_MODULE)

import django
django.setup() 

from alerj.models import createObjectsFromJson
from scraperMain import main


def scrape():
    print(os.getcwd())
    session_dates = main("-l -d 01/09/2020")
    metaFolder = f"tex/{session_dates}/meta"
    createObjectsFromJson(f"{metaFolder}/dump.json")
    os.chdir(metaFolder)
    for fileName in os.listdir(os.getcwd()):
        if ".pdf" in fileName:
            htmlFile = fileName[:-3] + "html"
            os.system(f"pdf2htmlEX {fileName}")

    for fileName in os.listdir(os.getcwd()):
        if ".html" in fileName:
            os.rename(fileName,f"../../../templates/{fileName}")

scrape()



