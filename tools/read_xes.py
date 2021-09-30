import xmltodict
from json import dumps,loads

"""
Code from https://github.com/FrankBGao/read_xes
"""

def get_one_event_dict(one_event, case_name,data_types):

    one_event_attri = list(one_event.keys())

    one_event_dict = {}
    for i in data_types:
        if i in one_event_attri:
            if type(one_event[i]) == list:
                for j in one_event[i]:
                    one_event_dict[j['@key']] = j['@value']
            else:
                one_event_dict[one_event[i]['@key']] = one_event[i]['@value']
    one_event_dict['case_name'] = case_name
    return one_event_dict

def gain_one_trace_info(one_trace,data_types):
    # for the attributer
    one_trace_attri = list(one_trace.keys())
    one_trace_attri_dict = {}

    for i in data_types:
        if i in one_trace_attri:
            if type(one_trace[i]) == list:
                for j in one_trace[i]:
                    one_trace_attri_dict[j['@key']] = j['@value']
            else:
                one_trace_attri_dict[one_trace[i]['@key']] = one_trace[i]['@value']

    # for event seq
    one_trace_events = []
    if type(one_trace['event']) == dict:
        one_trace['event'] = [one_trace['event']]

    for i in one_trace['event']:
        inter_event = get_one_event_dict(i, one_trace_attri_dict['concept:name'],data_types)
        one_trace_events.append(inter_event)

    return one_trace_attri_dict,one_trace_events

def gain_log_info_table(xml_string):
    data_types = ['string', 'int', 'date', 'float', 'boolean', 'id']

    log_is = xmltodict.parse(xml_string)
    log_is = loads(dumps(log_is))

    traces = log_is['log']['trace']

    trace_attri = []
    trace_event = []
    j = 0
    for i in traces:
        inter = gain_one_trace_info(i,data_types)
        trace_attri.append(inter[0])
        trace_event = trace_event + inter[1]
        j = j +1
        # print(j)
    return trace_attri,trace_event


xml_string = open("../BPI Challenge 2017.xes",mode='r').read()

inter = gain_log_info_table(xml_string)

trace_attri = inter[0]
trace_event = inter[1]
print(inter)