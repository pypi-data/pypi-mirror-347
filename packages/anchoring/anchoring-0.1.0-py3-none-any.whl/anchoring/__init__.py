"""
Anchoring: Selective Prompt Anchoring (SPA) for LLMs

SPA is a technique that allows for selective control over which parts of prompts 
influence language model generation.
"""

__version__ = "0.1.0"

# Import main components
from .spa import (
    SPALogitsProcessor,
    spa_tokenize,
    format_spa_input,
    preprocess_anchors,
    create_masked_attention,
    create_default_attention_mask,
    convert_to_tensor_format,
    get_mask_messages
)

from .spa_pipeline import (
    SPAPipeline,
    register_spa_pipeline
)

# Register the pipeline when the package is imported
register_spa_pipeline()

__all__ = [
    # Core SPA components
    "SPALogitsProcessor",
    "spa_tokenize",
    "format_spa_input",
    "preprocess_anchors",
    "create_masked_attention",
    "create_default_attention_mask",
    "convert_to_tensor_format",
    "get_mask_messages",
    
    # Pipeline components
    "SPAPipeline",
    "register_spa_pipeline"
] 