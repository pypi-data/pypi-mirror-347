import json
from langchain.tools import BaseTool
from typing import Optional, Any


class CaishenBalanceOtherTool(BaseTool):
    name = "caishen_balance_other"
    description = "Get the balance of ANOTHER wallet (not your own) or token account on Caishen."

    def __init__(self, sdk: Any, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, input: str, run_manager: Optional[Any] = None) -> str:
        try:
            parsed_input = json.loads(input)

            wallet = {
                "chainType": parsed_input["chainType"],
                "account": parsed_input["account"],
                "chainId": parsed_input.get("chainId"),
            }

            payload = {
                "token": parsed_input.get("tokenAddress")
            }

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
                "code": getattr(error, "code", "UNKNOWN_ERROR")
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported for this tool.")
import json
from langchain.tools import BaseTool  # Adjust import based on actual langchain version
from typing import Optional, Type
from pydantic import BaseModel


class CaishenBalanceOtherInput(BaseModel):
    chainType: str
    account: int
    chainId: Optional[int] = None
    tokenAddress: Optional[str] = None


class CaishenBalanceOtherTool(BaseTool):
    name = "caishen_balance_other"
    description = "Get the balance of ANOTHER wallet (not your own) or token account on Caishen."
    args_schema: Type[BaseModel] = CaishenBalanceOtherInput

    def __init__(self, sdk, **kwargs):
        super().__init__(**kwargs)
        self.sdk = sdk

    def _run(self, chainType: str, account: int, chainId: Optional[int] = None, tokenAddress: Optional[str] = None) -> str:
        try:
            wallet = {
                "chainType": chainType,
                "account": account,
                "chainId": chainId,
            }
            payload = {
                "token": tokenAddress
            }

            balance = self.sdk.crypto.get_balance({
                "wallet": wallet,
                "payload": payload
            })

            return json.dumps({
                "status": "success",
                "balance": balance
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e),
                "code": getattr(e, 'code', 'UNKNOWN_ERROR')
            })

    async def _arun(self, *args, **kwargs):
        raise NotImplementedError("Async execution not supported.")
