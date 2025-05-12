"""Settings module provides the adjusted subclass of ``PySide6.QtCore.QSettings``."""

import logging
from enum import StrEnum
from pathlib import Path
from typing import Literal, overload

from PySide6.QtCore import QSettings, QTimer, Signal

logger = logging.getLogger(__name__)


class SettingsKey(StrEnum):
    def __new__(
        cls,
        key: str,
        typ: type,
        default: str | float | Path | bool | None,
    ):
        """Define new settings class."""
        obj = str.__new__(cls, key)
        obj._value_ = key
        obj._default_ = default
        obj._typ_ = typ
        return obj

    @property
    def default(self) -> str | int | float | Path | bool | None:
        """Get default value for the key."""
        return self._default_

    def typ(self) -> type:
        """Get default value for the key."""
        return self._typ_

    QUESTIONVARIANT = "testgen/defaultQuestionVariant", int, 0
    INCLUDEINCATS = "testgen/includeCats", bool, False
    PARSERNF_TOLERANCE = "parser/nf/tolerance", int, 1
    PICTURESUBFOLDER = "core/pictureSubFolder", str, "Abbildungen"
    PICTUREFOLDER = "core/pictureFolder", Path, None
    SPREADSHEETFOLDER = "core/spreadsheetFolder", Path, None
    LOGLEVEL = "core/loglevel", str, "INFO"
    LOGFILE = "core/logfile", str, "excel2moodleLogFile.log"


class Settings(QSettings):
    """Settings for Excel2moodle."""

    shPathChanged = Signal(Path)

    def __init__(self) -> None:
        """Instantiate the settings."""
        super().__init__("jbosse3", "excel2moodle")
        if self.contains(SettingsKey.SPREADSHEETFOLDER):
            self.sheet = self.get(SettingsKey.SPREADSHEETFOLDER)
            if self.sheet.is_file():
                QTimer.singleShot(0, self._emitSpreadsheetChanged)

    def _emitSpreadsheetChanged(self) -> None:
        self.shPathChanged.emit(self.sheet)

    @overload
    def get(
        self,
        value: Literal[SettingsKey.QUESTIONVARIANT, SettingsKey.PARSERNF_TOLERANCE],
    ) -> int: ...
    @overload
    def get(self, value: Literal[SettingsKey.INCLUDEINCATS]) -> bool: ...
    @overload
    def get(
        self,
        value: Literal[
            SettingsKey.PICTURESUBFOLDER, SettingsKey.LOGLEVEL, SettingsKey.LOGFILE
        ],
    ) -> str: ...
    @overload
    def get(
        self,
        value: Literal[SettingsKey.PICTUREFOLDER, SettingsKey.SPREADSHEETFOLDER],
    ) -> Path: ...

    def get(self, value: SettingsKey):
        """Get the typesafe settings value."""
        logger.debug("entering get method. searched typ: %s", value.typ())
        if value.typ() is Path:
            logger.debug("trying to acess a path object from settings")
            path = self.value(value, defaultValue=value.default)
            try:
                path.resolve(strict=True)
            except ValueError:
                logger.warning(
                    f"The settingsvalue {value} couldn't be fetched with correct typ",
                )
                return value.default
            return path
        raw = self.value(value, defaultValue=value.default, type=value.typ())
        logger.debug("read a settings Value: %s of type: %s", value, value.typ())
        try:
            return value.typ()(raw)
        except (ValueError, TypeError):
            logger.warning(
                f"The settingsvalue {value} couldn't be fetched with correct typ",
            )
            return value.default

    def set(self, settingKey: SettingsKey, value: float | bool | Path | str) -> None:
        """Set the setting to value."""
        # if isinstance(value, SettingsKey.type):
        self.setValue(settingKey, value)
        logger.info("Saved the Setting %s = %s", settingKey, value)
        # else:
        #     logger.error("trying to save setting with wrong type not possible")

    def setSpreadsheet(self, sheet: Path) -> None:
        """Save spreadsheet path and emit the changed event."""
        if isinstance(sheet, Path):
            self.sheet = sheet.resolve(strict=True)
            logpath = str(self.sheet.parent / "excel2moodleLogFile.log")
            self.set(SettingsKey.LOGFILE, logpath)
            self.set(SettingsKey.SPREADSHEETFOLDER, self.sheet)
            self.shPathChanged.emit(sheet)
            return
