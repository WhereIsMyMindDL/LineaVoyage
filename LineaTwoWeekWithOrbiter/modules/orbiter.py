from loguru import logger
import random
import time

from modules.myaccount import Account
from help import sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data, check_gas, retry
from settings import decimal_places, stay_eth

chains = {
    "Optimism": ["0xe4edb277e41dc89ab076a1f049f4a3efa700bce8", "9007"],
    "zkSync": ["0xE4eDb277e41dc89aB076a1F049f4a3EfA700bCE8", "9014"],
    "Scroll": ["0xe4edb277e41dc89ab076a1f049f4a3efa700bce8", "9019"],
    "Linea": ["0xe4edb277e41dc89ab076a1f049f4a3efa700bce8", "9023"],
}


class OrbiterBridge(Account):
    send_list = ''
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        send_list = ''
        self.send_list = send_list

    @check_gas
    @retry
    def bridge(self, from_chain, to_chain):
        global send_list
        stay_eth_in_network = round(random.uniform(stay_eth[0], stay_eth[1]), decimal_places)

        value_in_eth = self.get_balance()["balance"] - stay_eth_in_network
        value_in_wei = int(self.w3.to_wei(value_in_eth, "ether"))

        value_str = str(value_in_wei)[:-4]
        transaction = get_tx_data(self, chains[from_chain][0], value=int(value_str + str(chains[to_chain][1])))

        logger.info(f'Orbiter: Bridge {"{:0.9f}".format(value_in_eth)} ETH from {from_chain} to {to_chain}...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)
        if txstatus == 1:
            logger.success(f'Orbiter: Bridge {"{:0.9f}".format(value_in_eth)} ETH {from_chain} to {to_chain}: {self.scan + tx_hash}')
            self.send_list += (f'\n{SUCCESS}Orbiter: Bridge {"{:0.4f}".format(value_in_eth)} ETH {from_chain} to {to_chain} - [tx hash]({self.scan + tx_hash})')
            time.sleep(25)
            self.wait_balance(transaction['value'], to_chain)
        else:
            logger.error(f'Orbiter: Bridge {"{:0.9f}".format(value_in_eth)} ETH {from_chain} to {to_chain}: {self.scan + tx_hash}')
            self.send_list += (f'\n{FAILED}Orbiter: Bridge {"{:0.4f}".format(value_in_eth)} ETH {from_chain} to {to_chain} - [tx hash]({self.scan + tx_hash})')

    def main(self, from_chain, to_chain):
        OrbiterBridge.bridge(self, from_chain, to_chain)
        sleeping_between_transactions()
        return self.send_list