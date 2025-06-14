from dataclasses import dataclass
from enum import Enum

class PaymentMethod(Enum):
    CASH = 1
    CREDIT_CARD = 2
    SELL_REPLACE = 4

class ProductType(Enum):
    GOLD = 1
    PLATINUM = 2

class ProductWeight(Enum):
    FIFTY_GRAM = 50
    ONE_HUNDRED_GRAM = 100
    FIVE_HUNDRED_GRAM = 500

@dataclass
class Customer:
    full_name: str
    furigana: str
    phone_number: str
    email: str
    address: str
    id_number: str
    id_type: str

@dataclass
class BankAccount:
    bank_name: str
    branch_name: str
    account_number: str

@dataclass
class Product:
    product_type: ProductType
    weight: ProductWeight
    serial_number: str
    price: float

@dataclass
class Order:
    customer: Customer
    products: List[Product]
    payment_method: PaymentMethod
    total_price: float