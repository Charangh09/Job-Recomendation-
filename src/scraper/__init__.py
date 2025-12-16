# src/scraper/__init__.py
"""
Web scraping module for SHL product catalog
"""

from .scrape_shl import SHLScraper
from .parser import AssessmentParser

__all__ = ['SHLScraper', 'AssessmentParser']
