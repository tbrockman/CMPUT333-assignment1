file = open("table.txt",'r')
ext = []
colcount = 0
inPre = False
offset = 0
for line in file:
    line = line.strip("\n")
    if line == "<tr>":
        colcount = 0
        offset = 0
        
    elif "<td>" in line:
        if colcount == 2:
            line = line.replace("<td>","",1)
            line = line.replace("</td>","",1)
            offset = int(line)
            
        colcount += 1
        
    elif ("<pre>" in line) and (colcount == 5):
        line = line.replace("<pre>","",1)
        inPre = True
        
        ext.append('n'*offset + line)
    
    elif inPre:
        if "</pre>" in line:
            inPre = False
            ext[-1] = ext[-1].replace(" ","")
        else:
            ext[-1] = ext[-1] + line


print (ext)
        