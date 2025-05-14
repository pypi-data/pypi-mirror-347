from pydantic import BaseModel, Field
from typing import Optional

class CryptoSendSchema(BaseModel):
    address: str = Field(description="The wallet address to send from")
    chainType: str = Field(description='The blockchain type (e.g., "EVM", "SOLANA")')
    chainId: Optional[int] = Field(default=None, description="The chain ID for the blockchain")
    publicKey: Optional[str] = Field(default=None, description="The public key of the wallet")
    account: int = Field(description="The account number")
    toAddress: str = Field(description="The recipient address to send to")
    amount: str = Field(description="The amount to send")
    token: Optional[str] = Field(default=None, description="Token address or symbol (send gas token if not specified)")
    memo: Optional[int] = Field(default=None, description="Transaction memo (for Solana, etc.)")

class CryptoGetBalanceSchema(BaseModel):
    address: str = Field(description="The wallet address to check balance for")
    chainType: str = Field(description='The blockchain type (e.g., "EVM", "SOLANA")')
    chainId: Optional[int] = Field(default=None, description="The chain ID for the blockchain")
    publicKey: Optional[str] = Field(default=None, description="The public key of the wallet")
    account: int = Field(description="The account number")
    token: Optional[str] = Field(default=None, description="Token address or symbol to check balance for (default is native token like ETH, SOL)")


class CryptoSwapSchema(BaseModel):
    account: int = Field(description="The wallet account number to perform the swap from")
    chainType: str = Field(description='The blockchain type (e.g., "EVM", "SOLANA")')
    confirmationCode: str = Field(description="The swap route confirmation code")


class CryptoGetSwapRouteSchema(BaseModel):
    account: int = Field(description="The account number")
    amount: str = Field(description="The amount to swap (in token units)")
    fromAddress: str = Field(description="The source token address")
    fromChainType: str = Field(description='The source blockchain type (e.g., "EVM", "SOLANA")')
    fromChainId: Optional[int] = Field(default=None, description="The source chain ID")
    toAddress: str = Field(description="The destination token address")
    toChainType: str = Field(description="The destination blockchain type")
    toChainId: Optional[int] = Field(default=None, description="The destination chain ID")


# Type aliases
CryptoSendParams = CryptoSendSchema
CryptoGetBalanceParams = CryptoGetBalanceSchema
CryptoSwapParams = CryptoSwapSchema
CryptoGetSwapRouteParams = CryptoGetSwapRouteSchema
