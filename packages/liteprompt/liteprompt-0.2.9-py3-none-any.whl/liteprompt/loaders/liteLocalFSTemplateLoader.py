from .liteTemplateLoader import LiteTemplateLoader
from liteprompt.libs.prompt_poet.template_loaders import LocalFSTemplateLoader


class LiteLocalFSTemplateLoader(LiteTemplateLoader, LocalFSTemplateLoader):
    """Renamed LocalFSTemplateLoader from liteprompt.libs.prompt_poet with no modifications."""

    pass
