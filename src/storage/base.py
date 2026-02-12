from abc import ABC, abstractmethod
from typing import Protocol
from src.models import Transaction


class StorageInterface(ABC):
    
    @abstractmethod
    def load(self) -> list[Transaction]:
        """
        Učitava sve transakcije iz pohrane.
        
        Returns:
            Lista svih pohranjenih transakcija
            
        Raises:
            IOError: Ako se dogodi greška pri učitavanju
        """
        pass
    
    @abstractmethod
    def save(self, transactions: list[Transaction]) -> None:
        """
        Sprema sve transakcije u pohranu.
        
        Args:
            transactions: Lista transakcija za spremanje
            
        Raises:
            IOError: Ako se dogodi greška pri spremanju
        """
        pass
    
    @abstractmethod
    def add(self, transaction: Transaction) -> None:
        """
        Dodaje novu transakciju.
        
        Args:
            transaction: Transakcija za dodavanje
        """
        pass
    
    @abstractmethod
    def update(self, transaction: Transaction) -> None:
        """
        Ažurira postojeću transakciju.
        
        Args:
            transaction: Ažurirana transakcija
            
        Raises:
            ValueError: Ako transakcija ne postoji
        """
        pass
    
    @abstractmethod
    def delete(self, transaction_id: str) -> None:
        """
        Briše transakciju prema ID-u.
        
        Args:
            transaction_id: ID transakcije za brisanje
            
        Raises:
            ValueError: Ako transakcija ne postoji
        """
        pass
    
    @abstractmethod
    def get_by_id(self, transaction_id: str) -> Transaction | None:
        """
        Dohvaća transakciju prema ID-u.
        
        Args:
            transaction_id: ID transakcije
            
        Returns:
            Pronađena transakcija ili None
        """
        pass
    
    @abstractmethod
    def get_all(self) -> list[Transaction]:
        """
        Dohvaća sve transakcije.
        
        Returns:
            Lista svih transakcija
        """
        pass


class StorageProtocol(Protocol):

    def load(self) -> list[Transaction]:
        ...
    
    def save(self, transactions: list[Transaction]) -> None:
        ...
    
    def add(self, transaction: Transaction) -> None:
        ...
    
    def update(self, transaction: Transaction) -> None:
        ...
    
    def delete(self, transaction_id: str) -> None:
        ...
    
    def get_by_id(self, transaction_id: str) -> Transaction | None:
        ...
    
    def get_all(self) -> list[Transaction]:
        ...
