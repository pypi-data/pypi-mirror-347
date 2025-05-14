import json
from langchain.tools import Tool
from ....caishen import CaishenSDK


class CaishenCashGetBalanceTool(Tool):
    name = 'cash_get_balance'
    description = """Retrieve the cash balance of a specified account.

    Inputs (JSON string):
    - account: number (required) — the account number to fetch the balance for.
    """

    def __init__(self, sdk: CaishenSDK):
        self.sdk = sdk
        super().__init__()

    async def _call(self, input: str) -> str:
        try:
            parsed_input = json.loads(input)

            # Validate the input
            if not isinstance(parsed_input.get('account'), int):
                raise ValueError('account field must be a number')

            # Fetch the balance
            result = await self.sdk.cash.get_balance(parsed_input)

            return json.dumps({
                'status': 'success',
                'balance': result
            })
        except Exception as error:
            return json.dumps({
                'status': 'error',
                'message': str(error),
                'code': getattr(error, 'code', 'CASH_GET_BALANCE_ERROR')
            })
