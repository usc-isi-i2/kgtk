##########################################
#    Utility Functions
##########################################

def gen_qnode(property_, start, end, unit=None):
    if not unit:
        return f'Interval-{property_}({start}_{end})'
    return f'Interval-{property_}|{unit}({start}_{end})'


def gen_qlabel(property_, start, end, unit=None):
    if not unit:
        return f'{property_}({start}_{end})'
    return f'{property_}|{unit}({start}_{end})'


def gen_pnode(pnode, unit=None):
    if not unit:
        return f'Interval-{pnode}'
    return f'Interval-{pnode}|{unit}'


def gen_plabel(pnode, unit=None):
    if not unit:
        return pnode + ' (Interval)'
    return pnode + ' ' + unit + ' (Interval)'


def parse_number(s):
    """
    Parsing the literals in Wikidata
    """
    if s[0] != '-' and '-' in s:
        try:
            return int(s.split('-')[0])
        except:
            try:
                print(s)
                return int(s.split('-')[0][:-1]) * 10
            except:
                print(s)
                return int(s.split('-')[0][:-2]) * 100
    return float(s.split('^^')[0])
