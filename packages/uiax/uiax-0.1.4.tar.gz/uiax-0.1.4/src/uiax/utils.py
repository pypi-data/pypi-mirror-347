import re
from uiautomation import Control


class XPathLexer:
    def __init__(self, xpath: str):
        self.xpath = xpath.strip()
        self.tokens = []
        self.pos = 0
        self.length = len(xpath)

    def next_char(self):
        return self.xpath[self.pos] if self.pos < self.length else None

    def advance(self, n=1):
        self.pos += n

    def tokenize(self):
        while self.pos < self.length:
            c = self.next_char()

            if c.isspace():
                self.advance()
                continue

            # 处理 // 和 /
            if self.xpath[self.pos : self.pos + 2] == "//":
                self.tokens.append(("DOUBLE_SLASH", "//"))
                self.advance(2)
                continue
            elif c == "/":
                self.tokens.append(("SLASH", "/"))
                self.advance()
                continue

            # 处理通配符 *
            if c == "*":
                self.tokens.append(("WILDCARD", "*"))
                self.advance()
                continue

            # 处理 [
            if c == "[":
                self.tokens.append(("LBRACKET", "["))
                self.advance()
                continue

            # 处理 ]
            if c == "]":
                self.tokens.append(("RBRACKET", "]"))
                self.advance()
                continue

            # 处理 @开头的属性
            if c == "@":
                self.advance()
                attr = self.consume_identifier()
                self.tokens.append(("ATTR", attr))
                continue

            # 处理 =号
            if c == "=":
                self.tokens.append(("EQUAL", "="))
                self.advance()
                continue

            # 处理字符串
            if c in ('"', "'"):
                string_value = self.consume_string(c)
                self.tokens.append(("STRING", string_value))
                continue

            # 处理函数，比如 contains(
            if c.isalpha():
                ident = self.consume_identifier()
                if self.next_char() == "(":
                    self.tokens.append(("FUNC", ident))
                    self.tokens.append(("LPAREN", "("))
                    self.advance()
                else:
                    self.tokens.append(("NODE", ident))
                continue

            # 处理数字，比如 [1]
            if c.isdigit():
                number = self.consume_number()
                self.tokens.append(("NUMBER", number))
                continue

            # 处理 , 号
            if c == ",":
                self.tokens.append(("COMMA", ","))
                self.advance()
                continue

            # 处理 (
            if c == "(":
                self.tokens.append(("LPAREN", "("))
                self.advance()
                continue

            # 处理 )
            if c == ")":
                self.tokens.append(("RPAREN", ")"))
                self.advance()
                continue

            raise Exception(f"无法识别的字符: {c}")

        return self.tokens

    def consume_identifier(self):
        start = self.pos
        while self.next_char() and (
            self.next_char().isalnum() or self.next_char() in ["_", "-"]
        ):
            self.advance()
        return self.xpath[start : self.pos]

    def consume_string(self, quote_char):
        self.advance()  # skip opening quote
        start = self.pos
        while self.next_char() and self.next_char() != quote_char:
            self.advance()
        if self.next_char() != quote_char:
            raise Exception("字符串未闭合")
        string_content = self.xpath[start : self.pos]
        self.advance()  # skip closing quote
        return string_content

    def consume_number(self):
        start = self.pos
        while self.next_char() and self.next_char().isdigit():
            self.advance()
        return self.xpath[start : self.pos]


class XPathParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.length = len(tokens)

    def next_token(self):
        return self.tokens[self.pos] if self.pos < self.length else None

    def advance(self):
        self.pos += 1

    def parse(self):
        steps = []
        current_traverse = None

        while self.pos < self.length:
            token_type, token_value = self.next_token()

            if token_type in ("SLASH", "DOUBLE_SLASH"):
                current_traverse = (
                    "descendant" if token_type == "DOUBLE_SLASH" else "child"
                )
                self.advance()
                continue

            if token_type in ("NODE", "WILDCARD"):
                step = {
                    "traverse": current_traverse or "child",  # 默认从子节点
                    "node_type": "*" if token_type == "WILDCARD" else token_value,
                    "conditions": [],
                    "index": None,
                }
                self.advance()

                # 处理 [条件]
                while self.next_token() and self.next_token()[0] == "LBRACKET":
                    self.advance()  # skip [

                    # 看下一个token
                    token_type, token_value = self.next_token()

                    if token_type == "ATTR":
                        condition = self.parse_attr_condition()
                        step["conditions"].append(condition)

                    elif token_type == "FUNC":
                        condition = self.parse_func_condition()
                        step["conditions"].append(condition)

                    elif token_type == "NUMBER":
                        step["index"] = int(token_value)
                        self.advance()

                    if self.next_token()[0] == "RBRACKET":
                        self.advance()  # skip ]

                steps.append(step)
                current_traverse = None
                continue

            raise Exception(f"Unexpected token {token_type} {token_value}")

        return steps

    def parse_attr_condition(self):
        # 解析 @Name="xxx" 这种条件
        token_type, attr_name = self.next_token()
        assert token_type == "ATTR"
        self.advance()

        token_type, op = self.next_token()
        assert token_type == "EQUAL"
        self.advance()

        token_type, value = self.next_token()
        assert token_type == "STRING"
        self.advance()

        return {"attr": attr_name, "op": "=", "value": value}

    def parse_func_condition(self):
        # 解析 contains(@AutomationId, "15") 这种函数条件
        token_type, func_name = self.next_token()
        assert token_type == "FUNC"
        self.advance()

        token_type, _ = self.next_token()
        assert token_type == "LPAREN"
        self.advance()

        token_type, attr_name = self.next_token()
        assert token_type == "ATTR"
        self.advance()

        token_type, _ = self.next_token()
        assert token_type == "COMMA"
        self.advance()

        token_type, value = self.next_token()
        assert token_type == "STRING"
        self.advance()

        token_type, _ = self.next_token()
        assert token_type == "RPAREN"
        self.advance()

        return {"func": func_name, "attr": attr_name, "value": value}


class XPathFinder:
    def __init__(self, root_element):
        self.root = root_element

    def find_all(self, steps):
        current_elements = [self.root]
        for step in steps:
            print(f"Processing step: {step}")
            matched_elements = []
            for elem in current_elements:
                if step["traverse"] == "child":
                    children = self.get_children(elem)
                else:
                    children = self.get_descendants(elem)

                if children is None:
                    raise Exception("没有找到元素")

                for child in children:
                    if self.match(child, step):
                        matched_elements.append(child)

            # 应用 index，如果指定了
            if step["index"] is not None:
                idx = step["index"] - 1
                if 0 <= idx < len(matched_elements):
                    current_elements = [matched_elements[idx]]
                else:
                    current_elements = []
            else:
                current_elements = matched_elements

        return current_elements

    def get_children(self, element: Control):
        # 应该返回直接子元素列表
        # 这里示例, 真实的根据你用的库改
        return element.GetChildren()

    def get_descendants(self, element: Control):
        # 应该返回所有后代元素列表
        descendants = []
        child = element.GetFirstChildControl()
        while child:
            descendants.append(child)
            descendants.extend(self.get_descendants(child))
            child = child.GetNextSiblingControl()
        return descendants

    def match(self, element: Control, step):
        # 先匹配节点类型
        print(
            f"Matching element: {element.Name}, ControlType: {element.ControlTypeName}"
        )
        if element.ControlTypeName != step["node_type"] and step["node_type"] != "*":
            return False

        # 然后匹配所有条件
        print("Matching conditions:")
        for cond in step["conditions"]:
            if "attr" in cond and "op" in cond:
                value = getattr(element, cond["attr"], None)
                if value != cond["value"]:
                    return False
            elif "func" in cond and cond["func"] == "contains":
                value = getattr(element, cond["attr"], None)
                if cond["value"] not in (value or ""):
                    return False
            else:
                raise Exception(f"未知的条件: {cond}")

        return True
