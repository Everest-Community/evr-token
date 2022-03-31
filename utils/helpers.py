import json
import os
import hashlib

TOTAL_SUPPLY = 250_000_000

def print_created_asset(algodclient, my_account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(my_account)
    idx = 0
    for my_account_info in account_info["created-assets"]:
        scrutinized_asset = account_info["created-assets"][idx]
        idx = idx + 1
        if scrutinized_asset["index"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["index"]))
            print(json.dumps(my_account_info["params"], indent=4))
            break


def print_asset_holding(algodclient, my_account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(my_account)
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            print("Asset ID: {}".format(scrutinized_asset["asset-id"]))
            print(json.dumps(scrutinized_asset, indent=4))
            break


def metadata_hash():
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    f = open(dir_path + "/coin-asset/coin-metadata/assetMetaData.json", "r")
    # Reading from file
    metadataJSON = json.loads(f.read())
    metadataStr = json.dumps(metadataJSON)

    hash = hashlib.new("sha512_256")
    hash.update(b"arc0003/amj")
    hash.update(metadataStr.encode("utf-8"))
    json_metadata_hash = hash.digest()
    return json_metadata_hash
