from enum import Enum

class UserRole(str, Enum):

    CUSTOMER = "CUSTOMER"
    DELIVERY_PARTNER = "DELIVERY_PARTNER"
    ADMIN = "ADMIN"
    RESTAURANT_OWNER = "RESTAURANT_OWNER"

class DeliveryPartnerStatus(str, Enum):

    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    OFFLINE = "OFFLINE"

class UserStatus(str, Enum):

    ACTIVE = "ACTIVE"
    CLOSE = "CLOSE"

class RestaurantStatus(str, Enum):

    OPEN = "OPEN"
    CLOSE = "CLOSE"


class VehicleTypeStatus(str, Enum):
    TWO_WHEELER = "Two wheeler"
    FOUR_WHEELER = "Four wheeler"


class MenuStatus(str, Enum):

    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

class OrderStatus(str, Enum):

    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    PICKED_UP = "PICKED_UP"
    DELIVERED = "DELIVERED"
    REPLACE = "REPLACE"
    CANCELLED = "CANCELLED"

class PaymentStatus(str, Enum):

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNED = "REFUNED"

MAX_ORDER_TIMES = 20
MAX_TRANSFER_LIMIT = 50000
