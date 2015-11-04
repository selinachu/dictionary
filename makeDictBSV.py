#  Copyright 2015 Selina Chu

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#   
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  This script parses an ontology CSV file to generate a customized 
#  BSV dictionary file  
#
#  % python makeDictBSV.py 
#  
#  Currently, filenames and their semantic types are hard-coded.  Only one 
#  semantic type are assigned to all entries in a CSV file
#
#  CSV files of these ontologies can be downloaded here:
#  https://bioportal.bioontology.org/ontologies/BTO
#  http://bioportal.bioontology.org/ontologies/DOID
#  https://bioportal.bioontology.org/ontologies/GO

#  *Downloaded files need to be unzipped first before running this script
#
#  Semantic types
#  T024 Tissue
#  T028 Gene or Genome
#  T047 Disease or Syndrome
    
import sys
import csv

filename=['BTO.csv','DOID.csv','GO.csv'] # input csv filename
type=['T024','T047','T028'] # semantic type for a file

if len(filename)!=len(type):
  sys.exit('Each csv file needs a corresponding type')

outputfile='newDictionary.bsv'

ofile=open(outputfile,'w')
for i in range(len(filename)):
  print 'Processed ' + filename[i]
  with open(filename[i]) as csvfile:
    reader=csv.DictReader(csvfile)
    for row in reader:
      term=row['Preferred Label']
      if ':' in term:
        tempterm=term.split(':')
        if filename[i]=='BTO.csv':
          term=tempterm[1]
        elif filename[i]=='GO.csv':
          term=tempterm[0]
        else:
          print 'check for other cases'

      if filename[i]=='BTO.csv':
        tempterm=term.rsplit(' ',1)
        if len(tempterm)>1:
          temp=tempterm[1]
          if temp.startswith('cell'):
            term=tempterm[0] 
        
      tempid=row['http://www.geneontology.org/formats/oboInOwl#id']
      line=tempid.replace(':',"")+'|'+str(type[i])+'|'+term+'\n'
      ofile.write(line)

ofile.close()   
print 'Output is in '+ outputfile
