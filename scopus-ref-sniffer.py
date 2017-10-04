#Looking for TNA references in text

import re
import codecs

from collections import Counter

count = 0
paper_count = 0
file_list = []
author_list = []
ref_list = []
fonds_list = []
series_list = []
author_doc_list = []

# Is the regex missing references in the format COPY 1/100/1 ? <- test this

#Diplomatic History
scopus_file = codecs.open("SCOPUS Diplomatic History 2008- July2017.csv", 'r', encoding='utf-8', errors='replace')
sniffer = re.compile(r"(KV|MUN|INF|PCOM|ED|RG|PIN|POST|LCO|OS|KB|ASSI|WARD|HCA|MH|MT|PL|DL|COPY|TS|LAB|MEPO|STAC|MAF|IR|T|WORK|HO|RAIL|PROB|SP|HW|GFM|DO|AB|AVIA|DSIR|DEFE|CAB|AIR|PREM|FO|FCO|EG|WO|ADM|CO|BT)([\s]\d+/\d+)") # rawstring in two groups
# J, E and C removed for false positives


#EHR and Past and Present
#scopus_file = codecs.open("SCOPUS EHR.csv", 'r', encoding='utf-8', errors='replace')
#scopus_file = codecs.open("SCOPUS Past and Present.csv", 'r', encoding='utf-8', errors='replace')
#scopus_file = codecs.open("SCOPUS HWJ.csv", 'r', encoding='utf-8', errors='replace')
#sniffer = re.compile(r"(KV|MUN|INF|PCOM|ED|RG|PIN|POST|LCO|OS|KB|ASSI|WARD|HCA|MH|MT|PL|DL|COPY|TS|LAB|MEPO|STAC|MAF|J|IR|E|C|T|WORK|HO|RAIL|PROB|SP|HW|GFM|DO|AB|AVIA|DSIR|DEFE|CAB|AIR|PREM|FO|FCO|EG|WO|ADM|CO|BT)([\s]\d+/\d+)") # rawstring in two groups
# Past and Present producing quite strange results

citations = scopus_file.readlines()


for line in citations:

    field = line.split(',')

    #Author information
    author = field[0]
    author = author.replace('\"', '')   
    
    for match in re.findall(sniffer, line):
        # print(match[0]+match[1] + " : " + author) # findall returns tuples, here glued together
        count += 1

        reference = match[0] + match[1]
        element = match[1].split('/')

        fonds_list.append(match[0])

        series = match[0] + element[0]
        series_list.append(series)

        if reference not in file_list:
            file_list.append(reference)

        if author not in author_list:
            author_list.append(author)

        if reference not in ref_list:
            ref_list.append(reference)

        glue = [reference,author] # creating single item list of author/reference pairing

        if glue not in author_doc_list: # repeated citations of a document BY THE SAME AUTHOR not included
            author_doc_list.append(glue) # creating list of those lists
         
    paper_count +=1

# Reporting
print ("\n" + str(count) + " citations located in " + str(paper_count) + " papers.")
print (str(len(author_list)) + " unique authors used TNA docs")
print (str(len(ref_list)) + " unique files detected")


# Counters
# Fonds count
print ("\n")
print(Counter(fonds_list))
print ("\n")

print(Counter(series_list))
print ("\n")


print(Counter(file_list))

# print(Counter(ref_list))

# Sort author/doc pairs by reference
author_doc_list.sort()
print(author_doc_list)


scopus_file.close()


      
