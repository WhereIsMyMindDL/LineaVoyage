from loguru import logger
import random

from modules.myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data_withABI
from vars import layerbank_abi, layerbank_abi2
from settings import supply_eth, decimal_places, borrow_eth

send_list = ''
class LayerBank(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)
        self.contract = self.get_contract(contract_address=self.w3.to_checksum_address("0x009a0b7c38b542208936f1179151cd08e2943833"), abi=layerbank_abi)

    @check_gas
    @retry
    def supply(self):
            global send_list
            balance_eth = round(random.uniform(supply_eth[0], supply_eth[1]), decimal_places)
            balance_wei = int(self.w3.to_wei(balance_eth, 'ether'))

            tx_data = get_tx_data_withABI(self, balance_wei)
            transaction = self.contract.functions.supply(self.w3.to_checksum_address('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231'), balance_wei).build_transaction(tx_data)

            logger.info(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH')
            gas = random.randint(300000, 310000)
            txstatus, tx_hash = sign_and_send_transaction(self, transaction, gas)

            if txstatus == 1:
                logger.success(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

            else:
                logger.error(f'LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}LayerBank: Supply {"{:0.9f}".format(balance_eth)} ETH - failed')

    @check_gas
    @retry
    def collateral(self):
        global send_list
        tx_data = get_tx_data_withABI(self)
        transaction = self.contract.functions.enterMarkets([self.w3.to_checksum_address('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231')]).build_transaction(tx_data)
        logger.info(f'LayerBank: Try enable collateral...')
        txstatus, tx_hash = sign_and_send_transaction(self, transaction)
        if txstatus == 1:
            logger.success(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n\n{SUCCESS}LayerBank: Collateral enable - [tx hash]({self.scan + tx_hash})')
            return True

        else:
            logger.error(f'LayerBank: Collateral enable : {self.scan + tx_hash}')
            send_list += (f'\n\n{FAILED}LayerBank: Collateral enable - failed')

    @check_gas
    @retry
    def borrow(self):
        global send_list
        balance_eth = round(random.uniform(borrow_eth[0], borrow_eth[1]), decimal_places)
        balance_wei = int(self.w3.to_wei(balance_eth, 'ether'))

        tx_data = get_tx_data_withABI(self)
        transaction = self.contract.functions.borrow(self.w3.to_checksum_address('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231'), balance_wei).build_transaction(tx_data)
        gas = random.randint(330000, 340000)
        txstatus, tx_hash = sign_and_send_transaction(self, transaction, gas)
        logger.info(f'LayerBank: Borrow {"{:0.9f}".format(balance_eth)} ETH')

        if txstatus == 1:
            logger.success(f'LayerBank: Borrow {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{SUCCESS}LayerBank: Borrow {"{:0.9f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

        else:
            logger.error(f'LayerBank: Borrow {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{FAILED}LayerBank: Borrow {"{:0.9f}".format(balance_eth)} ETH - failed')

    @check_gas
    @retry
    def repayBorrow(self):
        global send_list
        contract = self.get_contract('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231', layerbank_abi2)
        value_in_wei = contract.functions.borrowBalanceOf(self.address).call()
        value_in_eth = self.w3.from_wei(value_in_wei, 'ether')

        tx_data = get_tx_data_withABI(self, value_in_wei)
        transaction = self.contract.functions.repayBorrow(self.w3.to_checksum_address('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231'), value_in_wei).build_transaction(tx_data)

        logger.info(f'LayerBank: repayBorrow {"{:0.9f}".format(value_in_eth)} ETH')
        gas = random.randint(290000, 300000)
        txstatus, tx_hash = sign_and_send_transaction(self, transaction, gas)

        if txstatus == 1:
            logger.success(f'LayerBank: repayBorrow {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{SUCCESS}LayerBank: repayBorrow {"{:0.9f}".format(value_in_eth)} ETH - [tx hash]({self.scan + tx_hash})')

        else:
            logger.error(f'LayerBank: repayBorrow {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{FAILED}LayerBank: repayBorrow {"{:0.9f}".format(value_in_eth)} ETH - failed')

    @check_gas
    @retry
    def withdraw(self):
            global send_list
            tx_data = get_tx_data_withABI(self)
            contract = self.get_contract('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231', layerbank_abi2)
            value_in_wei = contract.functions.balanceOf(self.address).call()
            value_in_eth = self.w3.from_wei(value_in_wei, 'ether')

            transaction = self.contract.functions.redeemUnderlying(self.w3.to_checksum_address('0xc7D8489DaE3D2EbEF075b1dB2257E2c231C9D231'), int(value_in_wei)).build_transaction(tx_data)
            logger.info(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH')

            gas = random.randint(340000, 350000)
            txstatus, tx_hash = sign_and_send_transaction(self, transaction, gas)

            if txstatus == 1:
                logger.success(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n\n{SUCCESS}LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH - [tx hash]({self.scan + tx_hash})')
            else:
                logger.error(f'LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n\n{FAILED}LayerBank: Withdraw {"{:0.9f}".format(value_in_eth)} ETH - failed')

    def main(self):
        global send_list
        send_list = ''
        try:
            LayerBank.supply(self)
            sleeping_between_transactions()

            LayerBank.collateral(self)
            sleeping_between_transactions()

            LayerBank.borrow(self)
            sleeping_between_transactions()

            LayerBank.repayBorrow(self)
            sleeping_between_transactions()

            LayerBank.withdraw(self)
            sleeping_between_transactions()
            return send_list

        except Exception as e:
            logger.error(f'Failed: {str(e)}')
            return send_list