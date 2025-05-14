import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoSwapTool(BaseTool):
    name = 'swap_crypto'
    description = """Execute a crypto swap for a wallet after receiving a confirmation code.

Inputs (JSON string):
- wallet: object
  - account: number (required)
  - chainType: string (required, e.g., "EVM", "SOLANA")
- payload: object
  - confirmationCode: string (required) — swap route confirmation code

Returns the swap route output upon success."""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str = "", run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)

            wallet = parsed_input.get("wallet")
            payload = parsed_input.get("payload")

            if not wallet or wallet.get("account") is None or not wallet.get("chainType"):
                raise ValueError("wallet.account and wallet.chainType are required")
            if not payload or not payload.get("confirmationCode"):
                raise ValueError("payload.confirmationCode is required")

            route_output = self.sdk.crypto.swap({
                "wallet": wallet,
                "payload": payload
            })

            return json.dumps({
                "status": "success",
                "routeOutput": route_output
            })

        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "SWAP_CRYPTO_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
