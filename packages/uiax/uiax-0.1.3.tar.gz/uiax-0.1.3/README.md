# Uiax

## 概述
`uiax` 是一个用于 Windows UI 自动化的 Python 库，提供了对 UI 元素的 XPath 查询功能。它基于 `uiautomation`  库构建，允许用户使用 XPath 表达式来查找和操作 UI 元素。


## 使用

### 1. 安装

```bash
pip install uiax
```
### 2. 使用

```python
import uiax

elements = uiax.xpath('//Control[@Name="文件"]')
```

