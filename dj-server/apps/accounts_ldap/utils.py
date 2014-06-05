import ldap


def extruct_group(fqdn):
    return fqdn.split(',')[0].replace('CN=', '')


def extruct_group_list(data):
    groups = []
    for fqdn in data:
        groups.append(extruct_group(fqdn).lower())
    return groups


def get_user_info(ldap_domain, ldap_tree_scoupe, user_name, password):
    l = ldap.initialize("ldap://" + ldap_domain)
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.protocol_version = 3
    try:
        l.simple_bind_s(user_name + "@" + ldap_domain, password)
    except:
        return None

    r = l.search(
        ldap_tree_scoupe,
        ldap.SCOPE_SUBTREE,
        '(&(objectCategory=person)(objectClass=user)(sAMAccountName={0}))'.format(user_name),
        ['sAMAccountName', 'memberOf', 'displayName']
    )

    Type, Rez = l.result(r, 1, 10)

    params = {}
    params['full_name'] = Rez[0][1]['displayName'][0]
    params['user_name'] = Rez[0][1]['sAMAccountName'][0].lower()
    params['groups'] = extruct_group_list(Rez[0][1]['memberOf'])
    return params
