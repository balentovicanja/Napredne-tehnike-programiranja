"""
Testovi za filtere (closures).

Testira funkcionalnosti dinamičkog filtriranja.
"""

import unittest
from datetime import datetime, date
from decimal import Decimal

from src.business.filters import (
    create_category_filter,
    create_date_range_filter,
    create_type_filter,
    create_amount_range_filter,
    combine_filters
)
from src.models import Transaction


class TestFilters(unittest.TestCase):
    """Testovi za filter funkcije."""
    
    def setUp(self) -> None:
        """Priprema test transakcije."""
        self.transactions = [
            Transaction(
                id="1",
                amount=Decimal("100"),
                category="Hrana",
                date=datetime(2025, 1, 10),
                description="Hrana",
                type="expense"
            ),
            Transaction(
                id="2",
                amount=Decimal("2000"),
                category="Plaća",
                date=datetime(2025, 1, 5),
                description="Plaća",
                type="income"
            ),
            Transaction(
                id="3",
                amount=Decimal("50"),
                category="Transport",
                date=datetime(2025, 1, 15),
                description="Autobusa",
                type="expense"
            ),
        ]
    
    def test_category_filter(self) -> None:
        """Testira filtriranje po kategoriji."""
        filter_fn = create_category_filter("Hrana")
        
        filtered = [t for t in self.transactions if filter_fn(t)]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].category, "Hrana")
    
    def test_date_range_filter(self) -> None:
        """Testira filtriranje po datumu."""
        filter_fn = create_date_range_filter(
            start_date=date(2025, 1, 8),
            end_date=date(2025, 1, 12)
        )
        
        filtered = [t for t in self.transactions if filter_fn(t)]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "1")
    
    def test_type_filter(self) -> None:
        """Testira filtriranje po tipu."""
        filter_fn = create_type_filter("income")
        
        filtered = [t for t in self.transactions if filter_fn(t)]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].type, "income")
    
    def test_amount_range_filter(self) -> None:
        """Testira filtriranje po iznosu."""
        filter_fn = create_amount_range_filter(
            min_amount=Decimal("50"),
            max_amount=Decimal("500")
        )
        
        filtered = [t for t in self.transactions if filter_fn(t)]
        
        self.assertEqual(len(filtered), 2)
    
    def test_combine_filters(self) -> None:
        """Testira kombiniranje filtera."""
        category_filter = create_category_filter("Transport")
        type_filter = create_type_filter("expense")
        
        combined = combine_filters(category_filter, type_filter)
        
        filtered = [t for t in self.transactions if combined(t)]
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].id, "3")


if __name__ == '__main__':
    unittest.main()
