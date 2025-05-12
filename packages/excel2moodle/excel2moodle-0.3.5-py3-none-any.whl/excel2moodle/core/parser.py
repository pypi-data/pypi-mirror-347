import logging
import re

import lxml.etree as ET
import pandas as pd
from asteval import Interpreter

import excel2moodle.core.etHelpers as eth
from excel2moodle.core import stringHelpers
from excel2moodle.core.exceptions import QNotParsedException
from excel2moodle.core.globals import (
    DFIndex,
    TextElements,
    XMLTags,
    feedbackStr,
    feedBElements,
    parserSettings,
)
from excel2moodle.core.question import Picture, Question
from excel2moodle.logger import LogAdapterQuestionID
from excel2moodle.ui.settings import Settings, SettingsKey

loggerObj = logging.getLogger(__name__)

settings = Settings()


class QuestionParser:
    """Setup the Parser Object.

    This is the superclass which implements the general Behaviour of he Parser.
    Important to implement the answers methods.
    """

    def __init__(self, question: Question, data: dict) -> None:
        """Initialize the general Question parser."""
        self.question: Question = question
        self.rawInput = data
        self.logger = LogAdapterQuestionID(loggerObj, {"qID": self.question.id})
        self.logger.debug(
            "The following Data was provided: %s",
            self.rawInput,
        )
        self.genFeedbacks: list[XMLTags] = []

    def hasPicture(self) -> bool:
        """Create a ``Picture`` object ``question``if the question needs a pic."""
        if hasattr(self, "picture") and self.question.picture.ready:
            return True
        picKey = self.rawInput[DFIndex.PICTURE]
        svgFolder = settings.get(SettingsKey.PICTUREFOLDER)
        if picKey != 0 and pd.notna(picKey):
            if not hasattr(self.question, "picture"):
                self.question.picture = Picture(picKey, svgFolder, self.question)
            if self.question.picture.ready:
                return True
        return False

    def setMainText(self) -> None:
        paragraphs: list[ET._Element] = [TextElements.PLEFT.create()]
        ET.SubElement(paragraphs[0], "b").text = f"ID {self.question.id}"
        text = self.rawInput[DFIndex.TEXT]
        pcount = 0
        for t in text:
            if not pd.isna(t):
                pcount += 1
                paragraphs.append(TextElements.PLEFT.create())
                paragraphs[-1].text = t
        self.question.qtextParagraphs = paragraphs
        self.logger.debug("Created main Text with: %s paragraphs", pcount)

    def setBPoints(self) -> None:
        """If there bulletPoints are set in the Spreadsheet it creates an unordered List-Element in ``Question.bulletList``."""
        if DFIndex.BPOINTS in self.rawInput:
            bps: str = self.rawInput[DFIndex.BPOINTS]
            try:
                bulletList = self.formatBulletList(bps)
            except IndexError as e:
                msg = f"konnt Bullet Liste {self.question.id} nicht generieren"
                raise QNotParsedException(
                    msg,
                    self.question.id,
                    exc_info=e,
                )
            self.logger.debug(
                "Generated BPoint List: \n %s",
                ET.tostring(bulletList, encoding="unicode"),
            )
            self.question.bulletList = bulletList

    def formatBulletList(self, bps: str) -> ET.Element:
        self.logger.debug("Formatting the bulletpoint list")
        li: list[str] = stringHelpers.stripWhitespace(bps.split(";"))
        name = []
        var = []
        quant = []
        unit = []
        unorderedList = TextElements.ULIST.create()
        for item in li:
            sc_split = item.split()
            name.append(sc_split[0])
            var.append(sc_split[1])
            quant.append(sc_split[3])
            unit.append(sc_split[4])
        for i in range(len(name)):
            if re.fullmatch(r"{\w+}", quant[i]):
                self.logger.debug("Got an variable bulletItem")
                num_s = quant[i]
            else:
                self.logger.debug("Got a normal bulletItem")
                num = quant[i].split(",")
                if len(num) == 2:
                    num_s = f"{num[0]!s},\\!{num[1]!s}~"
                else:
                    num_s = f"{num[0]!s},\\!0~"
            bullet = TextElements.LISTITEM.create()
            bullet.text = (
                f"{name[i]}: \\( {var[i]} = {num_s} \\mathrm{{ {unit[i]}  }}\\)\n"
            )
            unorderedList.append(bullet)
        return unorderedList

    def appendToTmpEle(
        self,
        eleName: str,
        text: str | DFIndex,
        txtEle=False,
        **attribs,
    ) -> None:
        """Append ``text`` to the temporary Element.

        It uses the data from ``self.rawInput`` if ``text`` is type``DFIndex``
        Otherwise the value of ``text`` will be inserted.
        """
        t = self.rawInput[text] if isinstance(text, DFIndex) else text
        if txtEle is False:
            self.tmpEle.append(eth.getElement(eleName, t, **attribs))
        elif txtEle is True:
            self.tmpEle.append(eth.getTextElement(eleName, t, **attribs))

    def appendFromSettings(self, key="standards") -> None:
        """Appends 1 to 1 mapped Elements defined in the parserSettings to the element."""
        parser = ["Parser"]
        if isinstance(self, MCQuestionParser):
            parser.append("MCParser")
        elif isinstance(self, NFQuestionParser):
            parser.append("NFParser")
        for p in parser:
            try:
                for k, v in parserSettings[p][key].items():
                    self.appendToTmpEle(k, text=v)
            except KeyError as e:
                msg = f"Invalider Input aus den Einstellungen Parser: {
                    type(p) =}"
                self.logger.exception(msg, exc_info=e)
                raise QNotParsedException(msg, self.question.id, exc_info=e)

    def parse(self, xmlTree: ET._Element | None = None) -> None:
        """Parse the Question.

        Generates an new Question Element stored as ``self.tmpEle:ET.Element``
        if no Exceptions are raised, ``self.tmpEle`` is passed to ``self.question.element``
        """
        self.logger.info("Starting to parse")
        self.tmpEle = ET.Element(XMLTags.QUESTION, type=self.question.moodleType)
        # self.tmpEle.set(XMLTags.TYPE, self.question.moodleType)
        self.appendToTmpEle(XMLTags.NAME, text=DFIndex.NAME, txtEle=True)
        self.appendToTmpEle(XMLTags.ID, text=self.question.id)
        if self.hasPicture():
            self.tmpEle.append(self.question.picture.element)
        self.tmpEle.append(ET.Element(XMLTags.QTEXT, format="html"))
        self.appendToTmpEle(XMLTags.POINTS, text=str(self.question.points))
        self.appendToTmpEle(XMLTags.PENALTY, text="0.3333")
        self.appendFromSettings()
        for feedb in self.genFeedbacks:
            self.tmpEle.append(eth.getFeedBEle(feedb))
        if xmlTree is not None:
            xmlTree.append(self.tmpEle)
        ansList = self.setAnswers()
        self.setMainText()
        self.setBPoints()
        if ansList is not None:
            for ele in ansList:
                self.tmpEle.append(ele)
        self.logger.info("Sucessfully parsed")
        self.question.element = self.tmpEle

    def getFeedBEle(
        self,
        feedback: XMLTags,
        text: str | None = None,
        style: TextElements | None = None,
    ) -> ET.Element:
        span = feedBElements[feedback] if style is None else style.create()
        if text is None:
            text = feedbackStr[feedback]
        ele = ET.Element(feedback, format="html")
        par = TextElements.PLEFT.create()
        span.text = text
        par.append(span)
        ele.append(eth.getCdatTxtElement(par))
        return ele

    def setAnswers(self) -> list[ET.Element] | None:
        """Needs to be implemented in the type-specific subclasses."""
        return None

    def getNumericAnsElement(
        self,
        result: float,
        tolerance: float = 0,
        fraction: float = 100,
        format: str = "moodle_auto_format",
    ) -> ET.Element:
        """Get ``<answer/>`` Element specific for the numerical Question.

        The element contains those children:
            ``<text/>`` which holds the value of the answer
            ``<tolerance/>`` with the *relative* tolerance for the result in percent
            ``<feedback/>`` with general feedback for a true answer.
        """
        ansEle: ET.Element = eth.getTextElement(
            XMLTags.ANSWER,
            text=str(result),
            fraction=str(fraction),
            format=format,
        )
        ansEle.append(
            eth.getFeedBEle(
                XMLTags.ANSFEEDBACK,
                feedbackStr["right1Percent"],
                TextElements.SPANGREEN,
            ),
        )
        tolerance = self.getTolerancePercent(tolerance)
        tol = abs(round(result * (tolerance / 100), 3))
        ansEle.append(eth.getElement(XMLTags.TOLERANCE, text=str(tol)))
        return ansEle

    def getTolerancePercent(self, tolerance: float) -> int:
        """Get the correct tolerance.
        If ``tolerance < 1``:  it is interpreted as the fraction.
        If ``tolerance >= 1``: it is interpreted as percentage.
        """
        if tolerance == 0 or pd.isna(tolerance) or tolerance >= 100:
            tolerance = settings.get(SettingsKey.PARSERNF_TOLERANCE)
            self.logger.info(
                "Using default tolerance %s percent from settings",
                tolerance,
            )
        tolerancePercent = 100 * tolerance if tolerance < 1 else tolerance
        self.logger.debug("Using tolerance %s percent", tolerancePercent)
        return int(tolerancePercent)


