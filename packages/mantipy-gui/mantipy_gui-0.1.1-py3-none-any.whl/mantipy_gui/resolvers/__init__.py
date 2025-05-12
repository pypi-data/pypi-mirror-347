"""
Domain resolvers for mantipy-gui

This module provides the infrastructure for custom domain resolution
allowing apps to handle custom TLDs like .evr, .ipfs, .dao, etc.
"""

from .base import ResolverRegistry, DomainResolver
from .standard import HTTPResolver

__all__ = ['ResolverRegistry', 'DomainResolver', 'HTTPResolver'] 