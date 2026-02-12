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
        """transakcija --> rječnik za pohranu"""
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
        """Kreira transakciju iz rječnika."""
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
        """Vraća bilancu (prihodi - troškovi)."""
        return self.total_income - self.total_expense
    
    def to_dict(self) -> dict:
        """statistika --> rječnik."""
        return {
            'total_income': str(self.total_income),
            'total_expense': str(self.total_expense),
            'balance': str(self.balance),
            'transaction_count': self.transaction_count,
            'by_category': {k: str(v) for k, v in self.by_category.items()}
        }
