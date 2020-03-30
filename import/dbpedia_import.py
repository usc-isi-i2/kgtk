import csv
def db_import(input_file,output_file):
    limit=None
    write=True
    rows=[]
    header=[]
    header.append('node1')
    header.append('label')
    header.append('node2')
    header.append('node1_prefix')
    header.append('node1_id')
    header.append('label_prefix')
    header.append('label_id')
    header.append('node2_prefix')
    header.append('node2_id')
    header.append('node2_type')
    data_dict={}
    if write:
        with open(output_file, 'w', newline='') as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
            wr.writerow(header)
    with open(input_file,mode='r') as file:
        reader=csv.reader(file,delimiter=' ',escapechar="\\")
        for cnt,line in enumerate(reader):
            keep=True
            if limit and cnt >= limit:
                break
            if cnt % 500000 == 0 and cnt > 0:
                print(cnt)
            if len(line)!=4:
                print(line)
                keep=False
            if keep:
                subject_isuri=False
                line=line[:3]
                n1_parts=line[0].rsplit('/', 1)
                line+=n1_parts
                label_parts=line[1].rsplit('/', 1)
                line+=label_parts
                subject=line[2]
                if '^^' in subject:
                    subject_parts=subject.split('^^')
                    value=subject_parts[0]
                    datatype=subject_parts[1]
                    if 'www.w3.org' in subject:
                        if 'boolean' in datatype:
                            final_value=value.capitalize()
                        elif 'date' in datatype:
                            final_value='^'+value+'T00:00:00Z/11'
                        elif 'YearMonth' in datatype:
                            final_value='^'+value+'-00T00:00:00Z/10'
                        elif 'Year' in datatype:
                            final_value='^'+value+'-00-00T00:00:00Z/9'
                        else:
                            final_value=value
                    else:
                        final_value='\"'+value+'\"'
                else:
                    datatype=''
                    if subject.startswith('<'):
                        subject_isuri=True
                    else:
                        if '@' in subject:
                            str_parts=subject.split('@')
                            final_value='\''+str_parts[0]+'\'@'+str_parts[1]
                        else:
                            final_value='\"'+str(subject)+'\"'
                if subject_isuri:
                    subject_parts=subject.rsplit('/',1)
                    line+=subject_parts
                else:
                    line+=[':',final_value]
                line.append(datatype)
                rows.append(line)
                for i in range(len(line)):
                    line[i]=line[i].replace('<','')
                    line[i]=line[i].replace('>','')
                    if (not subject_isuri) and i==2:
                        line[i]=final_value
            if write:
                if cnt % 50000 == 0 and cnt > 0:
                    with open(output_file, 'a', newline='') as myfile:
                        for row in rows:
                            wr = csv.writer(myfile, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
                            wr.writerow(row)
                        rows=[]
        if write:
            with open(output_file, 'a', newline='') as myfile:
                for row in rows:
                    wr = csv.writer(myfile, quoting=csv.QUOTE_NONE,delimiter="\t",escapechar="\n",quotechar='')
                    wr.writerow(row)
if __name__ == '__main__':
    input_file='dbpedia dumps/specific_mappingbased_properties_en.ttl'
    output_file='Dbpedia_specific_mapping_properties.tsv'
    db_import(output_file)