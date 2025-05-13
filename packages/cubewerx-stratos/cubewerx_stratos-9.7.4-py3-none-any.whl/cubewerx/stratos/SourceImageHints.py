# $Id: SourceImageHints.py 79030 2025-05-01 20:10:29Z pomakis $

import datetime


class SourceImageHints:
    """Hints to help the CubeWerx Stratos server interpret a source image.

       To specify hints when adding source images to a layer, create a new
       SourceImageHints object, set the relevant properties, and pass this
       object to layer.addSourceImages()

       To specify or adjust hints of an existing source image, get the
       SourceImageHints object using sourceImage.getHints(), set or adjust
       the relevant properties, and commit the changes by calling
       sourceImage.commitHintUpdates().  Note that this may change the
       values of some of the properties of the source image, including
       its ID and whether or not it's considered a good source image.

    ARGUMENTS:
        dictionary - a dictionary supplying properties; do not specify;
            for internal use only
    """

    def __init__(self, dictionary: dict={}):
        self._dict = dictionary

        # Keep track of the properties that are programmatically changed
        # so that an appropriate patch dictionary can be constructed.
        self.__dataCoordSysChanged = False
        self.__dataCitationChanged = False
        self.__dataTimeChanged = False
        self.__nullColor1Changed = False
        self.__nullColor2Changed = False
        self.__nullFuzzChanged = False
        self.__rasterNBitsChanged = False

    @property
    def _changed(self) -> bool:
        return (self.__dataCoordSysChanged or
            self.__dataCitationChanged or
            self.__dataTimeChanged or
            self.__nullColor1Changed or
            self.__nullColor2Changed or
            self.__nullFuzzChanged or
            self.__rasterNBitsChanged)

    @property
    def dataCoordSys(self) -> str | None:
        """the coordinate system that the data is in"""
        return self._dict.get("dataCoordSys")

    @dataCoordSys.setter
    def dataCoordSys(self, value: str | None):
        if value:
            self._dict["dataCoordSys"] = str(value)
        else:
            del self._dict["dataCoordSys"]
        self.__dataCoordSysChanged = True

    @property
    def dataCitation(self) -> str | None:
        """a citation for the source of the data"""
        return self._dict.get("dataCitation")

    @dataCitation.setter
    def dataCitation(self, value: str | None):
        if value:
            self._dict["dataCitation"] = str(value)
        else:
            del self._dict["dataCitation"]
        self.__dataCitationChanged = True

    @property
    def dataTime(self) -> datetime.datetime | None:
        """the date (and possibly time), expressed in ISO8601 format,
        that this data was captured"""
        dataTimeStr = self._dict.get("dataTime")
        return datetime.date.fromisoformat(dataTimeStr) \
            if dataTimeStr else None

    @dataTime.setter
    def dataTime(self, value: datetime.datetime | None):
        if value:
            self._dict["dataTime"] = value.isoformat()
        else:
            del self._dict["dataTime"]
        self.__dataTimeChanged = True

    @property
    def nullColor1(self) -> datetime.datetime | None:
        """the color in the source images that represents the NULL color,
        expressed as a hexadecimal red-green-blue color value"""
        return self._dict.get("nullColor1")

    @nullColor1.setter
    def nullColor1(self, value: str | None):
        if value:
            self._dict["nullColor1"] = str(value)
        else:
            del self._dict["nullColor1"]
        self.__nullColor1Changed = True

    @property
    def nullColor2(self) -> datetime.datetime | None:
        """a second color in the source images that represents the NULL
        color, expressed as a hexadecimal red-green-blue color value"""
        return self._dict.get("nullColor2")

    @nullColor2.setter
    def nullColor2(self, value: str | None):
        if value:
            self._dict["nullColor2"] = str(value)
        else:
            del self._dict["nullColor2"]
        self.__nullColor2Changed = True

    @property
    def nullFuzz(self) -> int | None:
        """a fuzz factor to apply when detecting NULL colors (useful for
        processing lossy data); typically in the range of 0-255 for RGB
        or greyscale data"""
        return self._dict.get("nullFuzz")

    @nullFuzz.setter
    def nullFuzz(self, value: int | None):
        if value is not None and int(value) > 0:
            self._dict["nullFuzz"] = int(value)
        else:
            del self._dict["nullFuzz"]
        self.__nullFuzzChanged = True

    @property
    def rasterNBits(self) -> int | None:
        """the number of significant bits per channel in the source data"""
        return self._dict.get("rasterNBits")

    @rasterNBits.setter
    def rasterNBits(self, value: int | None):
        if value is not None and int(value) > 0:
            self._dict["rasterNBits"] = int(value)
        else:
            del self._dict["rasterNBits"]
        self.__rasterNBitsChanged = True

    @property
    def _patchDict(self) -> dict:
        patch = {}
        if self.__dataCoordSysChanged:
            patch["dataCoordSys"] = self.dataCoordSys
        if self.__dataCitationChanged:
            patch["dataCitation"] = self.dataCitation
        if self.__dataTimeChanged:
            patch["dataTime"] = self.dataTime
        if self.__nullColor1Changed:
            patch["nullColor1"] = self.nullColor1
        if self.__nullColor2Changed:
            patch["nullColor2"] = self.nullColor2
        if self.__nullFuzzChanged:
            patch["nullFuzz"] = self.nullFuzz
        if self.__rasterNBitsChanged:
            patch["rasterNBits"] = self.rasterNBits
        return patch
