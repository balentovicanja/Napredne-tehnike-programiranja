from __future__ import annotations

"""
Filteri za dinamičko filtriranje transakcija korištenjem closures.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Callable
from src.models import Transaction, TransactionType


def create_category_filter(category: str) -> Callable[[Transaction], bool]:
    
    def filter_fn(transaction: Transaction) -> bool:
        return transaction.category.lower() == category.lower()
    
    return filter_fn


def create_date_range_filter(
    start_date: date | None = None,
    end_date: date | None = None
) -> Callable[[Transaction], bool]:
    
    def filter_fn(transaction: Transaction) -> bool:
        trans_date = transaction.date.date() if isinstance(transaction.date, datetime) else transaction.date
        
        if start_date and trans_date < start_date:
            return False
        if end_date and trans_date > end_date:
            return False
        
        return True
    
    return filter_fn


def create_type_filter(
    transaction_type: TransactionType
) -> Callable[[Transaction], bool]:
   
    def filter_fn(transaction: Transaction) -> bool:
        return transaction.type == transaction_type
    
    return filter_fn


def create_amount_range_filter(
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None
) -> Callable[[Transaction], bool]:
    
    def filter_fn(transaction: Transaction) -> bool:
        if min_amount and transaction.amount < min_amount:
            return False
        if max_amount and transaction.amount > max_amount:
            return False
        
        return True
    
    return filter_fn


def combine_filters(
    *filters: Callable[[Transaction], bool]
) -> Callable[[Transaction], bool]:

    def combined_filter(transaction: Transaction) -> bool:
        for filter_fn in filters:
            if not filter_fn(transaction):
                return False
        return True
    
    return combined_filter
