"""
Podatkovni modeli za aplikaciju.

"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Literal
from decimal import Decimal
import json


TransactionType = Literal["income", "expense"]


@dataclass
class Transaction:
    """
    Predstavlja transakciju (prihod ili trošak).
    
    Attributes:
        id: Jedinstveni identifikator
        amount: Iznos (pozitivan broj)
        category: Kategorija transakcije
        date: Datum transakcije
        description: Opis transakcije
        type: Tip transakcije ('income' ili 'expense')
    """
    id: str
    amount: Decimal
    category: str
    date: datetime
    description: str
    type: TransactionType
    
    def to_dict(self) -> dict:
        """
        transakcija --> rjecnik za pohranu

        # Doctest: serialize a transaction
        >>> from decimal import Decimal
        >>> from datetime import datetime
        >>> t = Transaction(
        ...     id="1",
        ...     amount=Decimal("10.50"),
        ...     category="Food",
        ...     date=datetime(2023, 1, 2, 3, 4, 5),
        ...     description="lunch",
        ...     type="expense"
        ... )
        >>> t.to_dict()["amount"]
        '10.50'
        >>> t.to_dict()["date"]
        '2023-01-02T03:04:05'
        """
        return {
            'id': self.id,
            'amount': str(self.amount),
            'category': self.category,
            'date': self.date.isoformat(),
            'description': self.description,
            'type': self.type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """
        Kreira transakciju iz rjecnika.

        # Doctest: parse amount and date types
        >>> data = {
        ...     "id": "1",
        ...     "amount": "12.00",
        ...     "category": "Food",
        ...     "date": "2023-01-02T03:04:05",
        ...     "description": "x",
        ...     "type": "expense"
        ... }
        >>> t = Transaction.from_dict(data)
        >>> t.amount
        Decimal('12.00')
        >>> t.date.isoformat()
        '2023-01-02T03:04:05'
        """
        data_copy = data.copy()
        data_copy['amount'] = Decimal(data_copy['amount'])
        data_copy['date'] = datetime.fromisoformat(data_copy['date'])
        return cls(**data_copy)


@dataclass
class Category:
    """
    Predstavlja kategoriju transakcije.
    
    Attributes:
        name: Naziv kategorije
        color: Boja za prikaz
    """
    name: str
    color: str = "#000000"
    
    def to_dict(self) -> dict:
        """kategorija --> rječnik"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Category':
        """Kreira kategoriju iz rječnika."""
        return cls(**data)


class TransactionStats:
    
    def __init__(
        self,
        total_income: Decimal = Decimal("0"),
        total_expense: Decimal = Decimal("0"),
        transaction_count: int = 0,
        by_category: dict[str, Decimal] | None = None
    ):
        """
        Inicijalizira statističke podatke.
        
        Args:
            total_income: Ukupni prihodi
            total_expense: Ukupni troškovi
            transaction_count: Broj transakcija
            by_category: Rječnik s troškovima po kategoriji
        """
        self.total_income = total_income
        self.total_expense = total_expense
        self.transaction_count = transaction_count
        self.by_category = by_category or {}
    
    @property
    def balance(self) -> Decimal:
        """
        Vraca bilancu (prihodi - troskovi).

        # Doctest: balance calculation
        >>> from decimal import Decimal
        >>> stats = TransactionStats(total_income=Decimal("20"), total_expense=Decimal("5"))
        >>> stats.balance
        Decimal('15')
        """
        return self.total_income - self.total_expense
    
    def to_dict(self) -> dict:
        """
        statistika --> rjecnik.

        # Doctest: serialize stats with category totals
        >>> from decimal import Decimal
        >>> stats = TransactionStats(
        ...     total_income=Decimal("20"),
        ...     total_expense=Decimal("5"),
        ...     transaction_count=2,
        ...     by_category={"Food": Decimal("5")}
        ... )
        >>> stats.to_dict()["balance"]
        '15'
        >>> stats.to_dict()["by_category"]["Food"]
        '5'
        """
        return {
            'total_income': str(self.total_income),
            'total_expense': str(self.total_expense),
            'balance': str(self.balance),
            'transaction_count': self.transaction_count,
            'by_category': {k: str(v) for k, v in self.by_category.items()}
        }
