import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoGetBalanceTool(BaseTool):
    name = "crypto_get_balance"
    description = """Get the crypto balance for a wallet address.

Inputs (JSON string):
- wallet: object
  - address: string (required)
  - chainType: string (required, e.g., "EVM", "SOLANA")
  - chainId: number (optional)
  - publicKey: string (optional)
  - account: number (optional)
- payload: object
  - token: string (optional) — token address or symbol to check balance for (default is native token like ETH, SOL).

Returns the balance as a string."""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str, run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)
            wallet = parsed_input.get("wallet")
            payload = parsed_input.get("payload", {})

            if not wallet or not wallet.get("address") or not wallet.get("chainType"):
                raise ValueError("wallet.address and wallet.chainType are required")

            balance = self.sdk.crypto.get_balance({
                "wallet": wallet,
                "payload": payload
            })

            return json.dumps({
                "status": "success",
                "balance": balance
            })

        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "GET_BALANCE_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
