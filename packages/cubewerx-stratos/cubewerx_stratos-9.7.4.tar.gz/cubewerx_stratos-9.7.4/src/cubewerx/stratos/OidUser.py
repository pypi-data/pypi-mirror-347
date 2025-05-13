# $Id: OidUser.py 78570 2025-01-23 18:57:06Z pomakis $

from typing import TypedDict


class OidUser(TypedDict):
    """An OpenID Connect user identity.

    KEYS:
        issuer - the issuer URL of the OpenID Connect server that provides
            the identity
        sub - the "sub" (subject) claim of the user identity at the
            specified OpenID Connect server, or None to refer to all
            user identities at the specified OpenID Connect server
    """

    issuer: str
    sub: str | None
