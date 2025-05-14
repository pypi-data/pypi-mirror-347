import json
from langchain.tools import Tool
from ....caishen import CaishenSDK

class CaishenCashDepositTool(Tool):
    name = 'cash_deposit'
    description = """Deposit cash into your account using Caishen.

    Inputs (JSON string):
    - amount: string (required) — the amount to deposit
    - tokenAddress: string (required) — the token address
    - account: number (required) — account number
    """

    def __init__(self, sdk: CaishenSDK):
        self.sdk = sdk
        super().__init__()

    async def _call(self, input: str) -> str:
        try:
            parsed_input = json.loads(input)

            # Validate input fields
            if not parsed_input.get('amount') or not parsed_input.get('account') or not parsed_input.get('tokenAddress'):
                raise ValueError('amount, account, and tokenAddress fields are required')

            # Perform the deposit
            result = await self.sdk.cash.deposit(parsed_input)

            return json.dumps({
                'status': 'success',
                'transaction': result
            })
        except Exception as error:
            return json.dumps({
                'status': 'error',
                'message': str(error),
                'code': getattr(error, 'code', 'CASH_DEPOSIT_ERROR')
            })
