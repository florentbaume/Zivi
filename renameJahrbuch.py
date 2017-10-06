import re, sys, os, glob, shutil

#
# Input folders and paths stuff
#

# Complete paths to avoid mistakes when working from different folders.
currentPath=os.path.split(os.path.realpath(__file__))[0]
folderPath=os.path.split("path\\to\\folder")[0] # To change to use for other files
outPath=os.path.join(currentPath,"Jahrbuch")
print folderPath

for filename in glob.glob(os.path.join(folderPath,"*.pdf")):
    inFullPath = os.path.join(folderPath,filename)
    if os.path.isfile(inFullPath):
        fname = os.path.split(filename)[1]
        regEx= re.compile("^(\d{4})([A-Z])_(\d\d)-(\d\d)\.pdf$") # Define the export format <station><data type>_<yearIn>-<yearEnd>.pdf, eg 2351Q_05-05.pdf
        match=re.match(regEx,fname)
        if match:
            reGroups = match.groups()
            if reGroups[-1]==reGroups[-2]: 
                outFname = "%s%s_%s.pdf" % reGroups[0:-1] # Define the format used on the web <station><data type>_<yearIn>.pdf, eg 2351Q_05-05.pdf
                outPathFile=os.path.join(currentPath,"Jahrbuch",outFname)
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                shutil.copyfile(inFullPath,outPathFile)

