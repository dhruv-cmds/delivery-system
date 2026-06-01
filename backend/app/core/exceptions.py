from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status


class DeliverySystemError(HTTPException):
    """Base exception for delivery system errors."""

    def __init__(
        self,
        error_code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[dict] = None,
    ):
        self.error_code = error_code
        self.message = message

        detail = {
            "error": error_code,
            "message": message,
        }

        # call the parent class (HTTPException is parent class)
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )


class DatabaseError(DeliverySystemError):

    def __init__(
            
        self, 
        message = "Database operation failed"
    ):
        
        super().__init__(

            error_code="DATABASE_ERROR",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class PermissionDeniedError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "You do not have permission to perform this action"
    ):

        super().__init__(

            error_code="PERMISSION_DENIED",
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
class AdminAccessRequiredError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Admin access required"
    ):
        
        super().__init__(

            error_code="ADMIN_ACCESS_REQUIRED",
            message=message, 
            status_code=status.HTTP_403_FORBIDDEN
        )

class UserAlreadyExistsError(DeliverySystemError):

    def __init__(
        self,
        message: str = "User already exists with this name",
    ):
        
        super().__init__(
            error_code="USER_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


class UserNotFoundError(DeliverySystemError):

    def __init__(
        self,
        message: str = "User not found",
    ):
        
        super().__init__(
            error_code="USER_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )



class InvalidTokenError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Invalid token"
    ):

        super().__init__(
            error_code="INVALID_TOKEN",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class TokenExpiredError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Token has expired"
    ):

        super().__init__(
            error_code="TOKEN_EXPIRED",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )


class InvalidCredentialsError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Invalid email or password"
    ):
        
        super().__init__(
            error_code="INVALID_EMAIL_OR_PASSWORD",
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )

class RestaurantNotFoundError(DeliverySystemError):


    def __init__(
    
        self,
        message: str = "Restaurant not found"
    ):
    
        super().__init__(

            error_code="RESTAURANT_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class RestaurantAlreadyExistsError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Restaurant already exists"
    ):

        super().__init__(

            error_code="RESTAURANT_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )


class MenuNotFoundError(DeliverySystemError):

    def __init__(
        
        self,
        message: str = "Menu not found"
    ):
        
        super().__init__(

            error_code="MENU_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class MenuAlreadyExistsError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Menu item already exists"
    ):

        super().__init__(

            error_code="MENU_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )


class OrderNotFoundError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Order not found"
    ):

        super().__init__(

            error_code="ORDER_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class OrderAlreadyDeliveredError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Order has already been delivered",
    ):
        
        super().__init__(
            error_code="ORDER_ALREADY_DELIVERED",
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )


class OrderItemNotFoundError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Order item not found"
    ):

        super().__init__(

            error_code="ORDER_ITEM_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class EmptyOrderError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Order must contain at least one item"
    ):

        super().__init__(

            error_code="EMPTY_ORDER",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class InvalidOrderStateError(DeliverySystemError):

    def __init__(
        self,
        current_state: str,
        expected_state: str | None = None,
    ):
        
        if expected_state:
            message = (
                f"Invalid order state '{current_state}'. "
                f"Expected '{expected_state}'."
            )

        else:
            message = f"Invalid order state '{current_state}'."

        self.current_state = current_state
        self.expected_state = expected_state

        super().__init__(
            error_code="INVALID_ORDER_STATE",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class PaymentNotFoundError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Payment not found"
    ):

        super().__init__(

            error_code="PAYMENT_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class PaymentAlreadyCompletedError(DeliverySystemError):

    def __init__(
            
        self,
        message: str = "Payment has already been completed"
    ):

        super().__init__(
            
            error_code="PAYMENT_ALREADY_COMPLETED",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )



class InsufficientBalanceError(DeliverySystemError):

    def __init__(
        self,
        current_balance: Decimal,
        required_balance: Decimal,
    ):
        
        self.current_balance = current_balance
        self.required_balance = required_balance

        message = (
            f"Insufficient balance. "
            f"Current balance: {current_balance}, "
            f"Required: {required_balance}"
        )


        super().__init__(
            error_code="INSUFFICIENT_BALANCE",
            message=message,
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
        )


class DeliveryPartnerNotFoundError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Delivery partner not found"
    ):

        super().__init__(
            error_code="DELIVERY_PARTNER_NOT_FOUND",
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )


class DeliveryPartnerUnavailableError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Delivery partner is unavailable"
    ):

        super().__init__(
            error_code="DELIVERY_PARTNER_UNAVAILABLE",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )

class DeliveryPartnerAlreadyExistsError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Delivery partner already exists"
    ):

        super().__init__(
            error_code="DELIVERY_PARTNER_ALREADY_EXISTS",
            message=message,
            status_code=status.HTTP_409_CONFLICT
        )


class InvalidOperationError(DeliverySystemError):

    def __init__(
        self,
        message: str = "Invalid operation"
    ):

        super().__init__(
            error_code="INVALID_OPERATION",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )