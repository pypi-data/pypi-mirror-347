from liteprompt.libs.prompt_poet.prompt import TruncationBlock as BaseTruncationBlock
from liteprompt.libs.prompt_poet.template import Template as BaseTemplate
from liteprompt.libs.prompt_poet.prompt import Prompt as BasePrompt
import liteprompt.libs.prompt_poet.prompt as lite_prompt

from typing import Optional, Any, Iterable, Union
from typing import Literal, Required, TypedDict
from jinja2schema import infer, to_json_schema
from dataclasses import dataclass, asdict
import yaml
import json


@dataclass
class LiteTruncationBlock(BaseTruncationBlock):
    """Extended TruncationBlock with optional metadata."""

    metadata: Optional[dict] = None


lite_prompt.TruncationBlock = LiteTruncationBlock


class LiteTemplate(BaseTemplate):
    """Custom template class inheriting from Template."""

    metadata: Optional[dict] = None


lite_prompt.Template = LiteTemplate


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
class LiteMessage:
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
        """Convert the LiteMessage to a dictionary, excluding 'id', 'truncation_priority', 'expected_template_data_keys', and 'tokens'."""
        d = self._original_fields.copy() if self._original_fields else {}

        d.pop("id", None)
        d.pop("truncation_priority", None)
        d.pop("expected_template_data_keys", None)
        d.pop("tokens", None)

        return d


lite_prompt.PromptPart = LiteMessage


class LitePrompt(BasePrompt):
    """Custom Prompt class inheriting from Prompt."""

    def __init__(self, *args, **kwargs):
        self._raw_template = kwargs.get("raw_template", None)
        if kwargs.get("raw_template") and "template_path" not in kwargs:
            kwargs["template_path"] = ""
        super().__init__(*args, **kwargs)

    @property
    def messages(self):
        """Override the messages property to use LiteMessage to_dict."""
        return [part.to_dict() for part in self._parts]

    def _render_parts(self):
        """Override the render_parts method to handle LiteMessage with token handling and YAML safety."""
        self._rendered_template = self._template.render_template(self._template_data)
        loaded_yaml = yaml.load(self._rendered_template, Loader=yaml.CSafeLoader)

        self._parts = []
        seen_ids = set()

        for idx, yaml_part in enumerate(loaded_yaml):
            part = LiteMessage(**yaml_part)

            if part.id in seen_ids:
                self.logger.warning(f"Duplicate ID detected: {part.id} (Part {idx})")
            else:
                seen_ids.add(part.id)

            prepared_part = self._prepare_part(part)
            self._parts.append(prepared_part)

    def _cleanup_content(self, part):
        """Handle both string and structured content types."""
        if isinstance(part.content, str):
            content = part.content.strip().replace(self._space_marker, " ")
            part.content = self._unescape_special_characters(content)

    def _prepare_part(self, part: LiteMessage) -> LiteMessage:
        if not part._original_fields:
            part._original_fields = {
                k: v for k, v in asdict(part).items() if v is not None
            }

        self._validate_template_replacements(part)
        self._cleanup_content(part)

        if not self._allow_token_overrides and part.tokens is not None:
            raise ValueError("Token encoding is not allowed to be set manually.")

        if part.tokens is not None:
            self.logger.warning(
                f"Tokens were manually provided in part '{part.id}'. Skipping tokenization."
            )
            self._total_tokens += len(part.tokens)

        return part

    def _index_of(self, identifier: str) -> int:
        for i, part in enumerate(self._parts):
            if part.id == identifier:
                return i
        raise ValueError(f"PromptPart with id '{identifier}' not found.")

    ## TODO: allow to assign a raw_template and template_data
    def assign(self, at: str, item: LiteMessage):
        """Replace an existing message with `item` at the specified ID."""
        idx = self._index_of(at)
        self._parts[idx] = self._prepare_part(item)

    def append(self, item: LiteMessage, *, after: Optional[str] = None):
        """Append a message after a given ID or at the end."""
        item = self._prepare_part(item)
        if after is None:
            self._parts.append(item)
        else:
            idx = self._index_of(after)
            self._parts.insert(idx + 1, item)

    def prepend(self, item: LiteMessage, *, before: Optional[str] = None):
        """Prepend a message before a given ID or at the start."""
        item = self._prepare_part(item)
        if before is None:
            self._parts.insert(0, item)
        else:
            idx = self._index_of(before)
            self._parts.insert(idx, item)

    def list_message_ids(self) -> list[str]:
        """Return a list of message IDs from the prompt parts."""
        return [part.id for part in self._parts if hasattr(part, "id")]

    def get_schema(
        self, schema_type: Literal["json", "raw"] = "raw"
    ) -> Union[str, dict]:
        try:
            parsed_schema = infer(self._raw_template)
            if schema_type == "raw":
                return parsed_schema
            return json.dumps(to_json_schema(parsed_schema), indent=2)
        except Exception as e:
            self.logger.warning(f"Schema inference failed: {e}")
            return {} if schema_type == "raw" else "{}"
        
    ##TODO: add a procedure to save parts as template with the variables
