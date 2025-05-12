#!/usr/bin/env python3
"""
Direct test for EVR domain resolution
"""

import sys
from evrmore_rpc import EvrmoreClient

def test_resolve_evr(asset_name):
    """Test direct EVR asset resolution"""
    print(f"Testing EVR asset resolution for: {asset_name}")
    
    try:
        # Create Evrmore client
        client = EvrmoreClient()
        
        # Get asset data
        print(f"Fetching asset data...")
        asset_data = client.getassetdata(asset_name)
        print(f"Asset data result: {asset_data}")
        
        # Check for IPFS hash
        if asset_data and 'ipfs_hash' in asset_data and asset_data['ipfs_hash']:
            ipfs_hash = asset_data['ipfs_hash']
            print(f"✅ Found IPFS hash: {ipfs_hash}")
            print(f"IPFS URL: https://ipfs.io/ipfs/{ipfs_hash}")
        else:
            print(f"❌ No IPFS hash found for asset {asset_name}")
            if asset_data:
                print(f"Available asset data: {asset_data}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        

if __name__ == "__main__":
    # Get command line arguments
    if len(sys.argv) > 1:
        asset_name = sys.argv[1].upper()  # Convert to uppercase
    else:
        # Default assets to test
        print("No asset specified. Testing default assets...")
        default_assets = ["CHESS", "MANTICORE", "PYTHON", "TEST"]
        
        for asset in default_assets:
            print("\n" + "="*50)
            test_resolve_evr(asset)
            print("="*50)
        
        sys.exit(0)
    
    # Test the specified asset
    test_resolve_evr(asset_name) 