
shuffle = False                                                     # True / False. если нужно перемешать кошельки

decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел

delay_wallets = [100, 1500]                                         # минимальная и максимальная задержка между кошельками
delay_transactions = [20, 40]                                       # минимальная и максимальная задержка между транзакциями
waiting_gas = 60                                                    # макс значение газа при котором будет работать скрипт
RETRY_COUNT = 3                                                     # кол-во попыток при возникновении ошибок

supply_eth = [0.0191, 0.02]                                         # кол-во эфира для лендинга LayerBank
borrow_eth = [0.013, 0.0131]                                        # кол-во эфира для лендинга LayerBank

withdraw_from_okex = True                                           # True / False. если нужно выводить с окекса
stay_eth = [0.0052, 0.0071]                                         # кол-во эфира, которое остается в сети линея (вычитается из всего баланса в сети), для депа на окекс

#------okex-options------#
symbolWithdraw = "ETH"                                              # символ токена, не менять, нахуя вам другой токен
network = "Linea"                                                   # ID сети
amount = [0.006, 0.007]                                             # минимальная и максимальная сумма
transfer_subaccount = False                                         # Перевод с субакков на мейн

class API:
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""

#------bot-options------#
bot_status = True                                                   # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id