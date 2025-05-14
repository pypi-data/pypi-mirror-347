from ..ToolBase import ToolBase
from typing import TypedDict
class Tools(TypedDict):
    cash_get_balance: ToolBase
    cash_deposit: ToolBase
    cash_send: ToolBase
    cash_withdraw: ToolBase
    crypto_get_balance: ToolBase
    send_crypto: ToolBase
    swap_crypto: ToolBase
    crypto_get_swap_route: ToolBase