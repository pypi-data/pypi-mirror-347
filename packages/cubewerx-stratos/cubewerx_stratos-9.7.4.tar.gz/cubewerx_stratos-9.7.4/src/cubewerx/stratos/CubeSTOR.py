# $Id: CubeSTOR.py 79031 2025-05-02 14:53:24Z pomakis $

class CubeSTOR:
    """The details of a CubeSTOR database.

    Do not instantiate directly.  To get a list of CubeSTOR database
    details or the details of a specific CubeSTOR database, call the
    getCubeSTORs() or getCubeSTOR() methods of the Stratos object
    respectively.  To create, update or remove a CubeSTOR database,
    call the addCubeSTOR(), updateCubeSTOR() or removeCubeSTOR() methods
    of the Stratos object respectively.
    """

    def __init__(self, jsonRep: dict):
        self.__dbName = jsonRep.get("dbName")

        title = jsonRep.get("title")
        self.__title = title if title else None

        description = jsonRep.get("description")
        self.__description = description if description else None

        nFeatureSets = jsonRep.get("nFeatureSets")
        self.__nFeatureSets = nFeatureSets if nFeatureSets else 0

        dataStoreName = jsonRep.get("dataStoreName")
        self.__dataStoreName = dataStoreName if dataStoreName else None

        self.__canDelete = bool(jsonRep.get("canDelete", False))

    @property
    def dbName(self) -> str:
        """the name of this CubeSTOR database"""
        return self.__dbName

    @property
    def title(self) -> str | None:
        """the title of this CubeSTOR database, or None"""
        return self.__title

    @property
    def description(self) -> str | None:
        """a brief textual description of this CubeSTOR database, or None"""
        return self.__description

    @property
    def nFeatureSets(self) -> int:
        """the number of feature sets that are in this CubeSTOR database"""
        return self.__nFeatureSets

    @property
    def dataStoreName(self) -> str | None:
        """the name of the data store that this CubeSTOR database is the
        source of, or None if this CubeSTOR database is not the source of
        any data store"""
        return self.__dataStoreName

    @property
    def canDelete(self) -> bool:
        """whether or not this CubeSTOR database can currently be
        removed through this API"""
        return self.__canDelete

