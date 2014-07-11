import ldap


def extruct_group(fqdn):
    return fqdn.split(',')[0].replace('CN=', '')


def extruct_group_list(data):
    groups = []
    for fqdn in data:
        groups.append(extruct_group(fqdn).lower())
    return groups


def get_user_info(
        ldap_domain,
        ldap_tree_scoupe,
        user_name,
        bind_user_name,
        bind_password,
):

    l = ldap.initialize("ldap://" + ldap_domain)
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.protocol_version = 3
    try:
        l.simple_bind_s(bind_user_name + "@" + ldap_domain, bind_password)
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


class LdapAuthHelper(object):

    def __init__(self, config):
        super(LdapAuthHelper, self).__init__()
        self.ldap_domain = config['LDAP_DOMAIN']
        self.ldap_tree_scoupe = config['LDAP_TREE']
        self.ldap_inet_group = config['LDAP_INET_GROUPT']
        self.ldap_bind_user = config['LDAP_BIND_USER']
        self.ldap_bind_password = config['LDAP_BIND_PASSWORD']

    def get_user_info(self, user_name, password):
        bind_user_name = user_name
        bind_password = password
        if (not self.ldap_bind_user is None) and (not self.ldap_bind_password is None):
            bind_user_name = self.ldap_bind_user
            bind_password = self.ldap_bind_password

        return get_user_info(
            self.ldap_domain,
            self.ldap_tree_scoupe,
            user_name,
            bind_user_name,
            bind_password,
        )

    def auth(self, user_name, password):
        info = self.get_user_info(user_name, password)
        if info is None:
            return False
        if self.ldap_inet_group in info['groups']:
            return True
        return False
