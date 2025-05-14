import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenCryptoGetSupportedChainTypesTool(BaseTool):
    name = "crypto_get_supported_chain_types"
    description = """Fetch the list of supported chain types for creating wallets.

No input required.
"""

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str = "", run_manager: Optional[Any] = None) -> str:
        try:
            chain_types = self.sdk.crypto.get_supported_chain_types()
            return json.dumps({
                "status": "success",
                "chainTypes": chain_types
            })
        except Exception as error:
            return json.dumps({
                "status": "error",
                "message": str(error) or "Failed to get supported chain types",
                "code": getattr(error, "code", "CRYPTO_GET_SUPPORTED_CHAIN_TYPES_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
