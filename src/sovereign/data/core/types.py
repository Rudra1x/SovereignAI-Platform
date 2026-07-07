"""
Core type definitions used throughout the data platform.
"""

from __future__ import annotations

from enum import Enum


class SourceType(str, Enum):
    LOCAL = "local"
    HTTP = "http"
    GITHUB = "github"
    HUGGINGFACE = "huggingface"
    S3 = "s3"
    AZURE_BLOB = "azure_blob"


class DocumentFormat(str, Enum):
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"
    DOCX = "docx"
    UNKNOWN = "unknown"


class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    UNKNOWN = "unknown"


class DocumentCategory(str, Enum):
    DOCUMENTATION = "documentation"
    TUTORIAL = "tutorial"
    RESEARCH = "research"
    CODE = "code"
    QA = "qa"
    BOOK = "book"
    OTHER = "other"


class LicenseType(str, Enum):
    OPEN = "open"
    PUBLIC_DOCS = "public_docs"
    APACHE_2 = "apache_2"
    MIT = "mit"
    BSD = "bsd"
    UNKNOWN = "unknown"