from ldap3 import Server, Connection, ALL, NTLM
# from django.conf import settings
from icorp.icorp import settings


def search():
    conn.search('dc=kzp,dc=in',
                '(sAMAccountName=ilmir.ziganshin)',
                attributes=['OU', 'cn', 'sAMAccountName', 'userPrincipalName', 'objectClass', 'memberOf'])
    print(conn.entries)

def create_user(first_name, last_name, p,user_name, password):
    p = f" {p}" if p else ''
    cn = f"{last_name} {first_name}{p}"
    conn.add(f'cn={p},ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org', 'inetOrgPerson',
             {'givenName': 'Beatrix', 'sn': 'Young', 'departmentNumber': 'DEV', 'telephoneNumber': 1111})


if __name__ == '__main__':
    from environs import Env
    env = Env()
    env.read_env()
    server = Server(env.str("AD_HOST"), get_info=ALL)

    conn = Connection(server,
                      user=env.str("AD_ADMIN_NAME"),
                      password=env.str("AD_ADMIN_PASSWORD"),
                      authentication=NTLM)
    conn.bind()
    search()
