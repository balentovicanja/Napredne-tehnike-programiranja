"""
Testovi za datotečne modele.

Testira pravilnost podatkovnih struktura.
"""

import unittest
from decimal import Decimal
from datetime import datetime
from src.models import Transaction, Category, TransactionStats


class TestTransaction(unittest.TestCase):
    """Testovi za Transaction klasu."""
    
    def setUp(self) -> None:
        """Priprema test podatke."""
        self.transaction = Transaction(
            id="test-1",
            amount=Decimal("100.50"),
            category="Hrana",
            date=datetime(2025, 1, 15, 10, 30),
            description="Kupovnja namirnica",
            type="expense"
        )
    
    def test_creation(self) -> None:
        """Testira kreiranje transakcije."""
        self.assertEqual(self.transaction.id, "test-1")
        self.assertEqual(self.transaction.amount, Decimal("100.50"))
        self.assertEqual(self.transaction.category, "Hrana")
        self.assertEqual(self.transaction.type, "expense")
    
    def test_to_dict(self) -> None:
        """Testira konverziju u rječnik."""
        data = self.transaction.to_dict()
        
        self.assertEqual(data['id'], "test-1")
        self.assertEqual(data['amount'], "100.50")
        self.assertEqual(data['category'], "Hrana")
        self.assertEqual(data['type'], "expense")
    
    def test_from_dict(self) -> None:
        """Testira kreiranje iz rječnika."""
        data = {
            'id': "test-2",
            'amount': "250.75",
            'category': "Transport",
            'date': "2025-01-15T10:30:00",
            'description': "Benzin",
            'type': "expense"
        }
        
        transaction = Transaction.from_dict(data)
        
        self.assertEqual(transaction.id, "test-2")
        self.assertEqual(transaction.amount, Decimal("250.75"))
        self.assertEqual(transaction.category, "Transport")


class TestTransactionStats(unittest.TestCase):
    """Testovi za TransactionStats klasu."""
    
    def test_balance_calculation(self) -> None:
        """Testira izračun bilance."""
        stats = TransactionStats(
            total_income=Decimal("5000"),
            total_expense=Decimal("2000")
        )
        
        self.assertEqual(stats.balance, Decimal("3000"))
    
    def test_stats_dict(self) -> None:
        """Testira konverziju u rječnik."""
        stats = TransactionStats(
            total_income=Decimal("5000"),
            total_expense=Decimal("2000"),
            transaction_count=15
        )
        
        data = stats.to_dict()
        
        self.assertEqual(data['total_income'], "5000")
        self.assertEqual(data['balance'], "3000")
        self.assertEqual(data['transaction_count'], 15)


if __name__ == '__main__':
    unittest.main()
