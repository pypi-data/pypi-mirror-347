from pydantic import BaseModel, Field
from typing import Optional


class CashGetBalanceSchema(BaseModel):
    account: int = Field(description="The account number to fetch the balance for")


class SendTransactionSchema(BaseModel):
    toAddress: str = Field(description="The recipient account or destination address")
    amount: str = Field(description="The amount to send")
    account: int = Field(description="The account number to send from")


class DepositCashSchema(BaseModel):
    amount: str = Field(description="The amount to deposit")
    account: int = Field(description="The account number to deposit to")
    tokenAddress: str = Field(description="The token address to deposit")
    chainId: int = Field(description="The chain ID where the token is located")


class WithdrawCashSchema(BaseModel):
    amount: str = Field(description="The amount to withdraw")
    account: int = Field(description="The account number to withdraw from")
    tokenAddress: str = Field(description="The token address to withdraw")
    chainId: int = Field(description="The chain ID where the token should be withdrawn to")


class TokenSchema(BaseModel):
    address: str
    chainId: int
    decimals: int
    name: str
    symbol: str


class BalanceResponseSchema(BaseModel):
    success: bool
    balance: str
    balanceRaw: str


class TransactionResponseSchema(BaseModel):
    success: bool
    message: Optional[str]
    txHash: Optional[str]
    isSuccess: Optional[bool]

# Type aliases (for consistency with the TypeScript version)
CashGetBalanceParams = CashGetBalanceSchema
SendTransactionParams = SendTransactionSchema
DepositCashParams = DepositCashSchema
WithdrawCashParams = WithdrawCashSchema
Token = TokenSchema
BalanceResponse = BalanceResponseSchema
TransactionResponse = TransactionResponseSchema
