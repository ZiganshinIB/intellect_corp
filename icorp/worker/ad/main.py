from ldap3 import Server, Connection, ALL, NTLM
# from django.conf import settings
from icorp.icorp import settings
def main():
    server = Server(env.str("AD_HOST"), get_info=ALL)

    conn = Connection(server,
                      user=env.str("AD_ADMIN_NAME"),
                      password=env.str("AD_ADMIN_PASSWORD"),
                      authentication=NTLM)
    conn.bind()
    # print(server.schema)
    # print(conn)
    # print(conn.extend.standard.who_am_i())
    conn.search('dc=kzp,dc=in',
                '(objectClass=*)',
                attributes=['cn', 'sAMAccountName', 'userPrincipalName', 'objectClass', 'memberOf'])
    print(conn.entries[100:150])


if __name__ == '__main__':
    from environs import Env
    env = Env()
    env.read_env()
    main()
