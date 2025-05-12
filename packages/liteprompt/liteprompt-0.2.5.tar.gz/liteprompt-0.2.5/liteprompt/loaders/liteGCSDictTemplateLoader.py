from .liteTemplateLoader import LiteTemplateLoader
from prompt_poet.template_loaders import GCSDictTemplateLoader


class LiteGCSDictTemplateLoader(LiteTemplateLoader, GCSDictTemplateLoader):
    """Renamed GCSDictTemplateLoader from prompt_poet with no modifications."""

    pass
