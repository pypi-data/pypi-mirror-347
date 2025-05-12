#!/usr/bin/env python3
"""
Test URL resolution logic in the resolvers
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mantipy_gui.resolvers import ResolverRegistry
from mantipy_gui.resolvers.standard import HTTPResolver, EVRResolver


def test_resolver(url):
    """Test the resolver with a given URL"""
    print(f"\n=== Testing URL: {url} ===")
    
    # Create resolver registry
    registry = ResolverRegistry()
    
    # Add HTTP resolver
    registry.register(HTTPResolver())
    
    # Define EVR resolver function
    def custom_evr_resolver(domain):
        print(f"EVR resolver called with: {domain}")
        # Handle http:// format if present
        domain_clean = domain
        if domain.startswith("http://"):
            domain_clean = domain.replace("http://", "").rstrip("/")
            
        # Extract asset name
        asset_name = domain_clean.upper().replace(".EVR", "")
        print(f"Asset name for lookup: {asset_name}")
        return f"https://ipfs.io/ipfs/test-hash-for-{asset_name}"
    
    # Add EVR resolver
    evr_resolver = EVRResolver(custom_evr_resolver)
    registry.register(evr_resolver)
    
    # Test URL resolution
    print(f"Testing resolver.can_resolve: {evr_resolver.can_resolve(url)}")
    resolved = registry.resolve(url)
    print(f"Resolved URL: {resolved}")
    print(f"Changed: {url != resolved}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_url = sys.argv[1]
        test_resolver(test_url)
    else:
        # Test various URL formats
        test_urls = [
            "chess.evr",
            "CHESS.EVR",
            "http://chess.evr",
            "http://chess.evr/",
            "http://CHESS.EVR",
            "http://example.com",
            "example.com",
            "ipfs://QmHash",
        ]
        
        for url in test_urls:
            test_resolver(url) 