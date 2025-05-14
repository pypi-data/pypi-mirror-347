import json
from langchain.tools import Tool
from caishen import CaishenSDK

class CaishenCashSendTool(Tool):
    name = 'cash_send'
    description = """Send cash to another account or destination using Caishen.

    Inputs (JSON string):
    - amount: string (required) — amount to send
    - toAddress: string (required) — another account or destination address
    - account: number (required) - account number
    """

    def __init__(self, sdk: CaishenSDK):
        self.sdk = sdk
        super().__init__()

    async def _call(self, input: str) -> str:
        try:
            parsed_input = json.loads(input)

            # Validate required fields
            if not parsed_input.get('amount') or not parsed_input.get('account') or not parsed_input.get('toAddress'):
                raise ValueError('amount, account, and toAddress are required fields')

            # Send the cash using the SDK
            result = await self.sdk.cash.send(parsed_input)

            return json.dumps({
                'status': 'success',
                'transaction': result
            })
        except Exception as error:
            return json.dumps({
                'status': 'error',
                'message': str(error),
                'code': getattr(error, 'code', 'CASH_SEND_ERROR')
            })
