import uiautomation as auto

from uiautomation import Control
from uiax.utils import XPathLexer, XPathParser, XPathFinder


class Uiax:
    def __init__(self, control=None):
        self.root = control if control else auto.GetRootControl()

    def xpath(self, xpath_expr):
        lexer = XPathLexer(xpath_expr)
        tokens = lexer.tokenize()
        parser = XPathParser(tokens)
        steps = parser.parse()
        finder = XPathFinder(self.root)
        return finder.find(steps)

    def find(self, xpath_expr):
        elements = self.find_all(xpath_expr)
        assert elements, "未找到元素"
        assert len(elements) == 1, "找到了多个元素"
        return elements[0]

    def find_all(self, xpath_expr) -> list[Control]:
        lexer = XPathLexer(xpath_expr)
        tokens = lexer.tokenize()
        parser = XPathParser(tokens)
        steps = parser.parse()
        finder = XPathFinder(self.root)
        return finder.find_all(steps)


if __name__ == "__main__":
    # 示例用法
    uiax = Uiax()
    elements = uiax.xpath('//Control[@Name="文件"]')
    for elem in elements:
        print(f"Found element: {elem.Name}, ControlType: {elem.ControlTypeName}")
