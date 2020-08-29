import os
from main import main
from alerj.models import PL

session_dates = main("-l")
metaFolder = "tex/{session_dates}/meta"
createObjectsFromJson(f"{metaFolder}/fdump.json")
for fileName in os.listdir(metaFolder):
    if ".pdf" in fileName:
        htmlFile = pdfFile[:-3] + "html"
        os.system(f"pdf2htmlEX {metaFolder}/{pdfFile}")

for fileName in os.listdir(metaFolder):
    if ".html" in fileName:
        os.rename(fileName,"../templates")




