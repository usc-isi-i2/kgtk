from __future__ import unicode_literals

import bz2
import simplejson as json
import logging
import csv

logger = logging.getLogger(__name__)
def wikidata_to_csv(wikidata_file, doc_id='Wikidata', limit=None, to_print=False, lang="en", parse_descr=True):
    # Read the JSON wiki data and parse out the entities. Takes about 7-10h to parse 55M lines.
    # get latest-all.json.bz2 from https://dumps.wikimedia.org/wikidatawiki/entities/

    site_filter = '{}wiki'.format(lang)

    WD_META_ITEMS = [
    "Q163875",
    "Q191780",
    "Q224414",
    "Q4167836",
    "Q4167410",
    "Q4663903",
    "Q11266439",
    "Q13406463",
    "Q15407973",
    "Q18616576",
    "Q19887878",
    "Q22808320",
    "Q23894233",
    "Q33120876",
    "Q42104522",
    "Q47460393",
    "Q64875536",
    "Q66480449",
    ]

    # filter: currently defined as OR: one hit suffices to be removed from further processing
    exclude_list = WD_META_ITEMS
    
    # punctuation
    exclude_list.extend(["Q1383557", "Q10617810"])

    # letters etc
    exclude_list.extend(["Q188725", "Q19776628", "Q3841820", "Q17907810", "Q9788", "Q9398093"])

    neg_prop_filter = {
        'P31': exclude_list,    # instance of
        'P279': exclude_list    # subclass
    }

    title_to_id = dict()
    id_to_descr = dict()
    id_to_alias = dict()

    # parse appropriate fields - depending on what we need in the KB
    parse_properties = False
    parse_sitelinks = True
    parse_labels = True
    parse_aliases = True
    parse_claims = True
    
    # create the header of the csv file
    header=[]
    header.append('id')
    if parse_labels:
        header.append('label')
    header.append('type')
    if parse_descr:
        header.append('descriptions')
    if parse_aliases:
        header.append('aliases')
    header.append('document_id')
    with open('nodes.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        
        
    rows=[]
    
    with bz2.open(wikidata_file, mode='rb') as file:
        for cnt, line in enumerate(file):
            keep=False
            if limit and cnt >= limit:
                break
            if cnt % 500000 == 0 and cnt > 0:
                logger.info("processed {} lines of WikiData JSON dump".format(cnt))
                print(cnt)
            clean_line = line.strip()
            if clean_line.endswith(b","):
                clean_line = clean_line[:-1]
            if len(clean_line) > 1:
                obj = json.loads(clean_line)
                entry_type = obj["type"]
                if entry_type == "item" or entry_type == "property":
                    keep = True
                if keep:
                    row=[]
                    qnode=obj["id"]
                    row.append(qnode)
                    
                    
                    if parse_labels:
                        labels = obj["labels"]
                        if labels:
                            lang_label = labels.get(lang, None)
                            if lang_label:
                                row.append('\"'+lang_label['value']+'\"'+"@"+lang)
                                if to_print:
                                    print(
                                        "label (" + lang + "):", lang_label["value"]
                                    )
                            else:
                                row.append("")
                        else:
                            row.append("")
                    row.append(entry_type)

                    if parse_descr:
                        descriptions = obj["descriptions"]
                        if descriptions:
                            lang_descr = descriptions.get(lang, None)
                            if lang_descr:
                                row.append('\"'+lang_descr['value']+'\"'+"@"+lang)
                                if to_print:
                                    print(
                                        "description (" + lang + "):",
                                        lang_descr["value"],
                                    )
                            else:
                                row.append("")
                        else:
                            row.append("")

                    if parse_aliases:
                        aliases = obj["aliases"]
                        if aliases:
                            lang_aliases = aliases.get(lang, None)
                            if lang_aliases:
                                alias_list=[]
                                for item in lang_aliases:
                                    alias_list.append('\"'+item['value']+'\"'+"@"+lang)
                                    if to_print:
                                        print(
                                            "alias (" + lang + "):", item["value"]
                                        )
                                row.append("|".join(alias_list))
                            else:
                                row.append('')
                        else:
                            row.append('')
                                
                    row.append(doc_id)
                    rows.append(row)                 
            if cnt % 50000 == 0 and cnt > 0:
                with open('nodes.csv', 'a', newline='') as myfile:
                    for row in rows:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow(row)
                    rows=[]
    with open('nodes.csv', 'a', newline='') as myfile:
        for row in rows:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(row)
wikidata_to_csv('wikidata-20200203-all.json.bz2','wikidata-20200203')