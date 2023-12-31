
shuffle = True                                                      # True / False. если нужно перемешать кошельки

decimal_places = 7                                                  # количество знаков, после запятой для генерации случайных чисел
stay_eth = [0.0052, 0.0071]                                         # кол-во эфира, которое остается в сети оптимизм и линея (вычитается из всего баланса в сети)

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
