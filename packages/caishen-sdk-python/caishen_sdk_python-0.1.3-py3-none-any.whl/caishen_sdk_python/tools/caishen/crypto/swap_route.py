import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoGetSwapRouteTool(BaseTool):
    name = 'crypto_get_swap_route'
    description = """Get a swap route to exchange tokens between two chains or within the same chain.

Inputs (JSON string):
- wallet: object
  - account: number (required)
- payload: object
  - amount: string (required) — amount to swap (in token units)
  - from: object (required)
    - tokenAddress: string (required)
    - chainType: string (required, e.g., "EVM", "SOLANA")
    - chainId: number (optional)
  - to: object (required)
    - tokenAddress: string (required)
    - chainType: string (required)
    - chainId: number (optional)

Returns swap route data needed to later execute the swap."""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str = "", run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)

            wallet = parsed_input.get("wallet")
            payload = parsed_input.get("payload")

            if not wallet or wallet.get("account") is None:
                raise ValueError("wallet.account is required")
            if not payload or not payload.get("amount") or not payload.get("from") or not payload.get("to"):
                raise ValueError("payload.amount, payload.from, and payload.to are required")

            route_output = self.sdk.crypto.getSwapRoute({
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
                "code": getattr(error, "code", "GET_SWAP_ROUTE_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
