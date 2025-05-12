# Makes 'genagent' a package

from .llm_utils import (
    gen,
    simple_gen,
    fill_prompt,
    make_output_format,
    modular_instructions,
    parse_json,
    mod_gen,
    get_embedding,
    get_image,
    MemoryNode,
    Agent,
    create_simple_agent,
    ChatSession,
    create_simple_chat
)

__version__ = "0.1.1" # Consider bumping if these changes are published
