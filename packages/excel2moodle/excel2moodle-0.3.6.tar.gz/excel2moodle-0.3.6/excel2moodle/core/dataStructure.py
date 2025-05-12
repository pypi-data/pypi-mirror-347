"""Main Module which does the heavy lifting.

At the heart is the class ``xmlTest``
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import lxml.etree as ET  # noqa: N812
import pandas as pd
from PySide6 import QtWidgets

from excel2moodle.core import stringHelpers
from excel2moodle.core.category import Category
from excel2moodle.core.exceptions import InvalidFieldException, QNotParsedException
from excel2moodle.core.question import Question
from excel2moodle.core.questionValidator import Validator
from excel2moodle.logger import QSignaler
from excel2moodle.ui.dialogs import QuestionVariantDialog
from excel2moodle.ui.settings import Settings, SettingsKey
from excel2moodle.ui.treewidget import QuestionItem

if TYPE_CHECKING:
    from PySide6.QtWidgets import QMainWindow

logger = logging.getLogger(__name__)


class QuestionDB:
    """oberste Klasse für den Test."""

    dataChanged = QSignaler()

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.window: QMainWindow | None = None
        self.version = None
        self.categoriesMetaData = pd.DataFrame()
        self.categories: dict[str, Category] = {}

    def readSpreadsheetData(self, sheet: Path) -> None:
        """Read the metadata and questions from the spreadsheet.

        This method gathers this information and stores it in the
        ``categoriesMetaData`` dataframe
        It also reads the question data and stores it in ``self.categories = {}``
        """
        logger.info("Start Parsing the Excel Metadata Sheet\n")
        with Path(sheet).open("rb") as f:
            excelFile = pd.ExcelFile(f)
            self.categoriesMetaData = pd.read_excel(
                f,
                sheet_name="Kategorien",
                usecols=["Kategorie", "Beschreibung", "Punkte", "Version"],
                index_col=0,
            )
            logger.info("Sucessfully read categoriesMetaData")
            self.categories = {}
            for sh in excelFile.sheet_names:
                if sh.startswith("KAT"):
                    n = int(sh[4:])
                    katDf = pd.read_excel(
                        f,
                        sheet_name=str(sh),
                        index_col=0,
                        header=None,
                    )
                    if not katDf.empty:
                        p = self.categoriesMetaData["Punkte"].iloc[n - 1]
                        points = p if not pd.isna(p) else 1
                        v = self.categoriesMetaData["Version"].iloc[n - 1]
                        version = v if not pd.isna(v) else 0
                        self.categories[sh] = Category(
                            n,
                            sh,
                            self.categoriesMetaData["Beschreibung"].iloc[n - 1],
                            dataframe=katDf,
                            points=points,
                            version=version,
                        )
        # self.dataChanged.signal.emit("whoo")

    def parseAll(self) -> None:
        self.mainTree = ET.Element("quiz")
        for c in self.categories.values():
            validator = Validator(c)
            for q in c.dataframe.columns:
                logger.debug(f"Starting to check Validity of {q}")
                qdat = c.dataframe[q]
                if isinstance(qdat, pd.Series):
                    validator.setup(qdat, q)
                    check = False
                    try:
                        check = validator.validate()
                    except InvalidFieldException as e:
                        logger.exception(
                            f"Question {c.id}{q:02d} is invalid.",
                            exc_info=e,
                        )
                    if check:
                        c.questions[q] = validator.question
                        try:
                            c.parseQ(c.questions[q], validator.qdata)
                        except QNotParsedException as e:
                            logger.exception(
                                f"Frage {
                                    c.questions[q].id
                                } konnte nicht erstellt werden",
                                exc_info=e,
                            )

    def appendQuestions(
        self, questions: list[QuestionItem], file: Path | None = None
    ) -> None:
        """Append selected question Elements to the tree."""
        tree = ET.Element("quiz")
        catdict: dict[Category, list[Question]] = {}
        for q in questions:
            logger.debug(f"got a question to append {q=}")
            cat = q.parent().getCategory()
            if cat not in catdict:
                catdict[cat] = []
            catdict[cat].append(q.getQuestion())
        for cat, qlist in catdict.items():
            self.appendQElements(
                cat,
                qlist,
                tree=tree,
                includeHeader=self.settings.get(SettingsKey.INCLUDEINCATS),
            )
        stringHelpers.printDom(tree, file=file)

    def appendQElements(
        self,
        cat: Category,
        qList: list[Question],
        tree: ET.Element,
        includeHeader: bool = True,
    ) -> None:
        if includeHeader:
            tree.append(cat.getCategoryHeader())
            logger.debug(f"Appended a new category item {cat=}")
        variant: int = self.settings.get(SettingsKey.QUESTIONVARIANT)
        for q in qList:
            if cat.parseQ(q):
                if q.variants is not None:
                    if variant == 0 or variant > q.variants:
                        dialog = QuestionVariantDialog(self.window, q)
                        if dialog.exec() == QtWidgets.QDialog.Accepted:
                            variant = dialog.variant
                            logger.debug(f"Die Fragen-Variante {variant} wurde gewählt")
                            q.assemble(variant)
                        else:
                            pass
                else:
                    q.assemble()
                tree.append(q.element)
            else:
                logger.warning(f"Frage {q} wurde nicht erstellt")
