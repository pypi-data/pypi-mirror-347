from .liteTemplateLoader import LiteTemplateLoader
from liteprompt.libs.prompt_poet.template_loaders import CacheLoader


class LiteCacheLoader(LiteTemplateLoader, CacheLoader):
    """Renamed CacheLoader from liteprompt.libs.prompt_poet with no modifications."""

    pass
