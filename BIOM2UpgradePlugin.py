import sys

class BIOM2UpgradePlugin:
    def input(self, myfile):
       self.infile = open(myfile, 'r')

    def run(self):
        pass

    def output(self, myfile):
       outfile = open(myfile, 'w')

       biom1 = self.infile.read()  # Entire line

       biom2 = ""  # Form string, write at end

       biom2 += biom1[:biom1.find("rows")+6]
       rowlist = biom1[biom1.find("rows")+6:biom1.find(",\"columns\":")]
       rowlist = rowlist.replace("\"metadata\":", "\"metadata\":{\"taxonomy\":")
       rowlist = rowlist.replace("]", "]}")
       rowlist = rowlist[:len(rowlist)-1]

       i = 1
       while (i < len(rowlist)):
           if (rowlist[i] == '['): # Scan until the next ]
              #print("GOT ONE")
              entry = rowlist[i:rowlist.find(']', i)+1]
              #print("ENTRY: "+entry)
              if (entry.count(',') > 6):
                  numextra = entry.count(',')-6
                  pos = rowlist.find(']', i)-1
                  commacount = 0
                  while (commacount < numextra):
                      if (rowlist[pos] == ','):
                          commacount += 1
                      pos -= 1
                  rowlist = rowlist.replace(rowlist[pos+1:rowlist.find(']',i)], '')
              i = rowlist.find(']', i)+1
              #print("AFTER:"+rowlist)
              #input()
           else:
              i += 1
    
       #biom2 += "\"rows\":"
       biom2 += rowlist
       biom2 += ','

       collist = biom1[biom1.find("columns")+9]
       collist = biom1[biom1.find("columns")+9:biom1.find(",\"data\":")]

       i = 2
       while (i < len(collist)):
           metadata_idx = collist.find("\"metadata\"", i)
           if (collist[metadata_idx+11:metadata_idx+15] != 'null'):
              metadata_entry = collist[metadata_idx+11:collist.find("]", metadata_idx)+1]
              #print("REPLACING: "+metadata_entry+" WITH null")
              collist = collist.replace(metadata_entry, 'null')
              #print(collist[metadata_idx:])
           i = collist.find("null}", metadata_idx)+6
           #print("NEXT UP: "+collist[i:])

       #print(collist)

       biom2 += "\"columns\":"
       biom2 += collist
       biom2 += ','

       biom2 += biom1[biom1.find("\"data\""):]
       #print(biom2)
       outfile.write(biom2)
