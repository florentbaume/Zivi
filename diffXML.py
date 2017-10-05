import xml.etree.ElementTree as ET
import csv, re, sys, os

verbose=False 
#
# Input folders and paths stuff
#

# Changes behaviour if arguments are passed in the terminal , e.g. $ python diffXML.py arg1 arg2 

# Complete paths to avoid mistakes when working from different folders.
filePath=os.path.realpath(__file__)
folderPath=os.path.dirname(filePath)

# Path to XML files
xmlDamastDefault="Damast.xml"
xmlHydrowebDefault="Hydroweb.xml"

# 2 arguments: defines in and out folder
if len(sys.argv)==3:
    xmlDamast=os.path.join(sys.argv[1])
    xmlHydroweb=os.path.join(sys.argv[2])
# No arguments: Uses default in/outFolderDefault values
else:
    xmlDamast=os.path.join(xmlDamastDefault)
    xmlHydroweb=os.path.join(xmlHydrowebDefault)

# Take care of None values when importing, converting them to empty strings.
def TranslateNone(var):
    if var is not None:
        return var
    else:
        return ""

# Looks for a comment starting with a date formatted DD.MM.YYYY and extract it 
# (from the range 01.01.1600 - 31.12.2099)
# NB: will match a date like 31.02.2000, use with caution ! 
# For the string "31.01.2000: lorem ipsum", returns a list ["lorem ipsum", "31.01.2000"]
def GetDateFromComment(commentStr):
    patternDate= re.compile("(^(0[1-9]|[1-2][0-9]|3[0-1])\.(0[1-9]|1[0-2])\.(1[6-9]\d{2}|20\d{2})):\s") # eg. 04.09.2017

    checkDate=re.search(patternDate, commentStr)
    if checkDate : return [commentStr[11:], checkDate.group(1)]
    else: return [commentStr,""]

# Get stations ID, names and comments, and possibly extract date from an XML file.
def GetStationData(xmlName):
    tree = ET.parse(xmlName)
    root = tree.getroot()
    return [
            [
                child.attrib["eNr"], 
                child.find("ort").text.encode("utf-8")
            ]+GetDateFromComment(TranslateNone(child.find("comment").text).encode("utf-8"))
        for child in root]

# Print a list in a csv
def PrintListTocsv(csvName,listToPrint, commentCSV=None, columnNames=None ,myDelimiter="\t"):
    with open(csvName,"w") as csvfile:
        writer=csv.writer(csvfile, delimiter=myDelimiter)
        if not commentCSV == None: csvfile.write(commentCSV)
        if not columnNames== None: writer.writerow(columnNames)
        writer.writerows(listToPrint)


dataDamast=GetStationData(xmlDamast)
dataHydroweb=GetStationData(xmlHydroweb)

idHydroweb=[sub[0] for sub in dataHydroweb]

##########################################

# Write a list of the comments in Damast
listCommentFname=os.path.join(folderPath,"listCommentDamast.csv")
PrintListTocsv(listCommentFname,dataDamast,columnNames=["eNr", "ort", "comment", "date"])
print("Extracting list of comments from Damast file...")

##########################################

# Transforms the ID list to a set, and use set properties to get the Damast stations not in Hydropweb
missingHydroweb= list(set([i[0] for i in dataDamast])-set([i[0] for i in dataHydroweb]))

# Gets subset of Damast list that are in Hydroweb
subDataDamast=[sub  for sub in dataDamast if sub[0] in idHydroweb]

# Gets symmetric difference of those two lists (union minus intersection):
symDiff=map(list,list(set(map(tuple,subDataDamast)).symmetric_difference(set(map(tuple,dataHydroweb)))))


# Adds the name of the list it comes from
for sub in symDiff:
    if sub in subDataDamast: sub.append("Damast")
    elif sub in dataHydroweb: sub.append("Hydroweb")
symDiff=sorted(symDiff)


if len(symDiff)==0:
    print "The comments are the same in both files."
else:
    print "Differences found:\t"
    if verbose:
        for sub in symDiff: print sub

    # Print the list in a csv
    diffFname=os.path.join(folderPath,"commentDifferences.csv")
    PrintListTocsv(
            diffFname,
            symDiff, 
            columnNames=["eNr", "ort", "comment", "date", "file origin"]
            )
    print "They have been written in '"+diffFname+"'."

##########################################

# Gets union of the list
union=sorted(map(list,list(set(map(tuple,subDataDamast)).union(set(map(tuple,dataHydroweb))))))
# Gets lists with comments
union=[sub for sub in union if sub[2]!=""]

if len(union)==0:
    print "There is nothing common in the two XMLs."
else:
    print "Found entries common to both files:\t"
    if verbose:
        for sub in union: print sub

    # Print the list in a csv
    unionFname=os.path.join(folderPath,"commentUnion.csv")
    PrintListTocsv(
            unionFname,
            union, 
            columnNames=["eNr", "ort", "comment", "date"]
            )
    print "They have been written in '"+diffFname+"'."

##########################################

if len(missingHydroweb)==0:
    print "NO stations are missing in Hydroweb."
else:
    print "Missing stations found."
    indexMissing=[i for i,x in enumerate(dataDamast) if x[0] in missingHydroweb]
    if verbose:
        for i in indexMissing: print dataDamast[i]

    # Print the list in a csv
    missingStationName=os.path.join(folderPath,"missingStations.csv")
    PrintListTocsv(
            missingStationName,
            [dataDamast[i] for i in indexMissing], 
            commentCSV="# Found "+str(len(missingHydroweb))+" stations not in Hydroweb\n",
            columnNames=["eNr", "ort", "comment", "date"]
            )
    print "There are ", len(missingHydroweb), "stations in Damast that are not in Hydroweb:"
    print "They have been written in '"+missingStationName+"'."

 
