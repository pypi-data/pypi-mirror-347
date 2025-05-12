from .liteTemplateLoader import LiteTemplateLoader
from prompt_poet.template_loaders import CacheLoader


class LiteCacheLoader(LiteTemplateLoader, CacheLoader):
    """Renamed CacheLoader from prompt_poet with no modifications."""

    pass
