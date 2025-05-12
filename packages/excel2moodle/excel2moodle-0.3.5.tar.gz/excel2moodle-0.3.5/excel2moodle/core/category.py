import logging

import lxml.etree as ET
import pandas as pd

from excel2moodle.core.parser import (
    MCQuestionParser,
    NFMQuestionParser,
    NFQuestionParser,
    QNotParsedException,
)
from excel2moodle.core.question import Question
from excel2moodle.logger import LogAdapterQuestionID

loggerObj = logging.getLogger(__name__)


class Category:
    def __init__(
        self,
        n: int,
        name: str,
        description: str,
        dataframe: pd.DataFrame,
        points: float = 0,
        version: int = 0,
    ) -> None:
        self.n = n
        self.NAME = name
        self.desc = str(description)
        self.dataframe: pd.DataFrame = dataframe
        self.points = points
        self.version = int(version)
        self.questions: dict[int, Question] = {}
        self.maxVariants: int | None = None
        loggerObj.info("initializing Category %s", self.NAME)

    @property
    def name(self) -> str:
        return self.NAME

    @property
    def id(self) -> str:
        return f"{self.version}{self.n:02d}"

    def __hash__(self) -> int:
        return hash(self.NAME)

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, Category):
            return self.NAME == other.NAME
        return False

    def parseQ(
        self,
        q: Question,
        questionData: dict | None = None,
        xmlTree: ET._Element | None = None,
    ) -> bool:
        """Parse the given question."""
        logger = LogAdapterQuestionID(loggerObj, {"qID": q.id})
        if q.element is not None:
            logger.info("Question already parsed")
            return True
        if q.qtype == "NF":
            parser = NFQuestionParser(q, questionData)
            logger.debug("setup a new NF parser ")
        elif q.qtype == "MC":
            parser = MCQuestionParser(q, questionData)
            logger.debug("setup a new MC parser ")
        elif q.qtype == "NFM":
            parser = NFMQuestionParser(q, questionData)
            logger.debug("setup a new NFM parser ")
        else:
            logger.error("couldn't setup Parser")
            return False
        try:
            parser.parse(xmlTree=xmlTree)
            return True
        except QNotParsedException as e:
            logger.critical(
                "Question couldn't be parsed",
                exc_info=e,
                stack_info=True,
            )
            return False
        finally:
            del parser

    def getCategoryHeader(self) -> ET.Element:
        """Insert an <question type='category'> before all Questions of this Category."""
        header = ET.Element("question", type="category")
        cat = ET.SubElement(header, "category")
        info = ET.SubElement(header, "info", format="html")
        ET.SubElement(cat, "text").text = f"$module$/top/{self.NAME}"
        ET.SubElement(info, "text").text = str(self.desc)
        ET.SubElement(header, "idnumber").text = str(self.n)
        ET.indent(header)
        return header
