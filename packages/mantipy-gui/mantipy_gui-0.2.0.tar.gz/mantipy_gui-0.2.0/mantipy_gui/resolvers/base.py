"""
Base resolver classes for mantipy-gui domain resolution
"""

import re
from typing import Dict, Callable, Optional, Union


class DomainResolver:
    """Base class for domain resolvers in mantipy-gui"""
    
    def __init__(self, tld: str, resolver_func: Callable[[str], str]):
        """
        Initialize a domain resolver
        
        Args:
            tld: The top-level domain to handle (e.g., ".evr", ".ipfs")
                 or prefix to handle (e.g., "http://", "ipfs://")
            resolver_func: Function that takes a domain and returns a URL
        """
        self.tld = tld.lower()
        self.is_prefix = not self.tld.startswith('.') and self.tld
        
        # Only auto-add dot for TLD resolvers, not for prefix resolvers
        if not self.is_prefix and not self.tld.startswith('.'):
            self.tld = f".{self.tld}"
            
        self.resolver_func = resolver_func
        
    def can_resolve(self, domain: str) -> bool:
        """Check if this resolver can handle the given domain"""
        domain = domain.lower()
        
        # Handle prefix resolvers (like http://, ipfs://)
        if self.is_prefix:
            return domain.startswith(self.tld)
            
        # Handle URL formatted domain (http://example.evr)
        if '://' in domain:
            # Extract the domain part after the protocol
            parts = domain.split('://', 1)
            if len(parts) == 2:
                domain_part = parts[1].rstrip('/')
                return domain_part.endswith(self.tld)
        
        # Handle regular TLD resolvers
        return domain.endswith(self.tld)
    
    def resolve(self, domain: str) -> str:
        """Resolve the domain to a URL"""
        return self.resolver_func(domain)


class ResolverRegistry:
    """Registry for domain resolvers"""
    
    def __init__(self):
        self.resolvers: Dict[str, DomainResolver] = {}
        
    def register(self, tld: str, resolver_obj) -> None:
        """Register a domain resolver
        
        Args:
            tld: The domain extension or protocol prefix to register (e.g. '.evr', 'ipfs://')
            resolver_obj: An object with a resolve(url) method
        """
        # Create a DomainResolver if we're given a raw function
        if callable(resolver_obj) and not hasattr(resolver_obj, 'resolve'):
            resolver = DomainResolver(tld, resolver_obj)
        # Otherwise, store the object directly with its tld
        else:
            self.resolvers[tld] = resolver_obj
            return resolver_obj
        
    def register_function(self, tld: str, resolver_func: Callable[[str], str]) -> DomainResolver:
        """Register a resolver function for a TLD"""
        resolver = DomainResolver(tld, resolver_func)
        self.register(resolver.tld, resolver)
        return resolver
        
    def resolve(self, url: str) -> str:
        """
        Resolve a URL using registered resolvers
        
        If no resolver is found for the domain, the original URL is returned.
        """
        print(f"[Registry] Resolving: {url}")
        
        # First check for http:// URLs with .evr domains
        if url.lower().startswith('http://') and url.lower().endswith('.evr'):
            for tld, resolver in self.resolvers.items():
                if tld == '.evr':
                    try:
                        result = resolver.resolve(url)
                        print(f"[Registry] Resolved http .evr domain: {url} → {result}")
                        return result
                    except Exception as e:
                        print(f"[Registry] Error resolving .evr domain: {e}")
        
        # Check for specific domain resolvers like .evr
        for tld, resolver in self.resolvers.items():
            if tld.startswith('.') and url.lower().endswith(tld.lower()):
                try:
                    result = resolver.resolve(url)
                    print(f"[Registry] Resolved {url} → {result}")
                    return result
                except Exception as e:
                    print(f"[Registry] Error: {e}")
                    return url
        
        # Check for protocol resolvers like ipfs://
        for tld, resolver in self.resolvers.items():
            if not tld.startswith('.') and url.lower().startswith(tld.lower()):
                try:
                    result = resolver.resolve(url)
                    print(f"[Registry] Resolved {url} → {result}")
                    return result
                except Exception as e:
                    print(f"[Registry] Error: {e}")
                    return url
        
        # No resolver found, ensure proper URL format
        if '://' not in url:
            return f"http://{url}"
            
        # Return original if no changes needed
        return url 