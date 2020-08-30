import re
import requests
import sys

dumpFilePath = "txt"

def parseNestedParagraphs(text):
    indexes_start = []
    indexes_end = []
    lFile = text.split("\n")
    for linenumber,line in enumerate(lFile):
        match = re.findall("^[I][^a-zA-Z]+.*",line)
        if len(match)>0:
            indexes_start.append(linenumber)

    matching = False
    for linenumber,line in enumerate(lFile):
        match = re.findall("^[IXV]+[^a-zA-Z]+.*",line)
        if (len(match) > 0):
            matching = True
        elif (matching == True):
            indexes_end.append(linenumber)
            matching = False
        else:
            continue
    for i,(start,end) in enumerate(zip(indexes_start,indexes_end)):
        lFile.insert(start+i*2,"\\begin{enumerate}[label=\\Roman*]")
        lFile.insert(end+1+i*2,"\\end{enumerate}")

    for i,line in enumerate(lFile):
        lFile[i] = re.sub("^[IXV]+[^a-zA-Z]+", "\\item - ", line)

    return "\n".join(lFile)


def replaceTokens(lawProject):
    textFile = ""
    with open("tex/template_lei.tex","r") as temp:
        textFile = temp.read()
        textFile = re.sub(r'\*PROJETO',lawProject['projeto'],textFile)
        textFile = re.sub(r'\*URL',lawProject['url'],textFile)
        textFile = re.sub(r'\*EMENTA',lawProject['ementa'],textFile)
        textFile = re.sub(r'\*AUTOR',lawProject['autor'],textFile)
        textFile = re.sub(r'\*JUSTIFICATIVA',lawProject['justificativa'],textFile)
        try:
            textFile = re.sub(r'\*LOCALDATA',lawProject['localdata'],textFile)
        except:
            textFile = re.sub(r'\*LOCALDATA',"",textFile)
        textFile = re.sub(r'\*NOME',lawProject['nome'],textFile)
        textFile = re.sub(r'\*CORPO',lawProject['corpo'],textFile)
        textFile = re.sub(r'\*REFERÊNCIAS',lawProject['referencias'],textFile)
    return textFile


def cutBetween(start,end,lFileIn):
    copy = False
    sCutOut = ""
    for line in lFileIn:
        if re.search(start,line.strip()):
            copy = True
            continue
        elif re.search(end,line.strip()):
            copy = False
            continue
        elif copy:
            if line != "\n":
                sCutOut += line + "\n"
    return sCutOut

def tokenizeUrl(url, session_date, session_dates = None):
    r = requests.get(url)
    pureTxt = re.sub(r'<[^>]*>', '', r.text)
    pureTxt = re.sub(r'8220;',"``",pureTxt)
    pureTxt = re.sub(r'8221;',"\"",pureTxt)
    pureTxt = re.sub(r'8211;',"-",pureTxt)
    pureTxt = re.sub(r'&quot;',"\"",pureTxt)
    pureTxt = re.sub(r'\$',"\\$",pureTxt)


    project = ""
    ementa = ""
    autor = ""
    justificativa = ""
    corpo = ""
    referencias = ""
    lPureTxt = pureTxt.split("\n")


    for line in lPureTxt:
        p = re.compile("PROJETO[^0-9]+([\d]+\/[\d]+).*$")
        m = p.match(line)
        if m:
            project = m.group(1)

    if project == "":
        print("----------------")
        print("Law Project not found")
        return 
    else:
        print("----------------")
        print("Parsing Law: ", project)
        print("Url: ", url)


    lPureTxt = re.sub(r"RESOLVE:","RESOLVE:\n",'\n'.join(lPureTxt))
    lPureTxt = lPureTxt.split("\n")

    ementa = cutBetween("EMENTA:.*", "Autor\(es\):.*", lPureTxt)
    
    for line in lPureTxt:
        p = re.compile("Autor\(es\):(.*)")
        m = p.match(line)
        if m:
            autor = m.group(1)
    
    for line in lPureTxt:
        localdata =  re.search('(Plenário Barbosa Lima Sobrinho.*)',line.strip())
        if localdata:
            break
    
    if localdata: 
        endbody = localdata.group(1)
    else:
        endbody = "JUSTIFICATIVA"

    corpo = cutBetween(".*RESOLVE:.*", f".*{endbody}.*", lPureTxt)
    justificativa = cutBetween(r"JUSTIFICATIVA.*","(REFERÊNCIAS.*|Legislação Citada.*)",lPureTxt)

    nome = re.search(r".*Deputad[\w]+(.*)",autor)
    if nome:
        nome = nome.group(1)
    else:
        nome = autor

    justificativa = re.sub(r'%',"\%", justificativa)

    corpoList = corpo.split("\n")
    for i,line in enumerate(corpoList):
        corpoList[i] = re.sub(r'^ ?Art[a-z]*[^A-Z]+',"\\item - ", line)
    corpo = '\n'.join(corpoList)
    corpo = re.sub(r'8211;',"-", corpo)
    corpo = re.sub(r'&#-',"-", corpo)

    if localdata != None:
        localdata = localdata[0]
    else:
        localdata = ""

    lawProject = {'projeto': project,
                   'ementa': ementa,
                   'corpo': corpo,
                   'justificativa': justificativa,
                   'localdata': localdata,
                   'nome':nome,
                   'autor': autor,
                   'referencias': referencias,
                   'url': url}

    lawProjectSummary = {'projeto': project,
                         'ementa': ementa,
                         'localdata' : localdata,
                         'session_date': session_date}

    textFile = replaceTokens(lawProject)
    textFile = parseNestedParagraphs(textFile)
    project = project.replace("/","_")

    print("Project:",project)
    texFileName = "lei_" + project + ".tex"

    session_date = session_date.replace("/","_")
    if session_dates:
        session_dates = session_dates.replace("/","_")
        texFilePath=f"tex/{session_dates}/"
    else:
        texFilePath=f"tex/{session_date}/"

    with open(texFilePath+texFileName,"w") as lei:
        lei.write(textFile)
    return lawProjectSummary


if __name__ == "__main__":
    url = sys.argv[1]
    parseUrl(url)
