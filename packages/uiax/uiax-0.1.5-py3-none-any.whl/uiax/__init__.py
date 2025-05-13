from uiax.client import Uiax

uiax = Uiax()

# Re-export instance attributes
xpath = uiax.xpath
find = uiax.find

__all__ = ["xpath", "find"]  # Add xpath to exports

__version__ = "0.1.4"
