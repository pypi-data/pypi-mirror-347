from .liteTemplateLoader import LiteTemplateLoader
from prompt_poet.template_loaders import LocalFSTemplateLoader


class LiteLocalFSTemplateLoader(LiteTemplateLoader, LocalFSTemplateLoader):
    """Renamed LocalFSTemplateLoader from prompt_poet with no modifications."""

    pass
