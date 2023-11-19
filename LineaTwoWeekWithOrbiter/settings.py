
shuffle = True                                                      # True / False. если нужно перемешать кошельки

decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел
value_eth = [0.00001, 0.00006]                                      # минимальное и максимальное кол-во ETH для свапов и ликвы

delay_wallets = [180, 250]                                          # минимальная и максимальная задержка между кошельками
delay_transactions = [20, 40]                                       # минимальная и максимальная задержка между транзакциями
waiting_gas = 30                                                    # макс значение газа при котором будет работать скрипт
RETRY_COUNT = 3                                                     # кол-во попыток при возникновении ошибок

#------okex-options------#
symbolWithdraw = "ETH"                                              # символ токена, не менять, нахуя вам другой токен
network = "Optimism"                                                # ID сети, тоже, работает только в сети оптимизм
amount = [0.567, 0.597]                                             # минимальная и максимальная сумма
transfer_subaccount = True                                          # Перевод с субакков на мейн

class API:
    # okx API
    okx_apikey = ""
    okx_apisecret = ""
    okx_passphrase = ""

#------bot-options------#
bot_status = True                                                   # True / False
bot_token  = ''                                                     # telegram bot token
bot_id     = 0                                                      # telegram id
