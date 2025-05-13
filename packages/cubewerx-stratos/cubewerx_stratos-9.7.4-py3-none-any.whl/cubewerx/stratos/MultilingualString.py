# $Id: MultilingualString.py 78576 2025-01-27 14:28:16Z pomakis $

from collections import UserDict


class MultilingualString(UserDict):
    """A string expressed in potentially-multiple languages.

    This is a dictionary that maps ISO 639-1/RFC 3066 language identifiers
    (e.g., "en-CA", "fr") to the string expressed in that language.  The
    optional mapping from the empty string ("") indicates the string
    expressed in an unknown/default language.
    """

    def __init__(self, value: str | dict[str,str]):
      if isinstance(value, dict):
        super().__init__(value)
      else:
        super().__init__({"": str(value)})

    @property
    def _jsonRep(self) -> str | dict[str,str]:
        nKeys = len(self.data)
        if nKeys == 0:
            return ""
        elif nKeys == 1 and "" in self.data:
            return str(self.data[""])
        else:
            return self.data

