"""This Module holds small Helperfunctions related to string manipulation."""

import base64
from pathlib import Path

import lxml.etree as ET


def stripWhitespace(stringList):
    stripped = []
    for i in stringList:
        s = i.strip()
        if s:
            stripped.append(s)
    return stripped


def stringToFloat(string: str) -> float:
    string.replace(",", ".")
    return float(string)


def get_bullet_string(s):
    """Formatiert die Angaben zum Statischen System hübsch."""
    split = s.split(";")
    s_spl = stripWhitespace(split)
    name = []
    var = []
    quant = []
    unit = []
    for sc in s_spl:
        sc_split = sc.split()
        name.append(sc_split[0])
        var.append(sc_split[1])
        quant.append(sc_split[3])
        unit.append(sc_split[4])
    bulletString = ['</p><ul dir="ltr">']
    for i in range(len(s_spl)):
        num = quant[i].split(",")
        num_s = f"{num[0]!s},\\!{num[1]!s}~" if len(num) == 2 else f"{num[0]!s},\\!0~"
        bulletString.append('<li style="text-align: left;">')
        bulletString.append(
            f"{name[i]}: \\( {var[i]} = {num_s} \\mathrm{{ {unit[i]}  }}\\) </li>\n",
        )
    bulletString.append("<br></ul>")
    return "\n".join(bulletString)


def getBase64Img(imgPath):
    with open(imgPath, "rb") as img:
        return base64.b64encode(img.read()).decode("utf-8")


def getUnitsElementAsString(unit) -> None:
    def __getUnitEle__(name, multipl):
        unit = ET.Element("unit")
        ET.SubElement(unit, "multiplier").text = multipl
        ET.SubElement(unit, "unit_name").text = name
        return unit

    ET.Element("units")


def printDom(xmlElement: ET.Element, file: Path | None = None) -> None:
    """Prints the document tree of ``xmlTree`` to the ``file``, if specified, else dumps to stdout."""
    documentTree = ET.ElementTree(xmlElement)
    if file is not None:
        if file.parent.exists():
            documentTree.write(
                file,
                xml_declaration=True,
                encoding="utf-8",
                pretty_print=True,
            )
    else:
        pass


def texWrapper(text: str | list[str], style: str) -> list[str]:
    r"""Puts the strings inside ``text`` into a LaTex environment.

    if ``style == unit``: inside ``\\mathrm{}``
    if ``style == math``: inside ``\\( \\)``
    """
    answers: list[str] = []
    begin = ""
    end = ""
    if style == "math":
        begin = "\\("
        end = "\\)"
    elif style == "unit":
        begin = "\\(\\mathrm{"
        end = "}\\)"
    if isinstance(text, str):
        li = [begin]
        li.append(text)
        li.append(end)
        answers.append("".join(li))
    elif isinstance(text, list):
        for i in text:
            li = [begin]
            li.append(i)
            li.append(end)
            answers.append("".join(li))
    return answers
