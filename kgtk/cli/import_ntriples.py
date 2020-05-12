"""
Import an ntriple file into KGTK file
"""


def parser():
    return {
        'help': 'Import an ntriple file into KGTK file'
    }


def add_arguments(parser):
    """
    Parse arguments
    Args:
        parser (argparse.ArgumentParser)
    """
    parser.add_argument("-i",'--inp', action="store", type=str, dest="input_file",help='input file path')
    parser.add_argument("-o",'--out', action="store", type=str, dest="output_file",help='output file path')
    parser.add_argument("--limit", action="store", type=int, dest="limit",default=None,help='number of lines of input file to run on, default: runs on all')
    
    
    
def run(input_file, output_file, limit):
    # import modules locally
    import re
    import csv
    from kgtk.exceptions import KGTKException
    from kgtk.cli_argparse import KGTKArgumentParser
    
    
    
    try:
        regex = r"\"(?:\\\"|[^\"])+\"|[^\s]+"
        write = True
        errors = 0
        rows = []
        header = []
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
        data_dict = {}
        if write:
            with open(output_file, 'w', newline='') as myfile:
                wr = csv.writer(
                    myfile,
                    quoting=csv.QUOTE_NONE,
                    delimiter="\t",
                    escapechar="\n",
                    quotechar='')
                wr.writerow(header)
        with open(input_file, mode='r') as file:
            print('processing the ntriple file now...')
            for cnt, full_line in enumerate(file):
                matches = re.finditer(regex, full_line, re.MULTILINE)
                line = []
                for m in matches:
                    line.append(m.group())
                keep = True
                if limit and cnt >= limit:
                    break
                if cnt % 500000 == 0 and cnt > 0:
                    print('processed {} lines'.format(cnt))
                if len(line) < 4 or len(line) > 5:
                    errors += 1
                    #print(line)
                    keep = False
                if keep:
                    final_row = []
                    final_row.append(line[0])
                    final_row.append(line[1])
                    subject_isuri = False
                    if line[2].startswith('\"') and line[2].endswith('\"'):
                        line[2] = line[2][1:-1]
                    if line[3] != '.':
                        subject = line[2] + line[3]
                    else:
                        subject = line[2]
                    if '^^' in subject:
                        subject_parts = subject.split('^^')
                        value = subject_parts[0]
                        datatype = subject_parts[1]
                        if 'www.w3.org' in subject:
                            if 'boolean' in datatype:
                                final_value = value.capitalize()
                            elif 'date' in datatype:
                                final_value = '^' + value + 'T00:00:00Z/11'
                            elif 'YearMonth' in datatype:
                                final_value = '^' + value + '-01T00:00:00Z/10'
                            elif 'Year' in datatype:
                                final_value = '^' + value + '-01-01T00:00:00Z/9'
                            else:
                                final_value = value
                        else:
                            datatype = datatype.replace('<', '')
                            datatype = datatype.replace('>', '')
                            final_value = '!' + value + '^^' + datatype
                    else:
                        datatype = ''
                        if subject.startswith('<'):
                            subject_isuri = True
                            final_value = subject
                        else:
                            if '@' in subject:
                                str_parts = subject.split('@')
                                final_value = '\'' + \
                                    str_parts[0].replace("'","\\'") + '\'@' + str_parts[1]
                            else:
                                final_value = '\"' + str(subject) + '\"'
                    final_row.append(final_value)
                    n1_parts = line[0].rsplit('/', 1)
                    final_row += n1_parts
                    label_parts = line[1].rsplit('/', 1)
                    final_row += label_parts
                    if subject_isuri:
                        subject_parts = subject.rsplit('/', 1)
                        final_row += subject_parts
                    else:
                        final_row += [':', final_value]
                    final_row.append(datatype)
                    rows.append(final_row)
                    for i in range(len(final_row)):
                        final_row[i] = final_row[i].replace('<', '')
                        final_row[i] = final_row[i].replace('>', '')
                        if (not subject_isuri) and i == 2:
                            final_row[i] = final_value
                if write:
                    if cnt % 50000 == 0 and cnt > 0:
                        with open(output_file, 'a', newline='') as myfile:
                            for row in rows:
                                wr = csv.writer(
                                    myfile,
                                    quoting=csv.QUOTE_NONE,
                                    delimiter="\t",
                                    escapechar="\n",
                                    quotechar='')
                                wr.writerow(row)
                            rows = []
            if write:
                with open(output_file, 'a', newline='') as myfile:
                    for row in rows:
                        wr = csv.writer(
                            myfile,
                            quoting=csv.QUOTE_NONE,
                            delimiter="\t",
                            escapechar="\n",
                            quotechar='')
                        wr.writerow(row)               
        print('{} invalid lines in ntriple file'.format(errors))
        print('import complete')
    except:
        raise KGTKException
