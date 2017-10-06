#import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv, os, sys, codecs


#
# Input folders and paths stuff
#

# Changes behaviour if arguments are passed in the terminal , e.g. $ python PQstylesheet.py arg1 arg2 ...

inFolderDefault="input_pq"
outFolderDefault="output_pq"

# 2 arguments: defines in and out folder
if len(sys.argv)==3:
    inFolder=sys.argv[1]
    outFolder=sys.argv[2]
# 1 argument: defines out folder, in folder defined by outFolderDefault value
elif len(sys.argv)==2:
    inFolder=inFolderDefault
    outFolder=sys.argv[1]
# No arguments: Uses default in/outFolderDefault values
else:
    inFolder=inFolderDefault
    outFolder=outFolderDefault

# Complete paths to avoid mistakes when working from different folders.
filePath=os.path.realpath(__file__)
folderPath=os.path.dirname(filePath)
inFolderPath=os.path.join(folderPath,inFolder)
outFolderPath=os.path.join(folderPath,outFolder)

# Create out folder if does not exist.
if not os.path.exists(outFolderPath):
    os.makedirs(outFolderPath)

#
# Inserts the Processing instruction (spreadsheet tag) into the xmls found in input folder,
# and dump it in output folder.
#


folderLen=len(os.listdir(inFolderPath))+1
print folderLen, "file found. Inserting PI stylesheet..."
i=1

# Loop over the input folder, adds the PI, and write the resulting XML in the output folder
for xmlName in os.listdir(inFolderPath):
    #Print progress. May or may not be commented in the future.
    if i%20==0: print i,"/",folderLen
    i=i+1
    # If XML file, add the stylesheet PI
    if xmlName.endswith(".xml"):
    
        # Parses the XML file and creates a DOM. Then add the PI just before root.
        dom=minidom.parse(os.path.join(inFolderPath,xmlName))
        pi=dom.createProcessingInstruction("xml-stylesheet", "type='text/xsl' href='pq.xsl'")
        root = dom.firstChild
        dom.insertBefore(pi,root)
        
        # Removes everything after first underscore or space, and adds the extension back.
        # e.g. 2001_01 good.xml -> 2001.xml
        xmlNameOut=xmlName.split("_",1)[0].split(" ",1)[0]+".xml"
        # Using codecs, else problem with encoding. 
        # NB: overwrites if exists already !
        with codecs.open(os.path.join(outFolderPath,xmlNameOut),"w","utf-8") as file:
            dom.writexml(file)
