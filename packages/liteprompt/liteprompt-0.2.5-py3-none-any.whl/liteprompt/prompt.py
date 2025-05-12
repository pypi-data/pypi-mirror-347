from prompt_poet.prompt import TruncationBlock as BaseTruncationBlock
from prompt_poet.prompt import Template as BaseTemplate
from prompt_poet.prompt import Prompt as BasePrompt
from typing import Optional, Any, Iterable, Union
from typing import Literal, Required, TypedDict
import prompt_poet.prompt as lite_prompt
from dataclasses import dataclass
import yaml


@dataclass
class LiteTruncationBlock(BaseTruncationBlock):
    """Extended TruncationBlock with optional metadata."""

    metadata: Optional[dict] = None


class LiteTemplate(BaseTemplate):
    """Custom template class inheriting from Template."""

    metadata: Optional[dict] = None


class ChatCompletionSystemMessageParam(TypedDict, total=False):
    content: Required[str]
    """The contents of the system message."""
    role: Required[Literal["system"]]
    """The role of the messages author, in this case `system`."""
    name: str
    """An optional name for the participant."""


class ChatCompletionContentPartTextParam(TypedDict, total=False):
    text: Required[str]
    """The text content."""
    type: Required[Literal["text"]]
    """The type of the content part."""


class ImageURL(TypedDict, total=False):
    url: Required[str]
    """Either a URL of the image or the base64 encoded image data."""
    detail: Literal["auto", "low", "high"]
    """Specifies the detail level of the image."""


class ChatCompletionContentPartImageParam(TypedDict, total=False):
    image_url: Required[ImageURL]
    type: Required[Literal["image_url"]]
    """The type of the content part."""


ChatCompletionContentPartParam = Union[
    ChatCompletionContentPartTextParam, ChatCompletionContentPartImageParam
]


class ChatCompletionUserMessageParam(TypedDict, total=False):
    content: Required[Union[str, Iterable[ChatCompletionContentPartParam]]]
    """The contents of the user message."""
    role: Required[Literal["user"]]
    """The role of the messages author, in this case `user`."""
    name: str
    """An optional name for the participant."""


@dataclass
class LitePromptPart:
    """Extended PromptPart with an additional mandatory 'id' field and optional properties."""

    id: str
    """A clear, human-readable identifier for the part."""

    content: Optional[Union[str, Iterable[ChatCompletionContentPartParam]]] = None
    """The actual string payload that forms part of the prompt."""

    role: Optional[str] = "user"
    """Specifies the role of the participant."""

    expected_template_data_keys: Optional[list[str]] = None
    """A list of keys that are expected to be present in the template data."""

    tokens: Optional[list[int]] = None
    """The tokenized encoding of the content."""

    truncation_priority: Optional[int] = 0
    """Determines the order of truncation when necessary."""

    name: Optional[str] = None
    """The name of the function being called, used to reference which function's response is added to the conversation."""

    tool_calls: Optional[Any] = None
    """Any tool calls associated with this prompt part."""

    function_call: Optional[Any] = None
    """Any function call associated with this prompt part."""

    tool_call_id: Optional[str] = None
    """Identifier for the tool call."""

    _original_fields: Optional[dict] = None
    """Store the original fields from the loaded YAML or data."""

    def to_dict(self):
        """Convert the LitePromptPart to a dictionary, excluding 'id', 'truncation_priority', 'expected_template_data_keys', and 'tokens'."""
        d = self._original_fields.copy() if self._original_fields else {}

        d.pop("id", None)
        d.pop("truncation_priority", None)
        d.pop("expected_template_data_keys", None)
        d.pop("tokens", None)

        return d


lite_prompt.PromptPart = LitePromptPart


class LitePrompt(BasePrompt):
    """Custom Prompt class inheriting from Prompt."""

    def __init__(self, *args, **kwargs):
        if kwargs.get("raw_template") and "template_path" not in kwargs:
            kwargs["template_path"] = ""
        super().__init__(*args, **kwargs)

    @property
    def messages(self):
        """Override the messages property to use LitePromptPart to_dict."""
        return [part.to_dict() for part in self._parts]

    def _render_parts(self):
        """Override the render_parts method to handle LitePromptPart."""
        self._rendered_template = self._template.render_template(self._template_data)
        loaded_yaml = yaml.safe_load(self._rendered_template)

        self._parts = []
        for idx, yaml_part in enumerate(loaded_yaml):
            part = LitePromptPart(**yaml_part)
            part._original_fields = yaml_part
            self._validate_template_replacements(part)
            self._cleanup_content(part)
            self._parts.append(part)

    def _cleanup_content(self, part):
        """Handle both string and structured content types."""
        if isinstance(part.content, str):
            content = part.content.strip().replace(self._space_marker, " ")
            part.content = self._unescape_special_characters(content)
