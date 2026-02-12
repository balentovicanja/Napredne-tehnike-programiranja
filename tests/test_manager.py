"""
Testovi za poslovnu logiku (ExpenseManager).

Testira funkcionalnosti upravitelja troškova.
"""

import unittest
from decimal import Decimal
from datetime import datetime
from pathlib import Path
import tempfile
import json

from src.business.manager import ExpenseManager
from src.storage.json_storage import JsonStorage
from src.models import Transaction


class TestExpenseManager(unittest.TestCase):
    """Testovi za ExpenseManager klasu."""
    
    def setUp(self) -> None:
        """Priprema test okruženje."""
        # Kreiraj privremenu datoteku za testiranje
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.temp_dir.name) / "test.json"
        
        self.storage = JsonStorage(self.test_file)
        self.manager = ExpenseManager(self.storage)
    
    def tearDown(self) -> None:
        """Čisti test okruženje."""
        self.temp_dir.cleanup()
    
    def test_add_transaction(self) -> None:
        """Testira dodavanje transakcije."""
        transaction = self.manager.add_transaction(
            amount=Decimal("100"),
            category="Hrana",
            description="Kupovnja",
            transaction_type="expense"
        )
        
        self.assertIsNotNone(transaction.id)
        self.assertEqual(transaction.amount, Decimal("100"))
        self.assertEqual(transaction.category, "Hrana")
        self.assertEqual(transaction.type, "expense")
    
    def test_add_invalid_amount(self) -> None:
        """Testira dodavanje s neispravnim iznosom."""
        with self.assertRaises(ValueError):
            self.manager.add_transaction(
                amount=Decimal("-10"),
                category="Hrana",
                description="Test"
            )
    
    def test_get_all_transactions(self) -> None:
        """Testira dohvaćanje svih transakcija."""
        self.manager.add_transaction(
            amount=Decimal("100"),
            category="Hrana",
            description="Test 1"
        )
        self.manager.add_transaction(
            amount=Decimal("50"),
            category="Transport",
            description="Test 2"
        )
        
        transactions = self.manager.get_all_transactions()
        self.assertEqual(len(transactions), 2)
    
    def test_delete_transaction(self) -> None:
        """Testira brisanje transakcije."""
        transaction = self.manager.add_transaction(
            amount=Decimal("100"),
            category="Hrana",
            description="Test"
        )
        
        self.manager.delete_transaction(transaction.id)
        
        remaining = self.manager.get_all_transactions()
        self.assertEqual(len(remaining), 0)
    
    def test_get_transactions_by_category(self) -> None:
        """Testira filtriranje po kategoriji."""
        self.manager.add_transaction(
            amount=Decimal("100"),
            category="Hrana",
            description="Test 1"
        )
        self.manager.add_transaction(
            amount=Decimal("50"),
            category="Transport",
            description="Test 2"
        )
        
        food = self.manager.get_transactions_by_category("Hrana")
        self.assertEqual(len(food), 1)
        self.assertEqual(food[0].category, "Hrana")
    
    def test_calculate_stats(self) -> None:
        """Testira izračun statistike."""
        self.manager.add_transaction(
            amount=Decimal("1000"),
            category="Plaća",
            description="Mjesečna plaća",
            transaction_type="income"
        )
        self.manager.add_transaction(
            amount=Decimal("300"),
            category="Hrana",
            description="Kupovnja",
            transaction_type="expense"
        )
        self.manager.add_transaction(
            amount=Decimal("150"),
            category="Transport",
            description="Benzin",
            transaction_type="expense"
        )
        
        stats = self.manager.calculate_stats()
        
        self.assertEqual(stats.total_income, Decimal("1000"))
        self.assertEqual(stats.total_expense, Decimal("450"))
        self.assertEqual(stats.balance, Decimal("550"))
        self.assertEqual(stats.transaction_count, 3)


if __name__ == '__main__':
    unittest.main()
