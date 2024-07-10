from ldap3 import Server, Connection, ALL, NTLM, MODIFY_REPLACE, MODIFY_ADD
import subprocess
from icorp.icorp import settings


server = Server(settings.AD_HOST, get_info=ALL)
conn = Connection(server,
                  user=settings.AD_ADMIN_NAME,
                  password=settings.AD_ADMIN_PASSWORD,
                  authentication=NTLM)


class LDAPUserNotFound(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'User not found: {self.message}'
        else:
            return 'User not found'


class LDAPCreationError(Exception):
    def __init__(self, *args, **kwargs):
        if kwargs['object_class']:
            self.message = f'{kwargs["object_class"]} - '
        if args:
            self.message += args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Object creation error: {self.message}'
        else:
            return 'Object creation error'

class LDAPModificationError(Exception):
    def __init__(self, *args, **kwargs):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f'Modification error: {self.message}'
        else:
            return 'Modification error'


def reset_password(username, new_password):
    powershell_script = f'Set-ADAccountPassword {username} -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "{new_password}" -Force -Verbose) -PassThru'
    subprocess.run(['powershell', powershell_script])


def _search_user_(
        username,
        attributes=['DistinguishedName', 'sAMAccountName', 'userPrincipalName', 'objectClass', 'memberOf']
):
    conn.bind()
    conn.search('dc=kzp,dc=in',
                f'(sAMAccountName={username})',
                attributes=attributes)
    res = conn.entries
    conn.unbind()
    return res


def create_user(first_name, last_name, uis_login, password, position, path_ou, surname=None):
    conn.bind()
    surname = f" {surname}" if surname else ''
    cn = f"{last_name} {first_name}{surname}"
    dn = f"cn={cn},{path_ou}"
    if not conn.add(
            dn=dn,
            object_class="user",
            attributes={
                'displayName': cn,
                'givenName': first_name,
                'sn': last_name,
                "userPrincipalName": uis_login + "@kzp.in",
                "sAMAccountName": uis_login,
                "title": position,
            },
    ):
        raise LDAPCreationError(conn.result, object_class="user")
    res = conn.extend.microsoft.unlock_account(
        user=dn
    )
    reset_password(uis_login, password)
    change_uac_attribute = {
        "userAccountControl": [(MODIFY_REPLACE, [66048])]}
    conn.modify(
            dn=dn,
            changes=change_uac_attribute
    )
    conn.unbind()


def _create_object_(dn, object_class, **attribute):
    conn.bind()
    if not conn.add(
            dn=dn,
            object_class=object_class,
            attributes=attribute
    ):
        conn.unbind()
        raise LDAPCreationError(conn.result, object_class=object_class)
    conn.unbind()


def _unlock_account_(dn):
    conn.bind()
    if not conn.extend.microsoft.unlock_account(
            user=dn
    ):
        conn.unbind()
        raise LDAPCreationError(conn.result, object_class="user")
    conn.unbind()


def _update_attribute_(conn, dn, attribute, value):
    conn.modify(
            dn=dn,
            changes=_create_changes_from_dict({attribute: value}, modifier=MODIFY_REPLACE)
    )


def _modify_(dn, changes):
    conn.bind()
    if not conn.modify(
            dn=dn,
            changes=changes
    ):
        conn.unbind()
        raise LDAPModificationError(conn.result)
    conn.unbind()


def _add_attribute_(dn, attribute, value):
    conn.bind()
    conn.modify(
            dn=dn,
            changes=_create_changes_from_dict({attribute: value}, modifier=MODIFY_ADD)
    )
    conn.unbind()


def _create_changes_from_dict(changes, modifier=MODIFY_REPLACE):
    return {atr_name: [(modifier, [value_])] for atr_name, value_ in changes.items()}


def update_user(user, first_name, last_name, uis_login, password, position, path_ou=None, surname=None):
    conn.bind()
    dn = user.distinguishedName.value
    if path_ou:
        conn.modify_dn(dn, relative_dn=user.cn.value, new_superior=path_ou)
        dn = None
    surname = f" {surname}" if surname else ''
    cn = f"{last_name} {first_name}{surname}"
    if cn != user.cn.value:
        conn.modify_dn(f"cn={user.cn.value},{path_ou}", relative_dn=f"cn={cn}")
    dn = f"cn={cn},{path_ou}"

    if not conn.modify(
            dn=dn,
            changes=_create_changes_from_dict({
                'displayName': cn,
                'givenName': first_name,
                'sn': last_name,
                "userPrincipalName": uis_login + "@kzp.in",
                "sAMAccountName": uis_login,
                "title": position,
            })
    ):
        return "Не удалось обновить учётную запись в AD"
    reset_password(uis_login, password)
    conn.unbind()


class User:
    __default_atrs__ = [
        'DistinguishedName',
        'displayName',
        'givenName',
        'sn',
        'sAMAccountName',
        'userPrincipalName',
        'objectClass',
        'memberOf',
        'title'
    ]

    def __init__(self, username):
        self.get_user(username)

    def identify(self, username)-> bool:
        users = _search_user_(username, self.__default_atrs__)
        if users:
            self.user = users[0]
            return True
        else:
            return False

    def get_user(self, username):
        if self.identify(username):
            return self.user
        else:
            raise LDAPUserNotFound

    def update_attributes(self, **attributes):
        changes = _create_changes_from_dict(attributes, modifier=MODIFY_REPLACE)
        _modify_(self.user.distinguishedName.value, changes)

    def get_attribute(self, attribute):
        if attribute in self.__default_atrs__:
            return getattr(self.user, attribute).value
        else:
            castom = self.__default_atrs__+[attribute]
            user = _search_user_(self.user.sAMAccountName.value, castom)[0]
            return getattr(user, attribute).value


    @staticmethod
    def create_user(first_name, last_name, uis_login, password, position, path_ou, surname=None):
        surname = f" {surname}" if surname else ''
        cn = f"{last_name} {first_name}{surname}"
        dn = f"cn={cn},{path_ou}"
        _create_object_(
            dn,
            "user",
            displayName=cn,
            givenName=first_name,
            sn=last_name,
            userPrincipalName=uis_login + "@kzp.in",
            sAMAccountName=uis_login,
            title=position
        )
        _unlock_account_(dn)
        reset_password(uis_login, password)
        _update_attribute_(dn, 'userAccountControl', 66048)
        return User(uis_login)

    @staticmethod
    def have_user(username):
        return True if _search_user_(username) else False


if __name__ == '__main__':
    user = User('testkzp')
    print(user.get_attribute('sAMAccountName'))
