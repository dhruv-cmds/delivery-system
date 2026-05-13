from decimal import Decimal

class OrderAlreadyDeliveredException(Exception):

    def __init__(
        self,
        message: str = "Order has already been delivered"
    ):
        self.message = message
        super().__init__(self.message)


class InvalidOrderStateException(Exception):

    def __init__(
        self,
        current_state: str,
        expected_state: str | None = None
    ):

        if expected_state:
            message = (
                f"Invalid order state '{current_state}'. "
                f"Expected '{expected_state}'."
            )
        else:
            message = (
                f"Invalid order state '{current_state}'."
            )

        self.current_state = current_state
        self.expected_state = expected_state

        super().__init__(message)


class InsufficientBalanceException(Exception):

    def __init__(
        self,
        current_balance: Decimal,
        required_balance: Decimal
    ):

        self.current_balance = current_balance
        self.required_balance = required_balance

        message = (
            f"Insufficient balance. "
            f"Current balance: {current_balance}, "
            f"Required: {required_balance}"
        )

        super().__init__(message)


# USE CASE 

    '''routes'''
    # from core import constants
    # @app.exception_handler(InsufficientBalanceException)
    # async def payment_status (request , exc):

    #     return JSONResponse(
    #         status_code=400,
    #         content={
    #             "current_balance": str(exc.current_balance),
    #             "required_balance": str(exc.required_balance),
    #             "message": str(exc)
    #         }
    #     )

    '''service'''
    # async def transfer_money(sender, receiver, amount):

    #     if sender.balance < amount:

    #         raise InsufficientBalanceException(
    #             current_balance=sender.balance,
    #             required_balance=amount
    #         )

    #     sender.balance -= amount