import sys
import os

import re
import requests
import datetime
import argparse
from collections import defaultdict
from datetime import date
import json

import tokenizeUrl

def makeDestinationFolders(session_dates):
    session_dates = session_dates.replace("/","_")
    try:
        os.mkdir(f"tex/{session_dates}", 0o666)
    except:
        print(f"tex/{session_dates} Folder already exists...Continuing...")
    try:
        os.mkdir(f"tex/{session_dates}/meta", 0o666)
    except:
        print(f"tex/{session_dates}/meta Folder already exists...Continuing...")

def tokenizeSessions(lawp_urls, session_date, session_dates = None):
    lawSummaries = []
    for url in lawp_urls:
        temp = tokenizeUrl.tokenizeUrl(url.strip(), session_date, session_dates)
        if temp != None:
            lawSummaries.append(temp)
    return lawSummaries

def getProjectUrls(session_hrefs):
    lawp_urls = []
    for i, href in enumerate(session_hrefs):
        req = requests.get(href)
        htmlTokenList = req.text.replace("><",">\n<").split("\n")
        for line in htmlTokenList:
            match = re.search(r'.*href=\"(\/scpro[0-9A-Za-z.?\/]+)\">.*', line)
            if match:
                lawp_urls.append(match.group(1))

    for i,el in enumerate(lawp_urls):
        lawp_urls[i] = "http://alerjln1.alerj.rj.gov.br" + lawp_urls[i] + "\n"

    return lawp_urls

def getSessionsDictUrls():
    htmlSource = requests.get("http://alerjln1.alerj.rj.gov.br/ordemdia.nsf/OrdemInt?OpenForm")
    htmlTokenList = htmlSource.text.replace("><",">\n<").split("\n")
    sessionPattern = f".*href=\"(/ordemdia.*)\">([0-9][0-9]\/[0-9][0-9]\/[0-9][0-9][0-9][0-9])<.*"
    sessionDict = defaultdict(list)

    for line in htmlTokenList:
        match = re.search(sessionPattern, line)
        urlPrefix = "http://alerjln1.alerj.rj.gov.br"
        if match:
            date = match.group(2)
            date = date[3:5] + "/" + date[:2] + "/" + date[6:] # MDY to DMY
            sessionDict[date].append(urlPrefix + match.group(1))
    return sessionDict

def main(externalPipeline=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--latex", action="store_true",
                                help="Compile tex files into pdf")
    parser.add_argument("-d", "--date", type=str,
            help="format:dd/MM/YY or dd/MM/YY-dd/MM/YY")

    if externalPipeline:
        args = parser.parse_args(externalPipeline.split(" "))
    else:
        args = parser.parse_args()




    DATE_FORMAT = "([0-9][0-9])\/([0-9][0-9]\/[0-9][0-9][0-9][0-9])"
    sessionDict = getSessionsDictUrls()

    if args.date:
        match_dates = re.search(f"{DATE_FORMAT}-{DATE_FORMAT}", args.date)
        match_date = re.search(f"{DATE_FORMAT}", args.date)
        if not match_dates and not match_date:
            print("Input pattern not matched")
            exit(parser.print_help())
        session_dates = args.date
    else:
        match_dates = None
        match_date = None
        first_date = sorted(sessionDict)[0]
        last_date = sorted(sessionDict)[-1]
        session_dates = f"{first_date}-{last_date}"

    makeDestinationFolders(session_dates)

    lawSummaries = []

    if match_dates:
        dayBegin = int(match_dates.group(1))
        dayEnd = int(match_dates.group(3))
        MonthYear = match_dates.group(2)
        print(f"Day range: {dayBegin}-{dayEnd} of:{MonthYear}")
        
        print("\n### Scraping multiple day sessions ###")
        for day in range(dayBegin, dayEnd+1):
            
            session_date = f"{day}/{MonthYear}"
            print("Data da sessão:", session_date)
            lawp_urls = getProjectUrls(sessionDict[session_date])
            for url in lawp_urls:
                projectDict = tokenizeUrl.tokenizeUrl(url.strip(),session_date,session_dates)
                if projectDict != None:
                    lawSummaries.append(projectDict)
        print("############\n")

    elif match_date:
        session_date = session_dates
        print("\n### Scraping single day sessions ###")
        print("Data da sessão:", session_date)
        lawp_urls = getProjectUrls(sessionDict[session_date])
        for url in lawp_urls:
            projectDict = tokenizeUrl.tokenizeUrl(url.strip(),session_date,session_dates)
            if projectDict != None:
                lawSummaries.append(projectDict)
        print("############\n")
         
    else:
        print("\n### Scraping recent week sessions ###")
        for session_date in sessionDict.keys():
            print("Data da sessão:", session_date)
            lawp_urls = getProjectUrls(sessionDict[session_date])
            lawSummaries = tokenizeSessions(lawp_urls, session_date, session_dates)

        print("############\n")

    session_dates = session_dates.replace("/","_")


    with open(f"tex/{session_dates}/meta/dump.json", "w") as fp:
        json.dump(lawSummaries, fp)

    if args.latex:
        saveCwd = os.getcwd()
        os.chdir(f"tex/{session_dates}")
        pdfs = ""
        latexCompile = "pdflatex -interaction=nonstopmode -output-directory=meta"
        for filename in os.listdir("."):
            if ".tex" in filename:
                pdfs += filename[:-4] + ".pdf "
                print(f"Compiling LaTeX...{filename}")
                os.system(f"{latexCompile} \"{filename}\" > /dev/null 2>&1")

        os.chdir("meta")
        fullPdf = f"full_{session_dates}.pdf"
        print("Uniting Pdfs...")

        os.system(f"pdfunite {pdfs} {fullPdf}")
        os.system(f"mv {fullPdf} ../")
        os.chdir(saveCwd)
    return session_dates


if __name__ == "__main__":
    main()






