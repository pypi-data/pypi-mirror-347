# $Id: AuthUser.py 79029 2025-05-01 15:39:41Z pomakis $

import validators


class AuthUser:
    """A CubeWerx Stratos CwAuth user account.

    To create a new CubeWerx Stratos CwAuth user, create a new AuthUser
    object (specifying the desired username), set the required e-mail
    address and password for the user, set any other desired properties,
    and call the addOrReplaceAuthUser() method of the Stratos object.

    To change the details of an existing CubeWerx Stratos CwAuth
    user account, fetch the AuthUser object via the getAuthUsers()
    or getAuthUser() method of the Stratos object, update one or more
    properties of that user, and call the updateAuthUser() method of
    the Stratos object to commit those changes.

    To remove a CubeWerx Stratos CwAuth user account, call the removeUser()
    method of the Stratos object.

    ARGUMENTS:
        username - the user's username; each CubeWerx Stratos CwAuth user
            account must have a unique username; required unless supplied
            via the dictionary parameter
        dictionary - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, username: str=None, dictionary: dict={}):
        if username:
            if not "username" in dictionary: dictionary["username"] = username
        elif not "username" in dictionary:
            raise Exception("username needs to be specified")
        self._dict = dictionary

        # Keep track of the properties that are programmatically changed
        # so that an appropriate patch dictionary can be constructed.
        self.__firstNameChanged = False
        self.__lastNameChanged = False
        self.__emailAddressChanged = False
        self.__rolesChanged = False
        self.__maxSeatsChanged = False
        self.__isEditableChanged = False
        self.__isEnabledChanged = False

    @property
    def username(self):
        """the unique username of this CubeWerx Stratos CwAuth user
        account"""
        return self._dict.get("username")

    @property
    def firstName(self) -> str | None:
        """the first (given) name of this CubeWerx Stratos CwAuth user
        account (possibly also with middle name(s) and/or initial(s)),
        or None"""
        return self._dict.get("firstName")

    @firstName.setter
    def firstName(self, value: str | None):
        if value:
            self._dict["firstName"] = str(value)
        else:
            del self._dict["firstName"]
        self.__firstNameChanged = True

    @property
    def lastName(self) -> str | None:
        """the last (family) name (i.e., surname) of this CubeWerx
        Stratos CwAuth user account, or None"""
        return self._dict.get("lastName")

    @lastName.setter
    def lastName(self, value: str | None):
        if value:
            self._dict["lastName"] = str(value)
        else:
            del self._dict["lastName"]
        self.__lastNameChanged = True

    @property
    def displayName(self) -> str:
        """an appropriate name to display for this CubeWerx Stratos
        CwAuth user account, either the user's first and/or last name
        if set, or the user's username otherwise"""
        displayName = ""
        firstName = self._dict.get("firstName")
        lastName = self._dict.get("lastName")
        if firstName: displayName += firstName
        if firstName and lastName: displayName += " "
        if lastName: displayName += lastName
        if not displayName: displayName = self._dict.get("username")
        return displayName

    @property
    def emailAddress(self) -> str | None:
        """the e-mail address of this CubeWerx Stratos CwAuth user
        account, or None"""
        return self._dict.get("emailAddress")

    @emailAddress.setter
    def emailAddress(self, value: str):
        if not validators.email(str(value)):
            raise ValueError("Invalid emailAddress")
        self._dict["emailAddress"] = str(value)
        self.__emailAddressChanged = True

    @property
    def roles(self) -> list[str]:
        """the list of roles that this CubeWerx Stratos CwAuth user
        account has; these are the role names only; to get the full
        Role objects (for descriptions, etc.), pass this list to the
        getRoles() method of the Stratos object; this list of roles can
        be re-specified with a user.roles = [...] assignment; however,
        to add or remove a role to/from the existing list, use the
        addRole() or removeRole() methods rather than user.roles.append()
        or user.roles.remove()"""
        return self._dict.get("roles", [])

    @roles.setter
    def roles(self, value: list[str]):
        self._dict["roles"] = value if value else []
        self.__rolesChanged = True

    def addRole(self, roleName: str):
        """Add a role to this CubeWerx Stratos CwAuth user account.

        ARGUMENTS:
            roleName - the name of the role to add to this CubeWerx
                Stratos CwAuth user account; the specified role must
                exist; if the user already has this role, this is a no-op
        RETURNS:
            (nothing)
        """
        if roleName:
            if not self._dict.get("roles"): self._dict["roles"] = []
            if not roleName in self._dict["roles"]:
                self._dict["roles"].append(roleName)
            self.__rolesChanged = True

    def removeRole(self, roleName: str):
        """Remove a role from this CubeWerx Stratos CwAuth user account.

        ARGUMENTS:
            roleName - the name of the role to remove (revoke) from this
                CubeWerx Stratos CwAuth user account; if the user doesn't
                have this role, this is a no-op
        RETURNS:
            (nothing)
        """
        if (self._dict["roles"] and roleName and
                roleName in self._dict["roles"]):
            self._dict["roles"].remove(roleName)
            self.__rolesChanged = True

    @property
    def maxSeats(self) -> int | None:
        """the maximum number of times this CubeWerx Stratos CwAuth user
        account can be logged in, or None"""
        return self._dict.get("maxSeats")

    @maxSeats.setter
    def maxSeats(self, value: int | None):
        if value is not None and int(value) >= 0:
            self._dict["maxSeats"] = int(value)
        else:
            del self._dict["maxSeats"]
        self.__maxSeatsChanged = True

    @property
    def isEditable(self) -> bool:
        """is this CubeWerx Stratos CwAuth user allowed to edit their
        own information?"""
        return self._dict.get("isEditable", True)

    @isEditable.setter
    def isEditable(self, value: bool):
        self._dict["isEditable"] = bool(value)
        self.__isEditableChanged = True

    @property
    def isEnabled(self) -> bool:
        """is this CubeWerx Stratos CwAuth user account enabled (i.e.,
        can users sign in with this account)?"""
        return self._dict.get("isEnabled", True)

    @isEnabled.setter
    def isEnabled(self, value: bool):
        self._dict["isEnabled"] = bool(value)
        self.__isEnabledChanged = True

    @property
    def password(self) -> str | None:
        """the password for this CubeWerx Stratos CwAuth user account,
        or None; note that none of the user information returned by the
        getUsers() or getUser() methods of the Stratos object will
        include a password; however, a password must be set for the
        addOrReplaceAuthUser() method"""
        return self._dict.get("password")

    @password.setter
    def password(self, value: str):
        self._dict["password"] = str(value) if str(value) else ""

    @property
    def _patchDict(self) -> dict:
        patch = {}
        if self.__firstNameChanged:
            patch["firstName"] = self.firstName
        if self.__lastNameChanged:
            patch["lastName"] = self.lastName
        if self.__emailAddressChanged:
            patch["emailAddress"] = self.emailAddress
        if self.__rolesChanged:
            patch["roles"] = self.roles
        if self.__maxSeatsChanged:
            patch["maxSeats"] = self.maxSeats
        if self.__isEditableChanged:
            patch["isEditable"] = self.isEditable
        if self.__isEnabledChanged:
            patch["isEnabled"] = self.isEnabled
        return patch
