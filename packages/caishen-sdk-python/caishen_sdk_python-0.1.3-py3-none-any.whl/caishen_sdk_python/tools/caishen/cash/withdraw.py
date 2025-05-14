import json
from langchain.tools import Tool
from caishen import CaishenSDK

class CaishenCashWithdrawTool(Tool):
    name = 'cash_withdraw'
    description = """Withdraw cash from your Caishen account to a specified destination.

    Inputs (JSON string):
    - amount: string (required) — amount to withdraw
    - tokenAddress: string (required) — the token address
    - account: number (required) - account number
    """

    def __init__(self, sdk: CaishenSDK):
        self.sdk = sdk
        super().__init__()

    async def _call(self, input: str) -> str:
        try:
            parsed_input = json.loads(input)

            # Validate required fields
            if not parsed_input.get('amount') or not parsed_input.get('account') or not parsed_input.get('tokenAddress'):
                raise ValueError('amount, account, and tokenAddress are required fields')

            # Withdraw the cash using the SDK
            result = await self.sdk.cash.withdraw(parsed_input)

            return json.dumps({
                'status': 'success',
                'transaction': result
            })
        except Exception as error:
            return json.dumps({
                'status': 'error',
                'message': str(error),
                'code': getattr(error, 'code', 'CASH_WITHDRAW_ERROR')
            })
