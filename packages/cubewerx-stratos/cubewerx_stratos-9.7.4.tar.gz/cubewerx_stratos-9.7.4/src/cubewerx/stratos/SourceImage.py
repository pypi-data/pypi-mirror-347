# $Id: SourceImage.py 79031 2025-05-02 14:53:24Z pomakis $

from urllib.parse import quote

from .SourceImageHints import *
from .CwException import *


class SourceImage:
    """A source image (called a "scene" in the OGC API) of a coverage layer.

    Do not instantiate directly.  To add source images to a coverage
    layer, call Layer.addSourceImages().
    """

    def __init__(self, jsonRep: dict, scenesUrl: str,
                 authorizationToken: str):
        self.__id = jsonRep.get("id")
        if not self.__id:
            raise ValueError("jsonRep missing required 'id' field")
        self.__title = jsonRep.get("title")
        self.__links = jsonRep.get("links", [])
        self.__nominalResM = jsonRep.get("ogc:nominalResM")
        self.__dataCitation = jsonRep.get("ogc:citation")
        self.__hints = SourceImageHints(jsonRep.get("hints", {}))
        self.__isGood = bool(jsonRep.get("isGood", True))
        self.__errorMessage = jsonRep.get("errorMessage")

        self.__wgs84Extent = None
        extentJson = jsonRep.get("extent")
        if extentJson:
            spatialJson = extentJson.get("spatial")
            if spatialJson:
                bboxJson = spatialJson.get("bbox")
                if isinstance(bboxJson, list) and len(bboxJson) > 0:
                    firstBbox = bboxJson[0]
                    if isinstance(firstBbox, list) and len(firstBbox) > 3:
                        self.__wgs84Extent = firstBbox

        self.__sceneUrl = scenesUrl + "/" + quote(self.__id)
        self.__authorizationToken = authorizationToken

    @property
    def id(self) -> str:
        """the ID/name of this source image"""
        return self.__id

    @property
    def title(self) -> str | None:
        """the title of this source image, or None"""
        return self.__title

    @property
    def wgs84Extent(self) -> list | None:
        """the WGS 84 Geographic bounding box of this source image ([minLon,
        minLat, maxLon, maxLat]), or None; if minLon > maxLon, then the
        bounding box spans the antimeridian"""
        return self.__wgs84Extent

    @property
    def nominalResM(self) -> float | None:
        """the nominal resoution of this source image in metres, or None"""
        return self.__nominalResM

    @property
    def dataCitation(self) -> str | None:
        """citation for the source of this source image, or None"""
        return self.__dataCitation

    @property
    def isGood(self) -> bool:
        """if false, this source image is unuseable for the reason
        provided by the errorMessage property; consider adjusting its
        hints or removing it"""
        return self.__isGood

    @property
    def errorMessage(self) -> str | None:
        """an error message describing why the source image is unuseable,
        or None"""
        return self.__errorMessage

    @property
    def hints(self) -> SourceImageHints:
        """hints to help the CubeWerx Stratos server interpret this
        source image"""
        return self.__hints

    def getThumbnailImage(self, maxWidth: int, maxHeight: int):
        """TODO: document
        """
        thumbnailEndpointUrl = None
        for link in self.__links:
            if link.get("rel") == "thumbnail":
                thumbnailEndpointUrl = link.get("href")
                break

        if not thumbnailEndpointUrl:
            return None

        # TODO: implement
        # TODO: what should this return?

    def commitHintChanges(self, updateTiles: bool | None = None):
        """Commits any changes that were made to the hints.

        Commits to the CubeWerx Stratos server any changes that were
        programmatically made to the hints of this source image.  Note
        that this may change the values of some of the properties of
        the source image, including its ID and whether or not it's
        considered a good source image.

        ARGUMENTS:
            updateTiles - whether or not the data and map tiles of the
                layer should be updated, or None for auto;  None (auto)
                is typically the best option, since it will intelligently
                perform tile updates using delay timers to insure that an
                unnecessary number of tile updates is not performed.
        """
        hints = self.hints
        if hints._changed:
            requestHeaders = {
                "Accept": "application/json",
                "Authorization": "CwAuth " + self.__authorizationToken
            }
            params = {}
            if (updateTiles != None):
                params["updateTiles"] = bool(updateTiles)
            response = requests.patch(self.__sceneUrl, headers=requestHeaders,
                json=hints._patchDict)
            ServerException.raise_for_status(response)
