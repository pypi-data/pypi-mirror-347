import logging

logger = logging.getLogger(__name__)

__all__ = []

from .liteTemplateLoader import LiteTemplateLoader
from .liteLocalFSTemplateLoader import LiteLocalFSTemplateLoader
from .liteLocalPackageTemplateLoader import LiteLocalPackageTemplateLoader
from .liteCacheLoader import LiteCacheLoader
from .liteGCSDictTemplateLoader import LiteGCSDictTemplateLoader

try:
    import boto3
    from .liteS3AmazonTemplateLoader import LiteAmazonS3TemplateLoader

    __all__ += ["LiteAmazonS3TemplateLoader"]
except ImportError:
    boto3 = None
    LiteAmazonS3TemplateLoader = None

__all__ += [
    "LiteTemplateLoader",
    "LiteLocalFSTemplateLoader",
    "LiteLocalPackageTemplateLoader",
    "LiteCacheLoader",
    "LiteGCSDictTemplateLoader",
]
