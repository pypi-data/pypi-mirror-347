# LitePrompt: A Flexible Template-Based Prompt Engineering Library

`LitePrompt` is a Python library designed to provide a flexible and extensible system for managing and generating prompts for conversational AI systems. It leverages template-based prompt generation, with support for various storage backends, caching mechanisms, and structured prompt formats. The library allows developers to create complex, context-aware prompts with minimal setup and dependencies.

## Key Features

* **Template-based prompt generation**: Utilizes Jinja2 for flexible template rendering.
* **Multiple storage backends support**: Load templates from local files, Amazon S3, Google Cloud Storage, and local packages.
* **Built-in caching**: Optimizes performance by caching templates.
* **Role-based messaging**: Generates structured prompts with user, system, and assistant roles.
* **Multi-modal content**: Supports text, images, and file-based content.
* **Flexible template management**: Load and manage templates with ease.

## Repository Structure

```
LitePrompt/
├── liteprompt/                 # Core library implementation
│   ├── __init__.py            # Library initialization and dependency management
│   ├── exceptions.py          # Custom exception definitions
│   ├── prompt.py              # Core prompt generation and management
│   ├── registry.py            # Template registry implementation
│   └── loaders/               # Template loader implementations
│       ├── liteCacheLoader.py             # Caching implementation
│       ├── liteGCSDictTemplateLoader.py   # Google Cloud Storage loader
│       ├── liteLocalFSTemplateLoader.py   # Local filesystem loader
│       ├── liteLocalPackageTemplateLoader.py # Package-based loader
│       ├── liteS3AmazonTemplateLoader.py  # Amazon S3 loader
│       └── liteTemplateLoader.py          # Base loader interface
├── main.py                    # Example usage and implementation
└── pyproject.toml            # Project configuration and dependencies
```

## Usage Instructions

### Prerequisites

* **Python version**: 3.10 - 3.12
* **Required packages**:

  * `prompt-poet` (install without dependencies): `pip install prompt-poet==0.0.47 --no-deps`
  * `PyYAML`
  * `Jinja2`
* **Optional packages** (install based on your use case):

  * `boto3` (for S3 support)
  * `google-cloud-storage` (for GCS support)
  * `tiktoken` (for token counting)
  * `cachetools`

### Installation

You can install `LitePrompt` using pip or directly from the source:

```bash
# Install via pip
pip install liteprompt

# Install from source
git clone https://github.com/ggiallo28/liteprompt.git
cd liteprompt
pip install .
```

### Quick Start

Here’s a quick example of how to use `LitePrompt` to generate a prompt from a template:

```python
from liteprompt.loaders import LiteLocalFSTemplateLoader
from liteprompt.prompt import LitePrompt

# Create a template loader
loader = LiteLocalFSTemplateLoader(
    template_path="./templates/main_prompt.yml.j2"
)

# Define template data
template_data = {
    "character_name": "Ada",
    "username": "User",
    "user_query": "Hello!"
}

# Create and render prompt
prompt = LitePrompt(
    template_data=template_data,
    template_loader=loader
)

# Access generated messages
print(prompt.messages)
```

### More Detailed Examples

#### 1. Using Raw Templates:

```python
raw_template = """
- id: system_prompt
  role: system
  content: {{ content }}
"""

prompt = LitePrompt(
    raw_template=raw_template,
    template_data={"content": "You are a helpful assistant."}
)
```

#### 2. Multi-modal Content:

```python
raw_template = """
- id: user_parts
  role: user
  content:
    - type: text
      text: {{ text }}
    - type: image_url
      image_url:
        url: {{ image_url }}
        detail: high
"""

prompt = LitePrompt(
    raw_template=raw_template,
    template_data={
        "text": "Please analyze this image.",
        "image_url": "https://example.com/image.png"
    }
)
```

## Template Management and Structure

The `LitePrompt` library utilizes a flexible system for loading and managing templates, which can be stored across different backends such as local files, cloud storage (S3, Google Cloud), or packaged templates. The default template loader is capable of handling various types of prompt templates that are structured into multiple sections for different use cases.

### Default Loader Functionality

The default loader is designed to load templates from the local filesystem, allowing for an organized and modular template structure. It supports various types of templates, including:

- **Agent Prompts**: These templates define different agent behaviors, such as interactive, memory-based, or task-specific agents.
- **Procedure Prompts**: Templates focused on guiding an agent through specific steps or procedures, including detailed instructions, context, and summaries.
- **Memory-Based Prompts**: Templates for managing memory-related tasks, like recalling past interactions or episodic memories.
- **Tool and System Prompts**: Templates that help integrate tools or system-level instructions with the conversational flow.
- **User Query and Response Templates**: Specific templates for handling user queries, formulating responses, and managing chat histories.

These templates are stored within subdirectories, allowing for easy organization and flexibility when adding or updating individual components. The system is designed to load only the relevant templates based on the specific requirements of the prompt generation, making it efficient for creating context-aware and dynamic interactions.

The default loader seamlessly integrates these templates into the prompt generation process, allowing developers to specify the path and context for each prompt while maintaining clean separation of concerns across the different sections of the prompt.


### Troubleshooting

#### Common Issues and Solutions:

1. **Missing Dependencies**:

   * Error: `ImportError: 'boto3' is required but not installed`
   * Solution: `pip install boto3`

2. **Template Not Found**:

   * Ensure the template path is correct:

   ```python
   loader = LiteLocalFSTemplateLoader(
       template_path="./absolute/path/to/template.yml.j2"
   )
   ```

3. **Template Rendering Errors**:

   * Check for syntax errors in the template.
   * Ensure all required template variables are provided.
   * Enable debug logging to inspect errors:

   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

## Data Flow

The flow of data through the `LitePrompt` system involves multiple components that work together to generate formatted prompts for AI models:

```ascii
[Template Source] -> [Template Loader] -> [Template Engine]
         |                                      |
         v                                      v
    [Template Cache] <- [Prompt Generator] -> [Formatted Messages]
         ^                     |
         |                     v
[Template Registry]    [Content Validation]
```

### Component Interactions:

1. **Template Loaders**: Fetch templates from various sources like local files, Amazon S3, Google Cloud Storage, or local packages.
2. **Template Cache**: Caches templates to improve performance.
3. **Template Engine (Jinja2)**: Renders templates with provided data.
4. **Prompt Generator**: Creates structured message formats, ready to be used by AI models.
5. **Content Validation**: Ensures the correctness of the rendered content, such as proper formatting and required fields.
6. **Template Registry**: Manages template discovery and versioning for reuse.
7. **Cache System**: Optimizes template loading for faster response times.

## Why Choose `LitePrompt`?

`LitePrompt` was created to provide a flexible, efficient, and lightweight way to manage prompts for conversational AI systems. By separating core functionality from optional advanced features, it ensures that you only install what you need. Whether you're loading templates from a local filesystem, cloud storage, or using advanced caching features, `LitePrompt` gives you the flexibility to adapt to your needs without unnecessary dependencies.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

We welcome contributions! Please refer to the [contributing guidelines](#) for more details on how to get involved.