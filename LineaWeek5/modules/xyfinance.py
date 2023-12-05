from loguru import logger
import random

from modules.myaccount import Account
from help import check_gas, retry, sign_and_send_transaction, sleeping_between_transactions, SUCCESS, FAILED, get_tx_data, convert_to
from settings import deposit_eth, decimal_places, xyfinance_fee

send_list = ''
class xyFinance(Account):
    def __init__(self, id, private_key, proxy, rpc):
        super().__init__(id=id, private_key=private_key, proxy=proxy, rpc=rpc)

    @check_gas
    @retry
    def deposit(self):
            global send_list
            deposit = round(random.uniform(deposit_eth[0], deposit_eth[1]), decimal_places)
            deposit_wei = int(self.w3.to_wei(deposit, 'ether'))
            balance_eth = deposit + xyfinance_fee
            value_wei = int(self.w3.to_wei(balance_eth, 'ether'))
            data = f'0xb6b55f2500000000000000000000000000000000000000000000000000{convert_to(deposit_wei, 16)}'

            tx_data = get_tx_data(self, to='0xa5cb30e5d30a9843b6481ffd8d8d35dded3a3251', value=value_wei, data=data)

            logger.info(f'xyFinance: Deposit {"{:0.9f}".format(balance_eth)} ETH')
            txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

            if txstatus == 1:
                logger.success(f'xyFinance: Deposit {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{SUCCESS}xyFinance: Deposit {"{:0.4f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

                self.wait_balance(deposit_wei, 'Linea', '0x74A0EEA77e342323aA463098e959612d3Fe6E686')

            else:
                logger.error(f'xyFinance: Deposit {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
                send_list += (f'\n{FAILED}xyFinance: Deposit {"{:0.4f}".format(balance_eth)} ETH - failed')
    def withdraw(self):
        global send_list
        if self.check_allowance('0x74A0EEA77e342323aA463098e959612d3Fe6E686', '0xA5Cb30E5d30A9843B6481fFd8D8D35DDED3a3251') < 10:
            logger.info(f'xyFinance: try approve token xyETH...')
            send_list += self.approve(115792089237316195423570985008687907853269984665640564039457584007913129639935, '0x74A0EEA77e342323aA463098e959612d3Fe6E686', '0xA5Cb30E5d30A9843B6481fFd8D8D35DDED3a3251')
            sleeping_between_transactions()

        balance = self.get_balance('0x74A0EEA77e342323aA463098e959612d3Fe6E686')
        balance_eth = balance["balance"]
        data = f'0x2e1a7d4d00000000000000000000000000000000000000000000000000{convert_to(balance["balance_wei"], 16)}'
        value_wei = int(self.w3.to_wei(xyfinance_fee, 'ether'))

        tx_data = get_tx_data(self, to='0xa5cb30e5d30a9843b6481ffd8d8d35dded3a3251', value=value_wei, data=data)

        logger.info(f'xyFinance: Withdraw {"{:0.9f}".format(balance_eth)} ETH')
        txstatus, tx_hash = sign_and_send_transaction(self, tx_data)

        if txstatus == 1:
            logger.success(f'xyFinance: Withdraw {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{SUCCESS}xyFinance: Withdraw {"{:0.4f}".format(balance_eth)} ETH - [tx hash]({self.scan + tx_hash})')

        else:
            logger.error(f'xyFinance: Withdraw {"{:0.9f}".format(balance_eth)} ETH : {self.scan + tx_hash}')
            send_list += (f'\n\n{FAILED}xyFinance: Withdraw {"{:0.4f}".format(balance_eth)} ETH - failed')

    def main(self):
        global send_list
        send_list = ''
        try:
            xyFinance.deposit(self)
            sleeping_between_transactions()

            xyFinance.withdraw(self)
            sleeping_between_transactions()

            return send_list

        except Exception as e:
            logger.error(f'Failed: {str(e)}')
            return send_list