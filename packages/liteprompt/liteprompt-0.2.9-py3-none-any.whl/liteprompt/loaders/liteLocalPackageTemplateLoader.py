from .liteTemplateLoader import LiteTemplateLoader
from liteprompt.libs.prompt_poet.template_loaders import LocalPackageTemplateLoader


class LiteLocalPackageTemplateLoader(LiteTemplateLoader, LocalPackageTemplateLoader):
    """Renamed LocalPackageTemplateLoader from liteprompt.libs.prompt_poet with no modifications."""

    pass