class NFQuestionParser(QuestionParser):
    """Subclass for parsing numeric questions."""

    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.genFeedbacks = [XMLTags.GENFEEDB]

    def setAnswers(self) -> list[ET.Element]:
        result = self.rawInput[DFIndex.RESULT]
        ansEle: list[ET.Element] = []
        tol = self.rawInput[DFIndex.TOLERANCE]
        ansEle.append(self.getNumericAnsElement(result=result, tolerance=tol))
        return ansEle


class NFMQuestionParser(QuestionParser):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.genFeedbacks = [XMLTags.GENFEEDB]
        self.astEval = Interpreter()

    def setAnswers(self) -> None:
        equation = self.rawInput[DFIndex.RESULT]
        bps = str(self.rawInput[DFIndex.BPOINTS])
        ansElementsList: list[ET.Element] = []
        varNames: list[str] = self._getVarsList(bps)
        self.question.variables, number = self._getVariablesDict(varNames)
        for n in range(number):
            self._setupAstIntprt(self.question.variables, n)
            result = self.astEval(equation)
            if isinstance(result, float):
                tol = self.rawInput[DFIndex.TOLERANCE]
                ansElementsList.append(
                    self.getNumericAnsElement(result=round(result, 3), tolerance=tol),
                )
        self.question.answerVariants = ansElementsList
        self.setVariants(len(ansElementsList))

    def setVariants(self, number: int) -> None:
        self.question.variants = number
        mvar = self.question.category.maxVariants
        if mvar is None:
            self.question.category.maxVariants = number
        else:
            self.question.category.maxVariants = min(number, mvar)

    def _setupAstIntprt(self, var: dict[str, list[float | int]], index: int) -> None:
        """Setup the asteval Interpreter with the variables."""
        for name, value in var.items():
            self.astEval.symtable[name] = value[index]

    def _getVariablesDict(self, keyList: list) -> tuple[dict[str, list[float]], int]:
        """Liest alle Variablen-Listen deren Name in ``keyList`` ist aus dem DataFrame im Column[index]."""
        dic: dict = {}
        num: int = 0
        for k in keyList:
            val = self.rawInput[k]
            if isinstance(val, str):
                li = stringHelpers.stripWhitespace(val.split(";"))
                num = len(li)
                vars: list[float] = [float(i.replace(",", ".")) for i in li]
                dic[str(k)] = vars
            else:
                dic[str(k)] = [str(val)]
                num = 1
        return dic, num

    @staticmethod
    def _getVarsList(bps: str | list[str]) -> list:
        """Durchsucht den bulletPoints String nach den Variablen, die als "{var}" gekennzeichnet sind."""
        vars = []
        if isinstance(bps, list):
            for _p in bps:
                vars.extend(re.findall(r"\{\w\}", str(bps)))
        else:
            vars = re.findall(r"\{\w\}", str(bps))
        variablen = []
        for v in vars:
            variablen.append(v.strip("{}"))
        return variablen


