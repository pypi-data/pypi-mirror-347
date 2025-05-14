import json
from langchain.tools import Tool
from caishen import CaishenSDK

class CaishenCashGetSupportedTokensTool(Tool):
    name = 'cash_get_supported_tokens'
    description = """Fetch the list of supported tokens for cash operations.

    No input required.
    """

    def __init__(self, sdk: CaishenSDK):
        self.sdk = sdk
        super().__init__()

    async def _call(self, _input: str) -> str:
        try:
            # Fetch the supported tokens using the SDK
            tokens = await self.sdk.cash.get_supported_tokens()

            return json.dumps({
                'status': 'success',
                'tokens': tokens
            })
        except Exception as error:
            return json.dumps({
                'status': 'error',
                'message': str(error),
                'code': getattr(error, 'code', 'CASH_GET_SUPPORTED_TOKENS_ERROR')
            })
