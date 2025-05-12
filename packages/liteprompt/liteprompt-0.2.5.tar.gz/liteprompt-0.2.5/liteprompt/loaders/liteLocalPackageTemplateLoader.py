from .liteTemplateLoader import LiteTemplateLoader
from prompt_poet.template_loaders import LocalPackageTemplateLoader


class LiteLocalPackageTemplateLoader(LiteTemplateLoader, LocalPackageTemplateLoader):
    """Renamed LocalPackageTemplateLoader from prompt_poet with no modifications."""

    pass