class MCQuestionParser(QuestionParser):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.genFeedbacks = [
            XMLTags.CORFEEDB,
            XMLTags.PCORFEEDB,
            XMLTags.INCORFEEDB,
        ]

    def getAnsElementsList(
        self,
        answerList: list,
        fraction: float = 50,
        format="html",
    ) -> list[ET.Element]:
        elementList: list[ET.Element] = []
        for ans in answerList:
            p = TextElements.PLEFT.create()
            p.text = str(ans)
            text = eth.getCdatTxtElement(p)
            elementList.append(
                ET.Element(XMLTags.ANSWER, fraction=str(fraction), format=format),
            )
            elementList[-1].append(text)
            if fraction < 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["wrong"],
                        style=TextElements.SPANRED,
                    ),
                )
            elif fraction > 0:
                elementList[-1].append(
                    eth.getFeedBEle(
                        XMLTags.ANSFEEDBACK,
                        text=feedbackStr["right"],
                        style=TextElements.SPANGREEN,
                    ),
                )
        return elementList

    def setAnswers(self) -> list[ET.Element]:
        ansStyle = self.rawInput[DFIndex.ANSTYPE]
        true = stringHelpers.stripWhitespace(self.rawInput[DFIndex.TRUE].split(";"))
        trueAnsList = stringHelpers.texWrapper(true, style=ansStyle)
        self.logger.debug(f"got the following true answers \n {trueAnsList=}")
        false = stringHelpers.stripWhitespace(self.rawInput[DFIndex.FALSE].split(";"))
        falseAnsList = stringHelpers.texWrapper(false, style=ansStyle)
        self.logger.debug(f"got the following false answers \n {falseAnsList=}")
        truefrac = 1 / len(trueAnsList) * 100
        falsefrac = 1 / len(trueAnsList) * (-100)
        self.tmpEle.find(XMLTags.PENALTY).text = str(round(truefrac / 100, 4))
        ansList = self.getAnsElementsList(trueAnsList, fraction=round(truefrac, 4))
        ansList.extend(
            self.getAnsElementsList(falseAnsList, fraction=round(falsefrac, 4)),
        )
        return ansList
