"""
Standard domain resolvers for mantipy-gui
"""

from .base import DomainResolver
from typing import Optional, Callable


class HTTPResolver(DomainResolver):
    """Resolver that prepends http:// to domains if needed"""
    
    def __init__(self):
        def resolve_http(domain: str) -> str:
            if '://' not in domain:
                return f"http://{domain}"
            return domain
            
        super().__init__("", resolve_http)
    
    def can_resolve(self, domain: str) -> bool:
        return '://' not in domain


class EVRResolver(DomainResolver):
    """Resolver for .evr domains"""
    
    def __init__(self, resolver_func: Optional[Callable[[str], str]] = None):
        if resolver_func is None:
            def default_evr_resolver(domain: str) -> str:
                # Default implementation - replace with actual logic
                # Handle http:// format if present
                domain_clean = domain
                if domain.startswith("http://"):
                    domain_clean = domain.replace("http://", "").rstrip("/")
                    
                # Extract asset name from domain
                clean = domain_clean.upper().replace(".EVR", "")
                try:
                    # This is a placeholder - the actual implementation
                    # would connect to the Evrmore blockchain
                    print(f"Default EVR resolver: Looking up {clean}")
                    return f"https://ipfs.io/ipfs/placeholder-for-{clean}"
                except Exception as e:
                    print(f"[.evr resolve error] {e}")
                    return "about:blank"
            resolver_func = default_evr_resolver
            
        super().__init__(".evr", resolver_func)
        
    def can_resolve(self, domain: str) -> bool:
        """Check if this resolver can handle the given domain"""
        # Use case-insensitive check for .evr domains
        domain_lower = domain.lower()
        
        # Handle URL formatted domain (http://example.evr)
        if '://' in domain_lower:
            # Extract the domain part after the protocol
            parts = domain_lower.split('://', 1)
            if len(parts) == 2:
                domain_part = parts[1].rstrip('/')
                return domain_part.endswith(".evr")
        
        # Handle regular TLD
        return domain_lower.endswith(".evr")


class IPFSResolver(DomainResolver):
    """Resolver for .ipfs domains"""
    
    def __init__(self, gateway: str = "https://ipfs.io/ipfs"):
        def resolve_ipfs(domain: str) -> str:
            # Extract hash from domain
            hash_part = domain.lower().replace(".ipfs", "")
            return f"{gateway}/{hash_part}"
            
        super().__init__(".ipfs", resolve_ipfs) 