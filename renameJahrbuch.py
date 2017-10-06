import re, sys, os, glob, shutil

verbose=False 
#
# Input folders and paths stuff
#

# Complete paths to avoid mistakes when working from different folders.
currentPath=os.path.split(os.path.realpath(__file__))[0]
folderPath=os.path.split("N:\\benutzer\\prakti\\print\\")[0]
outPath=os.path.join(currentPath,"Jahrbuch")
print folderPath

for filename in glob.glob(os.path.join(folderPath,"*.pdf")):
    inFullPath = os.path.join(folderPath,filename)
    if os.path.isfile(inFullPath):
        fname = os.path.split(filename)[1]
        regEx= re.compile("^(\d{4})([A-Z])_(\d\d)-(\d\d)\.pdf$")
        match=re.match(regEx,fname)
        if match:
            reGroups = match.groups()
            if reGroups[-1]==reGroups[-2]: 
                outFname = "%s%s_%s.pdf" % reGroups[0:-1]
                outPathFile=os.path.join(currentPath,"Jahrbuch",outFname)
                if not os.path.exists(outPath):
                    os.makedirs(outPath)
                shutil.copyfile(inFullPath,outPathFile)

