import os
from dotenv import load_dotenv
from algosdk.v2client import algod
from utils.account import Account
from utils.helpers import print_asset_holding, print_created_asset, metadata_hash
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from release_asset.release import release_funds_to_treasury

load_dotenv()

MANAGER_SECRET = os.getenv('MANAGER_SECRET')
TREASURY_SECRET = os.getenv('TREASURY_SECRET')
API_KEY = os.getenv('API_KEY')

def algo_client_setup():
    algod_address = "https://mainnet-algorand.api.purestake.io/ps2"
    algod_token = API_KEY
    headers = {
   "X-API-Key": algod_token,
}
    return algod.AlgodClient(algod_token, algod_address, headers);


def get_manager_account():
  return Account(MANAGER_SECRET)  # type: ignore


algod_client = algo_client_setup()
params = algod_client.suggested_params()
system_account = get_manager_account()

account_info = algod_client.account_info(system_account.addr)
print("Account balance: {} microAlgos".format(account_info.get("amount")) + "\n")


txn = AssetConfigTxn(
    sender=system_account.getAddress(),
    sp=params,
    total=250000000000000,
    default_frozen=False,
    unit_name="EVR",
    asset_name="Everest",
    manager=system_account.getAddress(),
    reserve=system_account.getAddress(),
    freeze=None,
    clawback=None,
    strict_empty_address_check=False,
    url="https://www.everestxhq.com#arc3",
    metadata_hash=metadata_hash(),
    decimals=6,
)
stxn = txn.sign(system_account.getPrivateKey())

try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
    print("Result confirmed in round: {}".format(confirmed_txn["confirmed-round"]))

except Exception as err:
    print("Error::::::: ", err)

try:
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, system_account.getAddress(), asset_id)
    print_asset_holding(algod_client, system_account.getAddress(), asset_id)
except Exception as e:
    print(e)
    
release_funds_to_treasury(algod_client, system_account, asset_id, TREASURY_SECRET)  # type: ignore
