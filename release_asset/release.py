from algosdk.v2client.algod import AlgodClient
from utils.account import Account
from utils.helpers import print_asset_holding
from algosdk.future.transaction import AssetTransferTxn, wait_for_confirmation


def opt_account_in(algodclient, treasury_account: Account, assetid):
    params = algodclient.suggested_params()
    account_info = algodclient.account_info(treasury_account.getAddress())
    holding = None
    idx = 0
    for my_account_info in account_info["assets"]:
        scrutinized_asset = account_info["assets"][idx]
        idx = idx + 1
        if scrutinized_asset["asset-id"] == assetid:
            holding = True
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=treasury_account.getAddress(),
            sp=params,
            receiver=treasury_account.getAddress(),
            amt=0,
            index=assetid,
        )
        stxn = txn.sign(treasury_account.getPrivateKey())
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algodclient.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(algodclient, txid, 4)
            print(
                "Result confirmed in round: {}".format(confirmed_txn["confirmed-round"])
            )

        except Exception as err:
            print(err)

        print_asset_holding(algodclient, treasury_account.getAddress(), assetid)


def get_treasury_account(TREASURY_SECRET: str):
  return Account(TREASURY_SECRET)


def release_funds_to_treasury(
    client: AlgodClient,
    sender: Account,
    asset_id: int,
    TREASURY_SECRET: str
):
    ido_value = 50_000_000
    seed_round_value = 20_000_000
    marketing_value = 25_000_000
    evr_foundation_value = 5_000_000
    decimal = 6
    total_funds = ido_value + seed_round_value + marketing_value + evr_foundation_value
    total_funds = total_funds * (10**decimal)
    treasury_account = get_treasury_account(TREASURY_SECRET)
    opt_account_in(client, treasury_account, asset_id)
    params = client.suggested_params()

    txn = AssetTransferTxn(
        sender=sender.getAddress(),
        sp=params,
        receiver=treasury_account.getAddress(),
        amt=total_funds,
        index=asset_id,
    )
    stxn = txn.sign(sender.getPrivateKey())
    try:
        txid = client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(client, txid, 4)
        print(
            "Result confirmed in round: {}".format(confirmed_txn["confirmed-round"])
        )
    except Exception as err:
        print(err)
