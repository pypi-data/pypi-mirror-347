"""
Domain resolvers for mantipy-gui

This module provides standard resolvers for various domains.
"""
from urllib.parse import urlparse

class EvrmoreResolver:
    """Resolver for .evr domains using the Evrmore blockchain"""
    
    def __init__(self, rpc_url=None):
        """Initialize the Evrmore resolver"""
        self.rpc_url = rpc_url or "http://user:pass@127.0.0.1:12629"
        self._client = None
        
    @property
    def client(self):
        """Get the Evrmore RPC client"""
        if not self._client:
            try:
                from evrmore_rpc import EvrmoreClient
                self._client = EvrmoreClient(self.rpc_url)
            except ImportError:
                print("[EvrmoreResolver] Warning: evrmore_rpc not installed")
                self._client = None
        return self._client
    
    def resolve(self, url):
        """Resolve an Evrmore domain to a URL"""
        print(f"[EvrmoreResolver] Resolving: {url}")
        
        # Extract the domain part
        if url.startswith(('http://', 'https://')):
            parsed = urlparse(url)
            domain = parsed.netloc
        else:
            domain = url
            
        # Remove .evr extension if present
        if domain.lower().endswith('.evr'):
            domain = domain[:-4]
            
        # Convert to uppercase for Evrmore assets
        asset_name = domain.upper()
        print(f"[EvrmoreResolver] Asset name: {asset_name}")
        
        # Check for test assets first (for development)
        test_assets = {
            "CHESS": {
                "site_pubkey": "02b679f444cf89171eab391f5deb59910c5aa087327e0ff69421dbc44f5ec336ec",
                "site_title": "Chess",
                "site_description": "Peer to Peer chess with client side cryptographic anti-cheat!",
                "site_version": "1.0",
                "admin_asset": "CHESS",
                "content_type": "text/html",
                "content_ipns": "k51qzi5uqu5dit4twu44an063vqc3slwewu9f7qtksj6y4s0y37230njljean4"
            },
            "MANTICORE": {
                "site_title": "Manticore Technologies",
                "site_description": "Open source blockchain technologies",
                "content_ipfs": "QmVbpCdhSMoMjmKfNL3VjkkbrJgEAoE4TQfWqWdEqr7Nuu"
            },
            "TEST": {
                "content_ipfs": "QmYKnSuZPz3K3qj9Nh9yYwns5qWKWzGXsVZjLYqPNrZ5Pe"
            },
            "PYTHON": {
                "content_ipfs": "QmYvZpYtELyTBK4o1nKbvwsA8pJxYES3WgFpHEJEF5CP4J"
            }
        }
        
        try:
            # First check for test assets
            asset_data = None
            if asset_name in test_assets:
                asset_data = test_assets[asset_name]
                print(f"[EvrmoreResolver] Using test asset data for {asset_name}")
            # Otherwise, try to fetch from blockchain
            elif self.client:
                try:
                    asset_data = self.client.get_asset_data(asset_name)
                    if not asset_data:
                        error_msg = f"No asset data found for {asset_name}"
                        print(f"[EvrmoreResolver] Error: {error_msg}")
                        return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p></body></html>"
                except Exception as e:
                    print(f"[EvrmoreResolver] Error fetching asset data: {e}")
                    return f"data:text/html,<html><body><h1>Error</h1><p>Failed to fetch asset data for {asset_name}: {str(e)}</p></body></html>"
            else:
                error_msg = "Evrmore RPC client not available"
                print(f"[EvrmoreResolver] Error: {error_msg}")
                return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p></body></html>"
                
            # Check if we have asset data to work with
            if not asset_data:
                error_msg = f"No asset data found for {asset_name}"
                print(f"[EvrmoreResolver] Error: {error_msg}")
                return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p></body></html>"
                
            print(f"[EvrmoreResolver] Asset data: {asset_data}")
            
            # Check for content_ipns field (preferred for dynamic content)
            if "content_ipns" in asset_data:
                ipns_key = asset_data["content_ipns"]
                gateway_url = f"https://ipfs.io/ipns/{ipns_key}"
                print(f"[EvrmoreResolver] Found IPNS key: {ipns_key}")
                print(f"[EvrmoreResolver] Gateway URL: {gateway_url}")
                return gateway_url
                
            # Check for content_ipfs field
            elif "content_ipfs" in asset_data:
                ipfs_hash = asset_data["content_ipfs"]
                gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
                print(f"[EvrmoreResolver] Found IPFS hash: {ipfs_hash}")
                print(f"[EvrmoreResolver] Gateway URL: {gateway_url}")
                return gateway_url
                
            # Check for legacy ipfs_hash field
            elif "ipfs_hash" in asset_data:
                ipfs_hash = asset_data["ipfs_hash"]
                gateway_url = f"https://ipfs.io/ipfs/{ipfs_hash}"
                print(f"[EvrmoreResolver] Found legacy IPFS hash: {ipfs_hash}")
                print(f"[EvrmoreResolver] Gateway URL: {gateway_url}")
                return gateway_url
                
            # No IPFS/IPNS content found
            else:
                error_msg = f"No IPFS or IPNS content found for asset {asset_name}"
                print(f"[EvrmoreResolver] Error: {error_msg}")
                return f"data:text/html,<html><body><h1>Error</h1><p>{error_msg}</p><p>Asset data: {str(asset_data)}</p></body></html>"
                
        except Exception as e:
            print(f"[EvrmoreResolver] Exception: {e}")
            return f"data:text/html,<html><body><h1>Error</h1><p>Failed to resolve {url}: {str(e)}</p></body></html>"


class IPFSResolver:
    """Resolver for ipfs:// URLs to HTTP gateways"""
    
    def __init__(self, gateway="https://ipfs.io/ipfs"):
        """Initialize the IPFS resolver with a gateway"""
        self.gateway = gateway.rstrip('/')
        
    def resolve(self, url):
        """Resolve an IPFS URL to an HTTP gateway URL"""
        print(f"[IPFSResolver] Resolving: {url}")
        
        if not url.startswith('ipfs://'):
            return url
            
        # Extract the IPFS hash
        ipfs_hash = url.replace('ipfs://', '')
        
        # Construct the gateway URL
        gateway_url = f"{self.gateway}/{ipfs_hash}"
        print(f"[IPFSResolver] Resolved to gateway: {gateway_url}")
        
        return gateway_url 