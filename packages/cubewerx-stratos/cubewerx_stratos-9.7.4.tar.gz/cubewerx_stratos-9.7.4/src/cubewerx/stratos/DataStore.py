# $Id: DataStore.py 79034 2025-05-02 19:57:22Z pomakis $

import time # for testing
from urllib.parse import quote
from .AccessControlRule import *
from .MultilingualString import *
from .Layer import *


class DataStore:
    """A CubeWerx Stratos data store.

    To create a new CubeWerx Stratos data store, create a new DataStore
    object (specifying the desired name), set the required data store
    type and source properties, set any other desired properties, and
    call the addOrReplaceDataStore() method of the Stratos object.

    To change the details of an existing CubeWerx Stratos data store,
    fetch the DataStore object via the getDataStores() or getDataStore()
    method of the Stratos object, update one or more properties of that
    data store, and call the updateDataStore() method of the Stratos
    object to commit those changes.  Layer manipulation is an exception;
    any changes to the layers of a data store are updated on the server
    immediately.

    To remove a CubeWerx Stratos CwAuth data store, call the
    removeDataStore() method of the Stratos object.

    ARGUMENTS:
        name - the desired name of the data store; each data store must
            have a unique name; required unless supplied via the
            dictionary parameter
        jsonRep - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, name: str=None, jsonRep: dict={}):
        self.__name = jsonRep.get("name")
        if not self.__name:
            self.__name = name
        if not self.__name:
            raise Exception("name needs to be specified")

        # For each changeable property, grab a copy of the string
        # representation of the original value so that we can compare
        # later to see if it has changed (in order to construct a proper
        # PATCH dictionary).

        typeJson = jsonRep.get("type")
        self.__type = str(typeJson) if typeJson else None
        self.__typeOrigRep = repr(self.__type)

        sourceJson = jsonRep.get("source")
        self.__source = str(sourceJson) if sourceJson else None
        self.__sourceOrigRep = repr(self.__source)

        titleJson = jsonRep.get("title")
        self.__title = MultilingualString(titleJson) if titleJson else None
        self.__titleOrigRep = repr(self.__title)

        descriptionJson = jsonRep.get("description")
        self.__description = MultilingualString(descriptionJson) \
            if descriptionJson else None
        self.__descriptionOrigRep = repr(self.__description)

        attributionTitleJson = jsonRep.get("attributionTitle")
        self.__attributionTitle = MultilingualString(attributionTitleJson) \
            if attributionTitleJson else None
        self.__attributionTitleOrigRep = repr(self.__attributionTitle)

        attributionUrlJson = jsonRep.get("attributionUrl")
        self.__attributionUrl = str(attributionUrlJson) \
            if attributionUrlJson else None
        self.__attributionUrlOrigRep = repr(self.__attributionUrl)

        attributionHtmlJson = jsonRep.get("attributionHtml")
        self.__attributionHtml = MultilingualString(attributionHtmlJson) \
            if attributionHtmlJson else None
        self.__attributionHtmlOrigRep = repr(self.__attributionHtml)

        attributionLogoUrlJson = jsonRep.get("attributionLogoUrl")
        self.__attributionLogoUrl = str(attributionLogoUrlJson) \
            if attributionLogoUrlJson else None
        self.__attributionLogoUrlOrigRep = repr(self.__attributionLogoUrl)

        licenseTitleJson = jsonRep.get("licenseTitle")
        self.__licenseTitle = MultilingualString(licenseTitleJson) \
            if licenseTitleJson else None
        self.__licenseTitleOrigRep = repr(self.__licenseTitle)

        licenseUrlJson = jsonRep.get("licenseUrl")
        self.__licenseUrl = str(licenseUrlJson) if licenseUrlJson else None
        self.__licenseUrlOrigRep = repr(self.__licenseUrl)

        licenseHtmlJson = jsonRep.get("licenseHtml")
        self.__licenseHtml = MultilingualString(licenseHtmlJson) \
            if licenseHtmlJson else None
        self.__licenseHtmlOrigRep = repr(self.__licenseHtml)

        isExternalServiceJson = jsonRep.get("isExternalService", False)
        self.__isExternalService = bool(isExternalServiceJson)
        self.__isExternalServiceOrigRep = repr(self.__isExternalService)

        omitDataStoreThemeJson = jsonRep.get("omitDataStoreTheme", False)
        self.__omitDataStoreTheme = bool(omitDataStoreThemeJson)
        self.__omitDataStoreThemeOrigRep = repr(self.__omitDataStoreTheme)

        stylesUrlJson = jsonRep.get("stylesUrl")
        self.__stylesUrl = str(stylesUrlJson) if stylesUrlJson else None
        self.__stylesUrlOrigRep = repr(self.__stylesUrl)

        extraStylesUrlJson = jsonRep.get("extraStylesUrl")
        self.__extraStylesUrl = str(extraStylesUrlJson) \
            if extraStylesUrlJson else None
        self.__extraStylesUrlOrigRep = repr(self.__extraStylesUrl)

        provideSpectralIndexStylesJson = \
            jsonRep.get("provideSpectralIndexStyles")
        self.__provideSpectralIndexStyles = \
            bool(provideSpectralIndexStylesJson)
        self.__provideSpectralIndexStylesOrigRep = \
            repr(self.__provideSpectralIndexStyles)

        simulateTilesJson = jsonRep.get("simulateTiles")
        self.__simulateTiles = simulateTilesJson \
            if isinstance(simulateTilesJson, list) else []
        self.__simulateTilesOrigRep = repr(self.__simulateTiles)

        hintsJson = jsonRep.get("hints")
        self.__hints = hintsJson if isinstance(hintsJson, dict) else {}
        self.__hintsOrigRep = repr(self.__hints)

        accessControlRulesJson = jsonRep.get("accessControlRules")
        self.__accessControlRules = []
        if isinstance(accessControlRulesJson, list):
            for acrJsonRep in accessControlRulesJson:
                self.__accessControlRules.append(AccessControlRule(acrJsonRep))
        self.__accessControlRulesOrigRep = repr(self.__accessControlRules)

        # will be set later by _setServerAssociation
        self.__dataStoreAdminUrl = None
        self.__ogcApiLandingPageUrl = None
        self.__authorizationToken = None

        self.__layerCache = None

    @property
    def name(self) -> str:
        """the unique name of this CubeWerx Stratos data store"""
        return self.__name

    @property
    def type(self) -> str | None:
        """the type of data store (i.e., the type of its source); valid
        values are "cubestor" (for a CubeSTOR database), "oradb" (for a
        CubeWerx OraDB database), "ogcapi" (for an OGC API Service),
        "wms" (for an OGC Web Map Service), "wmts" (for an OGC Web Map
        Tile Service), "wfs" (for an OGC Web Map Feature Service),
        "arcgismap" for an ESRI® ArcGIS® Map service, and "GeoJSON" (for
        a GeoJSON source"""
        return self.__type

    @type.setter
    def type(self, value: str | None):
        self.__type = str(value) if value else None

    @property
    def source(self) -> str | None:
        """the name (for data stores of type "cubestor"), connect string
        (for data stores of type "oradb") or URL (for all other data
        store types) of the source of the data store; for data stores of
        type "cubestor", it's recommended that the GUI admin client
        fetch the list of available CubeSTORs via the getCubeSTORS()
        method of the Stratos object and present them in a drop-down list"""
        return self.__source

    @source.setter
    def source(self, value: str | None):
        self.__source = str(value) if value else None

    @property
    def title(self) -> MultilingualString | None:
        """the title of this data store, or None; if None, the title of
        the source is used"""
        return self.__title

    @title.setter
    def title(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__title = value
            else:
                self.__title = MultilingualString(value)
        else:
            self.__title = None

    @property
    def description(self) -> MultilingualString | None:
        """a brief textual description of this data store, or None; if
        None, the description of the source is used"""
        return self.__description

    @description.setter
    def description(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__description = value
            else:
                self.__description = MultilingualString(value)
        else:
            self.__description = None

    @property
    def attributionTitle(self) -> MultilingualString | None:
        """a human-readable attribution for this data store, or None"""
        return self.__attributionTitle

    @attributionTitle.setter
    def attributionTitle(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__attributionTitle = value
            else:
                self.__attributionTitle = MultilingualString(value)
        else:
            self.__attributionTitle = None

    @property
    def attributionUrl(self) -> str | None:
        """a URL to link to for the attribution of this data store, or
        None"""
        return self.__attributionUrl

    @attributionUrl.setter
    def attributionUrl(self, value: str | None):
        self.__attributionUrl = str(value) if value else None

    @property
    def attributionHtml(self) -> MultilingualString | None:
        """a human-readable attribution (with HTML markup) for this
        data store, or None; overrides both attributionTitle and
        attributionUrl"""
        return self.__attributionHtml

    @attributionHtml.setter
    def attributionHtml(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__attributionHtml = value
            else:
                self.__attributionHtml = MultilingualString(value)
        else:
            self.__attributionHtml = None

    @property
    def attributionLogoUrl(self) -> str | None:
        """a URL of a logo to display for the attribution of this data
        store, or None"""
        return self.__attributionLogoUrl

    @attributionLogoUrl.setter
    def attributionLogoUrl(self, value: str | None):
        self.__attributionLogoUrl = str(value) if value else None

    @property
    def licenseTitle(self) -> MultilingualString | None:
        """human-readable text describing how this data store is
        licensed, or None"""
        return self.__licenseTitle

    @licenseTitle.setter
    def licenseTitle(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__licenseTitle = value
            else:
                self.__licenseTitle = MultilingualString(value)
        else:
            self.__licenseTitle = None

    @property
    def licenseUrl(self) -> str | None:
        """a URL to link to for the license of this data store, or None"""
        return self.__licenseUrl

    @licenseUrl.setter
    def licenseUrl(self, value: str | None):
        self.__licenseUrl = str(value) if value else None

    @property
    def licenseHtml(self) -> MultilingualString | None:
        """human-readable text (with HTML markup) describing how this
        data store is licensed, or None; overrides both licenseTitle and
        licenseUrl"""
        return self.__licenseHtml

    @licenseHtml.setter
    def licenseHtml(self, value: MultilingualString | str | None):
        if value:
            if isinstance(value, MultilingualString):
                self.__licenseHtml = value
            else:
                self.__licenseHtml = MultilingualString(value)
        else:
            self.__licenseHtml = None

    @property
    def isExternalService(self) -> bool:
        """whether or not the source of this data store is an external
        service that CubeWerx Stratos clients can access directly; if
        True the CubeWerx Stratos Geospatial Data Server may redirect
        certain client requests directly to the source server for more
        efficient operation"""
        return self.__isExternalService

    @isExternalService.setter
    def isExternalService(self, value: bool):
        self.__isExternalService = bool(value)

    @property
    def omitDataStoreTheme(self) -> bool:
        """the CubeWerx Stratos WMS and WMTS web services are capable of
        combining multiple data stores into a single set of offerings, and
        furthermore are capable of providing their the list of available
        layers as a hierarchical set of themes; normally each data store
        served by such a web service is given its own top-level theme;
        setting this to True will disable this behavour for this data
        store, putting the offerings of this data store (which may
        themselves be organized by a theme hierarchy) directly as
        top-level items"""
        return self.__omitDataStoreTheme

    @omitDataStoreTheme.setter
    def omitDataStoreTheme(self, value: bool):
        self.__omitDataStoreTheme = bool(value)

    @property
    def stylesUrl(self) -> str | None:
        """a URL to a Styled-Layer Descriptor (SLD) document providing a
        set of styles for (and therefore defining the layers of) the
        coverages and/or feature sets provided by the source of this data
        store; not necessary if the data store source provides its own
        layers and styles"""
        return self.__stylesUrl

    @stylesUrl.setter
    def stylesUrl(self, value: str | None):
        self.__stylesUrl = str(value) if value else None

    @property
    def extraStylesUrl(self) -> str | None:
        """a URL to a Styled-Layer Descriptor (SLD) document providing an
        additional set of styles for the coverages and/or feature sets
        provided by the source of this data store, augmenting what may
        be provided by the data store source or by the stylesUrl field"""
        return self.__extraStylesUrl

    @extraStylesUrl.setter
    def extraStylesUrl(self, value: str | None):
        self.__extraStylesUrl = str(value) if value else None

    @property
    def provideSpectralIndexStyles(self) -> bool:
        """whether or not to provide a set of spectral-index styles for
        the coverages of this data store; for each coverage, only the
        spectral-index styles that are compatible with the channels/bands
        of that coverage will be provided"""
        return self.__provideSpectralIndexStyles

    @provideSpectralIndexStyles.setter
    def provideSpectralIndexStyles(self, value: bool):
        self.__provideSpectralIndexStyles = bool(value)

    @property
    def simulateTiles(self) -> list[str]:
        """some data store types (such as "cubestor", "ogcapi",
        and "wmts") are capable of natively providing map tiles,
        while others aren't; setting this gives the CubeWerx Stratos
        Geospatial Data Server permission to provide a tile interface
        by making tile-sized map requests to the data store source;
        the value is a list of coordinate-reference-system strings
        indicating the coordinate reference systems that such simulated
        tiles should be provided in; it's common to provide tiles in at
        least the Web Mercator (EPSG:3857) coordinate reference system;
        This should only be set to a non-empty list if the data store
        source is incapable of natively providing map tiles"""
        return self.__simulateTiles

    @simulateTiles.setter
    def simulateTiles(self, value: list[str] | str | None):
        if value:
            if isinstance(value, list):
                self.__simulateTiles = value
            else:
                self.__simulateTiles = [ str(value) ]
        else:
            self.__simulateTiles = []

    @property
    def hints(self) -> dict[str,str]:
        """a set of hints to provide to the CubeWerx Stratos convert
        library to help it understand or process the data store source"""
        return self.__hints

    @hints.setter
    def hints(self, value: dict[str,str] | None):
        self.__hints = value if value else []

    @property
    def accessControlRules(self) -> list[AccessControlRule]:
        """the set of access-control rules for this data store"""
        return self.__accessControlRules

    @accessControlRules.setter
    def accessControlRules(self, value: list[AccessControlRule] | None):
        self.__accessControlRules = value if value else []

    @property
    def canBeManaged(self) -> bool:
        """whether or not layers can be added to or removed from this
        data store, and whether or not the contents of the layers of
        this data store can be managed;  True iff the data store is of
        type "cubestor" and is part of a Stratos deployment (i.e., if
        the caller manually creates a new DataStore object, it can't
        be managed until stratos.addOrReplaceDataStore() is called)"""
        return (self.type == "cubestor" and
                self.__dataStoreAdminUrl and
                self.__ogcApiLandingPageUrl and
                self.__authorizationToken)

    def getLayers(self, forceRefetch: bool = False) -> list[Layer]:
        """Return the list of layers that this data store provides.

        Returns the list of layers (feature sets) that this data store
        provides.

        ARGUMENTS:
            forceRefetch - if True, the list of layers is (re-)fetched from
                the server even if a cached copy exists
        RETURNS:
            the list of layers that this data store provides
        """
        # If we're not associated with a Stratos deployment yet, simply
        # return an empty list.
        if not self.__ogcApiLandingPageUrl or not self.__authorizationToken:
            return []

        # Return cached results if available.
        if not forceRefetch and self.__layerCache is not None:
            return self.__layerCache

        # Fetch the {ogcApiLandingPage}/collections document.
        collectionsUrl = self.__ogcApiLandingPageUrl + "/collections"
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken
        }
        params = { "limit": "unlimited" }
        response = requests.get(collectionsUrl, headers=requestHeaders,
            params=params)
        ServerException.raise_for_status(response)
        responseJson = response.json()

        # Parse the collections into Layer objects.
        layers = []
        collectionsJson = responseJson.get("collections")
        if isinstance(collectionsJson, list):
            for collectionJson in collectionsJson:
                layer = Layer(collectionJson, self, collectionsUrl,
                    self.__authorizationToken)
                if layer: layers.append(layer)

        # Cache the results.
        self.__layerCache = layers

        return layers

    def addVectorLayer(self, id: str, dataFilePath: str,
                       title: str = None, description: str = None,
                       loadData: bool = True) -> Layer:
        """Add a vector layer to this data store.

        Adds a vector layer to this data store.  This can only
        be done for data stores whose canBeManaged property is True.
        The layer is immediately added to the Stratos deployment; there's
        no need to call stratos.updateDataStore() to commit the addition.

        ARGUMENTS:
            id - the ID/name to give the layer; the data store must not
                already have a layer with this ID
            dataFilePath - the fully-qualified local file path to a vector
                data file from which to derive the schema
            title - a title to give the layer, or None
            description - a brief textual description to give the layer,
                or None
            loadData - whether or not to actually load the vector data
                from the specified data file into the layer
        RETURNS:
            the new CoverageLayer
        """
        if self.type != "cubestor":
            raise CwException("layer manipulation can only be performed on "
                              "data stores of type \"cubestor\"")
        if not self.__dataStoreAdminUrl or not self.__authorizationToken:
            raise CwException("this data store is not yet part of a "
                              "Stratos deployment")
        # TODO: implement
        # TODO: add to self.__layerCache?

    def addCoverageLayer(self, id: str, title: str = None,
                         description: str = None) -> Layer:
        """Add a coverage layer to this data store.

        Adds a coverage layer to this data store.  This can only
        be done for data stores whose canBeManaged property is True.
        The layer is immediately added to the Stratos deployment; there's
        no need to call stratos.updateDataStore() to commit the addition.

        ARGUMENTS:
            id - the ID/name to give the layer; the data store must not
                already have a layer with this ID
            title - a title to give the layer, or None
            description - a brief textual description to give the layer,
                or None
        RETURNS:
            the new CoverageLayer
        """
        if self.type != "cubestor":
            raise CwException("layer manipulation can only be performed on "
                              "data stores of type \"cubestor\"")
        if not self.__ogcApiLandingPageUrl or not self.__authorizationToken:
            raise CwException("this data store is not yet part of a "
                              "Stratos deployment")

        # Make the HTTP PUT request to create the collection.
        collectionsUrl = self.__ogcApiLandingPageUrl + "/collections"
        collectionUrl = collectionsUrl + "/" + quote(id)
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken
        }
        jsonBody = {}
        if title: jsonBody["title"] = title
        if description: jsonBody["description"] = description
        response = requests.put(collectionUrl, headers=requestHeaders,
            json=jsonBody)
        ServerException.raise_for_status(response)

        # Fetch the definition of the new collection.
        response = requests.get(collectionUrl, headers=requestHeaders)
        ServerException.raise_for_status(response)

        # Parse the definition of the new collection into a Layer object,
        # and update the layer cache.
        newLayer = Layer(response.json(), self, collectionsUrl,
            self.__authorizationToken)
        if (self.__layerCache is not None):
            self.__layerCache.append(newLayer)

        # We're done!
        return newLayer

    def removeLayer(self, layer: Layer | str) -> bool:
        """Remove a layer from this data store.

        Removes a layer from this data store.  This can only be done
        for data stores whose canBeManaged property is True.  The layer
        is immediately removed from the Stratos deployment; there's no
        need to call stratos.updateDataStore() to commit the removal.

        WARNING: This will remove all data associated with the layer!!!
        This could be catastrophic if done unintentionally, so be careful!

        ARGUMENTS:
            layer - a layer definition or ID/name
        RETURNS:
            True if the layer was removed, or False if the layer didn't
            exist
        """
        if self.type != "cubestor":
            raise CwException("layer manipulation can only be performed on "
                              "data stores of type \"cubestor\"")
        if not self.__dataStoreAdminUrl or not self.__authorizationToken:
            return False

        # Determine the ID of the layer to remove.
        id = layer.id if isinstance(layer, Layer) else layer

        # Make the HTTP DELETE request to delete the collection.
        collectionsUrl = self.__ogcApiLandingPageUrl + "/collections"
        collectionUrl = collectionsUrl + "/" + quote(id)
        requestHeaders = {
            "Accept": "application/json",
            "Authorization": "CwAuth " + self.__authorizationToken
        }
        response = requests.delete(collectionUrl, headers=requestHeaders)
        if response.status_code == 404: return False
        ServerException.raise_for_status(response)

        # Remove this layer from the layer cache.
        if (self.__layerCache is not None):
            for i in range(len(self.__layerCache)):
                if self.__layerCache[i].id == id:
                    del self.__layerCache[i]
                    break

        # We're done!
        return True

    def _setServerAssociation(self, dataStoreAdminUrl: str,
            ogcApiLandingPageUrl: str, authorizationToken: str):
        self.__dataStoreAdminUrl = dataStoreAdminUrl
        self.__ogcApiLandingPageUrl = ogcApiLandingPageUrl
        self.__authorizationToken = authorizationToken
        self.__layerCache = None

    @property
    def _jsonRep(self) -> dict:
        jsonRep = {}
        jsonRep["type"] = self.__type
        jsonRep["source"] = self.__source
        if self.__title:
            jsonRep["title"] = self.__title._jsonRep
        if self.__description:
            jsonRep["description"] = self.__description._jsonRep
        if self.__attributionTitle:
            jsonRep["attributionTitle"] = self.__attributionTitle._jsonRep
        if self.__attributionUrl:
            jsonRep["attributionUrl"] = self.__attributionUrl
        if self.__attributionHtml:
            jsonRep["attributionHtml"] = self.__attributionHtml._jsonRep
        if self.__attributionLogoUrl:
            jsonRep["attributionLogoUrl"] = self.__attributionLogoUrl
        if self.__licenseTitle:
            jsonRep["licenseTitle"] = self.__licenseTitle._jsonRep
        if self.__licenseUrl:
            jsonRep["licenseUrl"] = self.__licenseUrl
        if self.__licenseHtml:
            jsonRep["licenseHtml"] = self.__licenseHtml._jsonRep
        if self.__isExternalService:
            jsonRep["isExternalService"] = self.__isExternalService
        if self.__omitDataStoreTheme:
            jsonRep["omitDataStoreTheme"] = self.__omitDataStoreTheme
        if self.__stylesUrl:
            jsonRep["stylesUrl"] = self.__stylesUrl
        if self.__extraStylesUrl:
            jsonRep["extraStylesUrl"] = self.__extraStylesUrl
        if self.__provideSpectralIndexStyles:
            jsonRep["provideSpectralIndexStyles"] = \
                self.__provideSpectralIndexStyles
        if self.__simulateTiles:
            jsonRep["simulateTiles"] = self.__simulateTiles
        if self.__hints:
            jsonRep["hints"] = self.__hints

        jsonRep["accessControlRules"] = acrs = []
        for acr in self.__accessControlRules:
            acrs.append(acr._jsonRep)

        return jsonRep

    @property
    def _patchDict(self) -> dict:
        patch = {}

        if repr(self.__type) != self.__typeOrigRep:
            patch["type"] = self.__type
        if repr(self.__source) != self.__sourceOrigRep:
            patch["source"] = self.__source
        if repr(self.__title) != self.__titleOrigRep:
            patch["title"] = self.__title._jsonRep
        if repr(self.__description) != self.__descriptionOrigRep:
            patch["description"] = self.__description._jsonRep
        if repr(self.__attributionTitle) != self.__attributionTitleOrigRep:
            patch["attributionTitle"] = self.__attributionTitle._jsonRep
        if repr(self.__attributionUrl) != self.__attributionUrlOrigRep:
            patch["attributionUrl"] = self.__attributionUrl
        if repr(self.__attributionHtml) != self.__attributionHtmlOrigRep:
            patch["attributionHtml"] = self.__attributionHtml._jsonRep
        if repr(self.__attributionLogoUrl) != self.__attributionLogoUrlOrigRep:
            patch["attributionLogoUrl"] = self.__attributionLogoUrl
        if repr(self.__licenseTitle) != self.__licenseTitleOrigRep:
            patch["licenseTitle"] = self.__licenseTitle._jsonRep
        if repr(self.__licenseUrl) != self.__licenseUrlOrigRep:
            patch["licenseUrl"] = self.__licenseUrl
        if repr(self.__licenseHtml) != self.__licenseHtmlOrigRep:
            patch["licenseHtml"] = self.__licenseHtml._jsonRep
        if repr(self.__isExternalService) != self.__isExternalServiceOrigRep:
            patch["isExternalService"] = self.__isExternalService
        if repr(self.__omitDataStoreTheme) != self.__omitDataStoreThemeOrigRep:
            patch["omitDataStoreTheme"] = self.__omitDataStoreTheme
        if repr(self.__stylesUrl) != self.__stylesUrlOrigRep:
            patch["stylesUrl"] = self.__stylesUrl
        if repr(self.__extraStylesUrl) != self.__extraStylesUrlOrigRep:
            patch["extraStylesUrl"] = self.__extraStylesUrl
        if repr(self.__provideSpectralIndexStyles) != \
                self.__provideSpectralIndexStylesOrigRep:
            patch["provideSpectralIndexStyles"] = \
                self.__provideSpectralIndexStyles
        if repr(self.__simulateTiles) != self.__simulateTilesOrigRep:
            patch["simulateTiles"] = self.__simulateTiles
        if repr(self.__hints) != self.__hintsOrigRep:
            patch["hints"] = self.__hints
        if repr(self.__accessControlRules) != self.__accessControlRulesOrigRep:
            patch["accessControlRules"] = acrs = []
            for rule in self.__accessControlRules:
                acrs.append(rule._jsonRep)

        return patch

