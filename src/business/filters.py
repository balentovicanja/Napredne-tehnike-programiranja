from __future__ import annotations

"""
Filteri za dinamičko filtriranje transakcija korištenjem closures.
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Callable
from src.models import Transaction, TransactionType


def create_category_filter(category: str) -> Callable[[Transaction], bool]:
    """
    # Doctest: case-insensitive category match
    >>> from decimal import Decimal
    >>> from datetime import datetime
    >>> t = Transaction(
    ...     id="1",
    ...     amount=Decimal("10"),
    ...     category="Food",
    ...     date=datetime(2023, 1, 1, 10, 0, 0),
    ...     description="x",
    ...     type="expense"
    ... )
    >>> f = create_category_filter("food")
    >>> f(t)
    True
    """
    
    def filter_fn(transaction: Transaction) -> bool:
        return transaction.category.lower() == category.lower()
    
    return filter_fn


def create_date_range_filter(
    start_date: date | None = None,
    end_date: date | None = None
) -> Callable[[Transaction], bool]:
    """
    # Doctest: start and end date boundaries
    >>> from decimal import Decimal
    >>> from datetime import datetime, date
    >>> t1 = Transaction(
    ...     id="1",
    ...     amount=Decimal("10"),
    ...     category="Food",
    ...     date=datetime(2023, 1, 1, 10, 0, 0),
    ...     description="x",
    ...     type="expense"
    ... )
    >>> t2 = Transaction(
    ...     id="2",
    ...     amount=Decimal("12"),
    ...     category="Food",
    ...     date=datetime(2023, 2, 1, 10, 0, 0),
    ...     description="y",
    ...     type="expense"
    ... )
    >>> f = create_date_range_filter(date(2023, 1, 15), date(2023, 2, 1))
    >>> f(t1)
    False
    >>> f(t2)
    True
    """
    
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
    """
    # Doctest: type match
    >>> from decimal import Decimal
    >>> from datetime import datetime
    >>> t = Transaction(
    ...     id="1",
    ...     amount=Decimal("10"),
    ...     category="Food",
    ...     date=datetime(2023, 1, 1, 10, 0, 0),
    ...     description="x",
    ...     type="expense"
    ... )
    >>> f = create_type_filter("expense")
    >>> f(t)
    True
    """
   
    def filter_fn(transaction: Transaction) -> bool:
        return transaction.type == transaction_type
    
    return filter_fn


def create_amount_range_filter(
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None
) -> Callable[[Transaction], bool]:
    """
    # Doctest: min and max amount boundaries
    >>> from decimal import Decimal
    >>> from datetime import datetime
    >>> t = Transaction(
    ...     id="1",
    ...     amount=Decimal("10"),
    ...     category="Food",
    ...     date=datetime(2023, 1, 1, 10, 0, 0),
    ...     description="x",
    ...     type="expense"
    ... )
    >>> f = create_amount_range_filter(Decimal("5"), Decimal("10"))
    >>> f(t)
    True
    """
    
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
    """
    # Doctest: combine category and amount filters
    >>> from decimal import Decimal
    >>> from datetime import datetime
    >>> t = Transaction(
    ...     id="1",
    ...     amount=Decimal("10"),
    ...     category="Food",
    ...     date=datetime(2023, 1, 1, 10, 0, 0),
    ...     description="x",
    ...     type="expense"
    ... )
    >>> f1 = create_category_filter("food")
    >>> f2 = create_amount_range_filter(Decimal("5"), Decimal("15"))
    >>> combined = combine_filters(f1, f2)
    >>> combined(t)
    True
    """

    def combined_filter(transaction: Transaction) -> bool:
        for filter_fn in filters:
            if not filter_fn(transaction):
                return False
        return True
    
    return combined_filter
