from .anthropic import AnthropicProvider
from .openai import OpenAIProvider
from typing import TypeAlias, Literal, Union
from genotype import Model


class DependencyProviderV1(Model):
    """Provider dependency. It defines a provider that is required for
    the collection to operate."""

    type: Literal["provider"]
    """Dependency type."""
    id: Union[OpenAIProvider, AnthropicProvider]
    """Provider id."""


DependencyV1: TypeAlias = DependencyProviderV1
"""Payload dependency."""
