from typing import Dict, Callable, Any
from ..caishen import CaishenSDK
from ..cash.schema import CashGetBalanceSchema, DepositCashSchema, SendTransactionSchema, WithdrawCashSchema
from ..crypto.schema import CryptoGetBalanceSchema, CryptoGetSwapRouteSchema, CryptoSendSchema, CryptoSwapSchema
from .ToolBase import ToolBase
from caishen_sdk_python.constants import ChainType
from caishen_sdk_python.tools.interfaces import Tools
import json

async def get_tools(sdk: CaishenSDK) -> Tools:
    tools: Tools = {
        "cash_get_balance": ToolBase(
            name="cash_get_balance",
            description="""Retrieve the cash balance of a specified account.
            
            Inputs (JSON string):
            - account: number (required) — the account number to fetch the balance for.
            """,
            parameters=CashGetBalanceSchema,
            execute=lambda params: _execute_cash_get_balance(sdk, params),
        ),
        
        "cash_deposit": ToolBase(
            name="cash_deposit",
            description="""Deposit cash into your account using Caishen.

            Inputs (JSON string):
            - amount: string (required) — the amount to deposit
            - tokenAddress: string (required)- the token address
            - account: number (required) - account number
            """,
            parameters=DepositCashSchema,
            execute=lambda params: _execute_cash_deposit(sdk, params),
        ),
        
        "cash_send": ToolBase(
            name="cash_send",
            description="""Send cash to another account or destination using Caishen.

            Inputs (JSON string):
            - amount: string (required) — amount to send
            - toAddress: string (required)- another account or destination address
            - account: number (required) - account number
            """,
            parameters=SendTransactionSchema,
            execute=lambda params: _execute_cash_send(sdk, params),
        ),
        
        "cash_withdraw": ToolBase(
            name="cash_withdraw",
            description="""Withdraw cash from your Caishen account to a specified destination.

            Inputs (JSON string):
            - amount: string (required) — amount to withdraw
            - tokenAddress: string (required) — the token address
            - account: number (required) - account number
            """,
            parameters=WithdrawCashSchema,
            execute=lambda params: _execute_cash_withdraw(sdk, params),
        ),
        
        "crypto_get_balance": ToolBase(
            name="crypto_get_balance",
            description="""Get the crypto balance for a wallet address.

            Inputs (JSON string):
            - wallet: object
              - address: string (required)
              - chainType: string (required, e.g., "EVM", "SOLANA")
              - chainId: number (optional)
              - publicKey: string (optional)
              - account: number (optional)
            - payload: object
              - token: string (optional) — token address or symbol to check balance for (default is native token like ETH, SOL).
            Returns the balance as a string.""",
            parameters=CryptoGetBalanceSchema,
            execute=lambda params: _execute_crypto_get_balance(sdk, params),
        ),
        
        "send_crypto": ToolBase(
            name="send_crypto",
            description="""Send crypto from a wallet to another address.

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
            Returns the transaction signature as a string.""",
            parameters=CryptoSendSchema,
            execute=lambda params: _execute_send_crypto(sdk, params),
        ),
        
        "swap_crypto": ToolBase(
            name="swap_crypto",
            description="""Execute a crypto swap for a wallet after receiving a confirmation code.

            Inputs (JSON string):
            - wallet: object
              - account: number (required)
              - chainType: string (required, e.g., "ETHEREUM", "SOLANA")
            - payload: object
              - confirmationCode: string (required) — swap route confirmation code
            Returns the swap route output upon success.""",
            parameters=CryptoSwapSchema,
            execute=lambda params: _execute_swap_crypto(sdk, params),
        ),
        
        "crypto_get_swap_route": ToolBase(
            name="crypto_get_swap_route",
            description="""Get a swap route to exchange tokens between two chains or within the same chain.

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
            Returns swap route data needed to later execute the swap.""",
            parameters=CryptoGetSwapRouteSchema,
            execute=lambda params: _execute_crypto_get_swap_route(sdk, params),
        ),
    }
    
    return tools

# Helper functions to execute each tool's logic
async def _execute_cash_get_balance(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not isinstance(params.get("account"), int):
        raise ValueError("account field must be a number")
    return await sdk.cash.get_balance(params)

async def _execute_cash_deposit(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params for k in ("amount", "account", "tokenAddress")):
        raise ValueError("amount, account, and tokenAddress fields are required")
    return await sdk.cash.deposit(params)

async def _execute_cash_send(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params for k in ("amount", "account", "toAddress")):
        raise ValueError("amount, account, and toAddress fields are required")
    return await sdk.cash.send(params)

async def _execute_cash_withdraw(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params for k in ("amount", "account", "tokenAddress")):
        raise ValueError("amount, account, and tokenAddress fields are required")
    return await sdk.cash.withdraw(params)

async def _execute_crypto_get_balance(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params["wallet"] for k in ("address", "chainType")):
        raise ValueError("wallet.address and wallet.chainType are required")
    return await sdk.crypto.get_balance(params)

async def _execute_send_crypto(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params["payload"] for k in ("toAddress", "amount")):
        raise ValueError("payload.toAddress and payload.amount are required")
    return await sdk.crypto.send(params)

async def _execute_swap_crypto(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not all(k in params["wallet"] for k in ("account", "chainType")):
        raise ValueError("wallet.account and wallet.chainType are required")
    if not params["payload"].get("confirmationCode"):
        raise ValueError("payload.confirmationCode is required")
    return await sdk.crypto.swap(params)

async def _execute_crypto_get_swap_route(sdk: CaishenSDK, params: Dict[str, Any]) -> Any:
    if isinstance(params, str):
        params = json.loads(params)
    if not isinstance(params["wallet"].get("account"), int):
        raise ValueError("wallet.account is required")
    if not all(k in params["payload"] for k in ("amount", "from", "to")):
        raise ValueError("payload.amount, payload.from, and payload.to are required")
    return await sdk.crypto.get_swap_route(params)
