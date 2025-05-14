import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoGetRPCTool(BaseTool):
    name = "crypto_get_rpc"
    description = """Fetch the RPC endpoint for a given chain ID.

Input (JSON string):
- chainId: The chain ID for which you want the RPC endpoint (e.g., 1 for Ethereum).
"""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str = "", run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)
            chain_id = parsed_input.get("chainId")

            if not chain_id:
                raise ValueError("chainId is required")

            rpc_endpoint = self.sdk.crypto.get_rpc(chain_id)

            return json.dumps({
                "status": "success",
                "chainId": chain_id,
                "rpcEndpoint": rpc_endpoint
            })

        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error) or "Failed to get RPC endpoint",
                "code": getattr(error, "code", "CRYPTO_GET_RPC_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
