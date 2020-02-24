from __future__ import unicode_literals

import bz2
import json
import logging
import csv
import time
import uuid

logger = logging.getLogger(__name__)
def wikidata_to_csv(wikidata_file, doc_id='Wikidata', limit=None, to_print=True, lang="en", parse_descr=True):
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
    parse_properties = True
    parse_sitelinks = True
    parse_labels = True
    parse_aliases = True
    parse_claims = True
    
    # create the header of the csv file
    header=[]
    header.append('id')
    header.append('node')
    header.append('property')
    header.append('value')
    header.append('document_id')
    with open('sample.csv', 'w', newline='') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        
    rows=[]
    tempid=uuid.uuid1()
    with bz2.open(wikidata_file, mode='rb') as file:
        for cnt, line in enumerate(file):
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
                if entry_type == "item":
                    keep = True
                    
                claims = obj["claims"]

                if parse_claims:
                    for prop, value_set in neg_prop_filter.items():
                        claim_property = claims.get(prop, None)
                        if claim_property:
                            for cp in claim_property:
                                cp_id = (
                                    cp["mainsnak"]
                                    .get("datavalue", {})
                                    .get("value", {})
                                    .get("id")
                                )
                                cp_rank = cp["rank"]
                                if cp_rank != "deprecated" and cp_id in value_set:
                                    keep = False
                                                                                        
                if keep:
                    qnode=obj["id"]
                    if parse_properties:
                        for prop, claim_property in claims.items():
                            #cp_vals=[]
                            seq_no=1
                            for cp in claim_property:
                                if cp['rank']!='deprecated' and cp['mainsnak']['snaktype']=='value':
                                    val=cp['mainsnak']['datavalue'].get('value')
                                    typ=cp['mainsnak']['datatype']
                                    sid=qnode+'-'+prop+'-'+str(seq_no)
                                    seq_no+=1
                                    if typ.startswith('wikibase'):
                                        rows.append([sid,qnode,prop,val.get('id',''),doc_id])
                                    elif typ=='quantity':
                                        if val.get('upperbound',None) or val.get('lowerbound',None):
                                            rows.append([sid,qnode,prop,val['amount']+'['+val.get('upperbound','')+','+val.get('lowerbound','')+']',doc_id])
                                        else:
                                            rows.append([sid,qnode,prop,val['amount'],doc_id])
                                    elif typ=='globe-coordinate':
                                        rows.append([sid,qnode,prop,'@'+str(val['latitude'])+'/'+str(val['longitude']),doc_id])
                                    elif typ=='time':
                                        rows.append([sid,qnode,prop,val['time']+'/'+str(val['precision']),doc_id])
                                    elif typ=='monolingualtext':
                                        rows.append([sid,qnode,prop,'\"'+val['text']+'\"'+'@'+val['language'],doc_id])           
                                    else:
                                        rows.append([sid,qnode,prop,'\"'+val+'\"',doc_id])
                                        
                                    # get qualifiers for the statements that we are importing    
                                    if cp.get('qualifiers',None):
                                        quals=cp['qualifiers']
                                        for qual_prop, qual_claim_property in quals.items():
                                            qual_seq_no=1
                                            for qcp in qual_claim_property:
                                                if qcp['snaktype']=='value':
                                                    val=qcp['datavalue'].get('value')
                                                    typ=qcp['datatype']
                                                    tempid=sid+'-'+qual_prop+'-'+str(qual_seq_no)
                                                    qual_seq_no+=1
                                                    if typ.startswith('wikibase'):
                                                        rows.append([tempid,sid,qual_prop,val.get('id',''),doc_id])
                                                    elif typ=='quantity':
                                                        if val.get('upperbound',None) or val.get('lowerbound',None):
                                                            rows.append([tempid,sid,qual_prop,val['amount']+'['+val.get('upperbound','')+','+val.get('lowerbound','')+']',doc_id])
                                                        else:
                                                            rows.append([tempid,sid,qual_prop,val['amount'],doc_id])
                                                    elif typ=='globe-coordinate':
                                                        rows.append([tempid,sid,qual_prop,'@'+str(val['latitude'])+'/'+str(val['longitude']),doc_id])
                                                    elif typ=='time':
                                                        rows.append([tempid,sid,qual_prop,val['time']+'/'+str(val['precision']),doc_id])
                                                    elif typ=='monolingualtext':
                                                        rows.append([tempid,sid,qual_prop,'\"'+val['text']+'\"'+'@'+val['language'],doc_id])           
                                                    else:
                                                        rows.append([tempid,sid,qual_prop,'\"'+val+'\"',doc_id])
                            '''
                            if cp_vals:
                                if to_print:
                                    print("prop:", prop, cp_vals)
                            cp_dicts = [
                                cp["mainsnak"]["datavalue"].get("value")
                                for cp in claim_property
                                if cp["mainsnak"].get("datavalue")
                            ]
                            cp_values = [
                                cp_dict.get("id")
                                for cp_dict in cp_dicts
                                if isinstance(cp_dict, dict)
                                if cp_dict.get("id") is not None
                            ]
                            if cp_values:
                                if to_print:
                                    print("prop:", prop, cp_values)
                            '''
            if cnt % 50000 == 0 and cnt > 0:
                with open('sample.csv', 'a', newline='') as myfile:
                    for row in rows:
                        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                        wr.writerow(row)
                    rows=[]
    with open('sample.csv', 'a', newline='') as myfile:
        for row in rows:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(row)
start=time.time()
wikidata_to_csv('wikidata-20200203-all.json.bz2','wikidata-20200203',limit=2)
end=time.time()
print((end-start)/3600)