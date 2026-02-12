from __future__ import annotations

import json
from pathlib import Path
from typing import Optional
from src.models import Transaction
from .base import StorageInterface


class JsonStorage(StorageInterface):
    
    def __init__(self, file_path: Path) -> None:

        self.file_path = Path(file_path)
        self._transactions: list[Transaction] = []
        self._load_from_disk()
    
    def _ensure_file_exists(self) -> None:
        """Osigurava da datoteka postoji."""
        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.file_path.write_text('[]')
    
    def _load_from_disk(self) -> None:
        """Učitava transakcije iz JSON datoteke."""
        self._ensure_file_exists()
        try:
            content = self.file_path.read_text(encoding='utf-8')
            data = json.loads(content) if content else []
            self._transactions = [
                Transaction.from_dict(item) for item in data
            ]
        except (json.JSONDecodeError, IOError) as e:
            raise IOError(f"Greška pri učitavanju podataka: {e}")
    
    def _save_to_disk(self) -> None:
        """Sprema transakcije u JSON datoteku."""
        try:
            data = [t.to_dict() for t in self._transactions]
            content = json.dumps(data, indent=2, ensure_ascii=False)
            self.file_path.write_text(content, encoding='utf-8')
        except IOError as e:
            raise IOError(f"Greška pri spremanju podataka: {e}")
    
    def load(self) -> list[Transaction]:
        return self._transactions.copy()
    
    def save(self, transactions: list[Transaction]) -> None:
        self._transactions = transactions.copy()
        self._save_to_disk()
    
    def add(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)
        self._save_to_disk()
    
    def update(self, transaction: Transaction) -> None:
        for i, t in enumerate(self._transactions):
            if t.id == transaction.id:
                self._transactions[i] = transaction
                self._save_to_disk()
                return
        raise ValueError(f"Transakcija s ID-om {transaction.id} nije pronađena")
    
    def delete(self, transaction_id: str) -> None:
        for i, t in enumerate(self._transactions):
            if t.id == transaction_id:
                del self._transactions[i]
                self._save_to_disk()
                return
        raise ValueError(f"Transakcija s ID-om {transaction_id} nije pronađena")
    
    def get_by_id(self, transaction_id: str) -> Optional[Transaction]:
        for t in self._transactions:
            if t.id == transaction_id:
                return t
        return None
    
    def get_all(self) -> list[Transaction]:
        return self._transactions.copy()
