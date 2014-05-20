

def get_ipt_params(classifier):
    result = u''
    if classifier.protocol:
        result += u'-p ' + classifier.protocol + u' '
    if classifier.src_ip:
        result += u'-src ' + classifier.src_ip + u' '
    if classifier.dst_ip:
        result += u'-dst ' + classifier.dst_ip + u' '
    if classifier.input_if:
        result += u'-i ' + classifier.input_if.name + u' '
    if classifier.output_if:
        result += u'-o ' + classifier.output_if.name + u' '
    if classifier.src_ports:
        result += u'-m multiport --sports ' + classifier.src_ports + u' '
    if classifier.dst_ports:
        result += u'-m multiport --dports ' + classifier.dst_ports + u' '
    if classifier.icmp_type:
        result += u'--icmp-type ' + classifier.icmp_type + u' '
    return result
