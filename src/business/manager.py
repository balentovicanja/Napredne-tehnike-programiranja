from __future__ import annotations

"""
Rad sa transakcijama i glavne funkcionalnosti aplikacije.
"""

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Callable
from src.models import Transaction, TransactionStats, TransactionType
from src.storage.base import StorageInterface
from .decorators import validate_amount, log_operation, require_non_empty
from .filters import (
    create_category_filter,
    create_date_range_filter,
    create_type_filter,
    combine_filters
)


class ExpenseManager:
    
    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage
        self._transactions = storage.load()
    
    @log_operation("Dodavanje transakcije")
    @validate_amount(Decimal("0.01"))
    @require_non_empty("category")
    @require_non_empty("description")
    def add_transaction(
        self,
        amount: Decimal | float | int,
        category: str,
        description: str,
        transaction_type: TransactionType = "expense",
        date_time: datetime | None = None
    ) -> Transaction:
        amount = Decimal(str(amount))
        date_time = date_time or datetime.now()
        
        transaction = Transaction(
            id=str(uuid.uuid4()),
            amount=amount,
            category=category,
            date=date_time,
            description=description,
            type=transaction_type
        )
        
        self._transactions.append(transaction)
        self.storage.add(transaction)
        
        return transaction
    
    @log_operation("Ažuriranje transakcije")
    @validate_amount(Decimal("0.01"))
    def update_transaction(
        self,
        transaction_id: str,
        amount: Decimal | float | int | None = None,
        category: str | None = None,
        description: str | None = None,
        date_time: datetime | None = None
    ) -> Transaction:
        transaction = self.get_transaction(transaction_id)
        if not transaction:
            raise ValueError(f"Transakcija {transaction_id} nije pronađena")
        
        # Ažuriranje samo promijenjenih polja
        if amount is not None:
            transaction.amount = Decimal(str(amount))
        if category is not None:
            transaction.category = category
        if description is not None:
            transaction.description = description
        if date_time is not None:
            transaction.date = date_time
        
        # Ažuriranje u kolekciji
        for i, t in enumerate(self._transactions):
            if t.id == transaction_id:
                self._transactions[i] = transaction
                break
        
        self.storage.update(transaction)
        return transaction
    
    @log_operation("Brisanje transakcije")
    def delete_transaction(self, transaction_id: str) -> None:
        # Provjera postoji li transakcija
        found = any(t.id == transaction_id for t in self._transactions)
        if not found:
            raise ValueError(f"Transakcija {transaction_id} nije pronađena")
        
        # Brisanje iz kolekcije
        self._transactions = [t for t in self._transactions if t.id != transaction_id]
        
        # Brisanje iz pohrane
        self.storage.delete(transaction_id)
    
    def get_transaction(self, transaction_id: str) -> Transaction | None:
        for transaction in self._transactions:
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def get_all_transactions(self) -> list[Transaction]:
        return self._transactions.copy()
    
    def filter_transactions(
        self,
        filter_fn: Callable[[Transaction], bool]
    ) -> list[Transaction]:
        return [t for t in self._transactions if filter_fn(t)]
    
    def get_transactions_by_category(self, category: str) -> list[Transaction]:
        filter_fn = create_category_filter(category)
        return self.filter_transactions(filter_fn)
    
    def get_transactions_by_date_range(
        self,
        start_date: date,
        end_date: date
    ) -> list[Transaction]:
        filter_fn = create_date_range_filter(start_date, end_date)
        return self.filter_transactions(filter_fn)
    
    def get_transactions_by_type(
        self,
        transaction_type: TransactionType
    ) -> list[Transaction]:
        filter_fn = create_type_filter(transaction_type)
        return self.filter_transactions(filter_fn)
    
    def calculate_stats(
        self,
        transactions: list[Transaction] | None = None
    ) -> TransactionStats:
        """
        # Doctest: calculate totals and category sums
        >>> from decimal import Decimal
        >>> from datetime import datetime
        >>> class DummyStorage:
        ...     def __init__(self, items):
        ...         self._items = items
        ...     def load(self):
        ...         return list(self._items)
        ...     def add(self, transaction):
        ...         pass
        ...     def update(self, transaction):
        ...         pass
        ...     def delete(self, transaction_id):
        ...         pass
        >>> t1 = Transaction(
        ...     id="1",
        ...     amount=Decimal("10"),
        ...     category="Food",
        ...     date=datetime(2023, 1, 1, 10, 0, 0),
        ...     description="a",
        ...     type="expense"
        ... )
        >>> t2 = Transaction(
        ...     id="2",
        ...     amount=Decimal("25"),
        ...     category="Salary",
        ...     date=datetime(2023, 1, 2, 10, 0, 0),
        ...     description="b",
        ...     type="income"
        ... )
        >>> manager = ExpenseManager(DummyStorage([t1, t2]))
        >>> stats = manager.calculate_stats()
        >>> stats.total_income
        Decimal('25')
        >>> stats.total_expense
        Decimal('10')
        >>> stats.transaction_count
        2
        >>> stats.by_category["Food"]
        Decimal('10')
        """
        transactions = transactions or self._transactions
        
        total_income = Decimal("0")
        total_expense = Decimal("0")
        by_category: dict[str, Decimal] = {}
        
        for transaction in transactions:
            if transaction.type == "income":
                total_income += transaction.amount
            else:
                total_expense += transaction.amount
            
        
            if transaction.category not in by_category:
                by_category[transaction.category] = Decimal("0")
            by_category[transaction.category] += transaction.amount
        
        return TransactionStats(
            total_income=total_income,
            total_expense=total_expense,
            transaction_count=len(transactions),
            by_category=by_category
        )
    
    def reload_from_storage(self) -> None:
        self._transactions = self.storage.load()
