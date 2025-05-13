# $Id: Layer.py 79043 2025-05-05 19:50:09Z pomakis $

from __future__ import annotations
import os
import requests
from urllib.parse import quote
import zipfile
import tempfile

from .DataStore import *
from .SourceImage import *
from .MultilingualString import *
from .CwException import *


class Layer:
    """A layer (called a "collection" in the OGC API) that's available
    through a data store.

    Do not instantiate directly.  To add a layer to a data store,
    call either DataStore.addVectorLayer() or DataStore.addCoverageLayer().
    """

    def __init__(self, jsonRep: dict, dataStore: DataStore,
                 collectionsUrl: str, authorizationToken: str):
        self.__id = jsonRep.get("id")
        if not self.__id:
            raise ValueError("jsonRep missing required 'id' field")
        self.__title = jsonRep.get("title")
        self.__description = jsonRep.get("description")
        self.__links = jsonRep.get("links", [])

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

        self.__isVectors = (jsonRep.get("itemType") == "feature")
        self.__isCoverage = False
        self.__isMappable = False
        for link in self.__links:
            rel = link.get("rel")
            if rel:
                if rel.endswith("/coverage") or rel.endswith(":coverage]"):
                    self.__isCoverage = True
                elif rel.endswith("/coverage-scenes"):
                    self.__isCoverage = True
                elif rel.endswith(":coverage-scenes]"):
                    self.__isCoverage = True
                elif rel.endswith("/map") or rel.endswith(":map]"):
                    self.__isMappable = True

        self.__dataStore = dataStore
        self.__collectionUrl = collectionsUrl + "/" + quote(self.__id)
        self.__authorizationToken = authorizationToken

    @property
    def id(self) -> str:
        """the ID/name of this layer"""
        return self.__id

    @property
    def title(self) -> str | None:
        """the title of this layer, or None"""
        return self.__title

    @property
    def description(self) -> str | None:
        """a brief textual description of this layer, or None"""
        return self.__description

    @property
    def wgs84Extent(self) -> list | None:
        """the WGS 84 Geographic bounding box of this layer ([minLon,
        minLat, maxLon, maxLat]), or None; if minLon > maxLon, then the
        bounding box spans the antimeridian"""
        return self.__wgs84Extent

    # TODO: temporalExtent property
    # TODO: nativeCrs property
    # TODO: styles property
    # TODO: defaultStyle property

    @property
    def isVectors(self) -> bool:
        """whether or not this a vector (or empty) layer"""
        return self.__isVectors

    @property
    def isCoverage(self) -> bool:
        """whether or not this a coverage (or empty) layer"""
        return self.__isCoverage

    @property
    def isMappable(self) -> bool:
        """whether or not maps can be requested from this layer"""
        return self.__isMappable

    @property
    def canBeManaged(self) -> bool:
        """whether or the data of this layer can be manipulated"""
        return self.__dataStore.type == "cubestor"

    # TODO: somehow add the ability to change the layer's title and description

    def getSourceImages(self, includeGood: bool = True,
                        includeBad: bool = False) -> list[SourceImage]:
        """Return a list of the source images of this layer.

        Returns a list of all of the source images of this layer,
        regardless of what collection they're in.  Only useful for
        coverage layers.

        ARGUMENTS:
            includeGood - whether or not to include good source images
            includeBad - whether or not to include bad source images
        RETURNS:
            a list of the source images of this layer
        """
        # Fetch the .../collections/{collectionId}/scenes document.
        scenesUrl = self.__collectionUrl + "/scenes"
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken
        }
        params = {
            "includeGood": includeGood,
            "includeBad": includeBad,
            "limit": 1000000,
        }
        response = requests.get(scenesUrl, headers=requestHeaders,
            params=params)
        ServerException.raise_for_status(response)
        responseJson = response.json()

        # Parse the scenes into SourceImage objects.
        sourceImages = []
        scenesJson = responseJson.get("scenes");
        if isinstance(scenesJson, list):
            for sceneJson in scenesJson:
                sourceImage = SourceImage(sceneJson, scenesUrl,
                    self.__authorizationToken)
                if sourceImage: sourceImages.append(sourceImage)

        return sourceImages

    def addSourceImages(self, filePaths: list[str],
                        hints: SourceImageHints = None,
                        updateTiles: bool | None = None) -> list[SourceImage]:
        """Add one or more source images to this coverage layer.

        Adds one or more source images to this layer.  This can only
        be done if (canBeManaged and isCoverage).  Source images added in
        this way don't get added to a specific collection.  Also note that
        this does not update the wgs84Extent propery of the layer object.

        ARGUMENTS:
            filePaths - the fully-qualified local file paths to the source
                image(s) to be added, including any necessary auxilliary
                files; alternatively, a ZIP file containing the source
                image(s) to be added can be specified, as long as it meets
                the following requirements: a) it's the only specified
                file, b) it has a '.zip' suffix, and c) it consists only
                of files or of exactly one directory whose contents exist
                only of files
            hints - hints to help the CubeWerx Stratos server interpret
                the source images, or None
            updateTiles - whether or not the data and map tiles of the
                layer should be updated, or None for auto;  None (auto)
                is typically the best option, since it will intelligently
                perform tile updates using delay timers to insure that an
                unnecessary number of tile updates is not performed.
        RETURNS:
            a list of the source images that were added; note that some of
            the source images may be marked as bad, and should be adjusted
            or removed
        """
        nFiles = len(filePaths)
        if nFiles < 1:
            # No source images were specified.  Trivial return.
            return []
        elif nFiles == 1 and filePaths[0].endswith('.zip'):
            # A ZIP file was specified.  Open it.
            zipFile = os.open(filePaths[0], 'rb')
        else:
            # One or more source-image files were specified.  Package
            # them together into a temporary ZIP archive.
            zipFile = tempfile.TemporaryFile(suffix='.zip')
            zipArchive = zipfile.ZipFile(zipFile, "x")
            for filePath in filePaths:
                filename = os.path.basename(filePath)
                if filename:
                    zipArchive.write(filePath, filename)
            zipArchive.close()
            zipFile.seek(0)

        # Make an HTTP POST request to the scenes endpoint.
        scenesUrl = self.__collectionUrl + "/scenes"
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken,
            "Content-Type": "application/zip"
        }
        params = {}
        if (hints is not None):
             params.update(hints._dict)
        if updateTiles is not None:
            params["updateTiles"] = bool(updateTiles)
        response = requests.post(scenesUrl, headers=requestHeaders,
                                 params=params, data=zipFile)
        ServerException.raise_for_status(response)
        responseJson = response.json()

        # Close (and remove) the temporary ZIP file.
        zipFile.close()

        # Read the resulting SourceImage objects from the response.
        sourceImages = []
        if isinstance(responseJson, list):
            for sceneJson in responseJson:
                sourceImage = SourceImage(sceneJson, scenesUrl,
                    self.__authorizationToken)
                if sourceImage: sourceImages.append(sourceImage)

        # We're done!
        return sourceImages

    def removeSourceImage(self, sourceImage: SourceImage | str,
                           updateTiles: bool | None = None):
        """Remove a source image from this coverage layer.

        Removes a source image from this layer, regardless of whether or
        not they're in a specific collection.  This can only be done if
        (canBeManaged and isCoverage).  Also note that this does not
        update the wgs84Extent propery of the layer object.

        ARGUMENTS:
            sourceImage - the source-image object or ID to remove
            updateTiles - whether or not the data and map tiles of the
                layer should be updated, or None for auto;  None (auto)
                is typically the best option, since it will intelligently
                perform tile updates using delay timers to insure that an
                unnecessary number of tile updates is not performed.
        """
        return self.removeSourceImages([sourceImage], updateTiles)

    def removeSourceImages(self, sourceImages: list[SourceImage|str],
                           updateTiles: bool | None = None):
        """Remove one or more source images from this coverage layer.

        Removes one or more source images from this layer, regardless of
        whether or not they're in a specific collection.  This can only
        be done if (canBeManaged and isCoverage).  Also note that this
        does not update the wgs84Extent propery of the layer object.

        ARGUMENTS:
            sourceImages - the source-image objects or IDs to remove
            updateTiles - whether or not the data and map tiles of the
                layer should be updated, or None for auto;  None (auto)
                is typically the best option, since it will intelligently
                perform tile updates using delay timers to insure that an
                unnecessary number of tile updates is not performed.
        """
        scenesUrl = self.__collectionUrl + "/scenes"
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken,
        }

        # Make an HTTP DELETE request to each specified scene.
        # Pass updateTiles=false to all but the last one.
        nSourceImages = len(sourceImages)
        for i in range(nSourceImages):
            sourceImage = sourceImages[i]
            sceneId = sourceImage.id if isinstance(sourceImage, SourceImage) \
                else sourceImage
            sceneUrl = scenesUrl + "/" + sceneId

            if i < nSourceImages-1:
                params = { "updateTiles": false }
            elif updateTiles is not None:
                params = { "updateTiles": bool(updateTiles) }
            else:
                params = {}

            response = requests.delete(sceneUrl, headers=requestHeaders,
                                       params=params)
            ServerException.raise_for_status(response)

    def getCollections(self) -> list[Collection]:
        pass # TODO: implement

    def addCollection(self):
        #TODO: other parameters TBD
        pass # TODO: implement

    def removeCollection(self, collection: Collection | str):
        pass # TODO: implement

