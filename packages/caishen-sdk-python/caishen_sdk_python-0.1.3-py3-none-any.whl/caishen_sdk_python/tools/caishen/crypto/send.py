import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoSendTool(BaseTool):
    name = "send_crypto"
    description = """Send crypto from a wallet to another address.

        Inputs (JSON string):
        - wallet: object
        - address: string (required)
        - chainType: string (required, e.g., "EVM", "SOLANA")
        - chainId: number (optional)
        - publicKey: string (optional)
        - account: number (optional)
        - payload: object
        - toAddress: string (required) — recipient address
        - amount: string (required) — amount to send
        - token: string (optional) — token address or symbol (send gas token if not specified)
        - memo: number (optional) — transaction memo (for Solana, etc.)

        Returns the transaction signature as a string."""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str = "", run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)

            wallet = parsed_input.get("wallet")
            payload = parsed_input.get("payload")

            if not wallet or not wallet.get("address") or not wallet.get("chainType"):
                raise ValueError("wallet.address and wallet.chainType are required")
            if not payload or not payload.get("toAddress") or not payload.get("amount"):
                raise ValueError("payload.toAddress and payload.amount are required")

            signature = self.sdk.crypto.send({
                "wallet": wallet,
                "payload": payload
            })

            return json.dumps({
                "status": "success",
                "signature": signature
            })

        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error),
                "code": getattr(error, "code", "SEND_CRYPTO_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
