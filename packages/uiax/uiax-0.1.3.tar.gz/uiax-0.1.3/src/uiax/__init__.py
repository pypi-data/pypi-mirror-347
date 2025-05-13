from uiax.client import Uiax

uiax = Uiax()

# Re-export instance attributes
xpath = uiax.xpath

__all__ = [
    "xpath",  # Add xpath to exports
]

__version__ = "0.1.2"
