from typing import List
from caishen_sdk_python.caishen import CaishenSDK

def create_agent_tools(sdk: CaishenSDK) -> List:
    # Import tools inside the function to avoid circular imports
    from .CaishenCryptoGetBalanceTool import CaishenCryptoGetBalanceTool
    from .CaishenCryptoGetRPCTool import CaishenCryptoGetRPCTool
    from .CaishenCryptoGetSupportedChainTypesTool import CaishenCryptoGetSupportedChainTypesTool
    from .CaishenCryptoGetSwapRouteTool import CaishenCryptoGetSwapRouteTool
    from .CaishenCryptoSendTool import CaishenCryptoSendTool
    from .CaishenBalanceOtherTool import CaishenBalanceOtherTool
    from .CaishenCryptoSwapTool import CaishenCryptoSwapTool
    from .CaishenCashDepositTool import CaishenCashDepositTool
    from .CaishenCashGetBalanceTool import CaishenCashGetBalanceTool
    from .CaishenCashGetSupportedTokensTool import CaishenCashGetSupportedTokensTool
    from .CaishenCashSendTool import CaishenCashSendTool
    from .CaishenCashWithdrawTool import CaishenCashWithdrawTool

    return [
        CaishenCryptoGetBalanceTool(sdk),
        CaishenCryptoGetRPCTool(sdk),
        CaishenCryptoGetSupportedChainTypesTool(sdk),
        CaishenCryptoGetSwapRouteTool(sdk),
        CaishenCryptoSendTool(sdk),
        CaishenBalanceOtherTool(sdk),
        CaishenCryptoSwapTool(sdk),
        CaishenCashDepositTool(sdk),
        CaishenCashGetBalanceTool(sdk),
        CaishenCashGetSupportedTokensTool(sdk),
        CaishenCashSendTool(sdk),
        CaishenCashWithdrawTool(sdk),
    ]
