from functools import wraps
from decimal import Decimal
from typing import Callable, Any, TypeVar
from datetime import datetime


F = TypeVar('F', bound=Callable[..., Any])


def validate_amount(min_amount: Decimal = Decimal("0")) -> Callable[[F], F]:
    """
    Provjera da je iznos pozitivan broj.

    # Doctest: accepts value above minimum
    >>> @validate_amount(Decimal("0.01"))
    ... def f(amount):
    ...     return amount
    >>> f(1)
    1

    # Doctest: raises on too small value
    >>> @validate_amount(Decimal("1"))
    ... def g(amount):
    ...     return amount
    >>> g(0)
    Traceback (most recent call last):
    ...
    ValueError: Iznos mora biti veći od 1. Dobiveno: 0
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            amount = kwargs.get('amount')

            if not amount and args:
                for arg in args[1:] if args and hasattr(args[0], '__dict__') else args:
                    if isinstance(arg, (int, float, Decimal)):
                        amount = Decimal(str(arg))
                        break
            
            if amount is not None:
                amount = Decimal(str(amount))
                if amount < min_amount:
                    raise ValueError(
                        f"Iznos mora biti veći od {min_amount}. Dobiveno: {amount}"
                    )
            
            return func(*args, **kwargs)
        
        return wrapper  # type: ignore
    
    return decorator


def log_operation(operation_name: str) -> Callable[[F], F]:
    """
    Dekorator koji logira operacije.
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Operacija: {operation_name}")
            
            try:
                result = func(*args, **kwargs)
                print(f"[{timestamp}] ✓ Uspješno izvršena")
                return result
            except Exception as e:
                print(f"[{timestamp}] ✗ Greška: {e}")
                raise
        
        return wrapper 
    
    return decorator


def require_non_empty(attribute_name: str) -> Callable[[F], F]:
    """
    Osigurava da je atribut neprazan string.

    # Doctest: raises on empty string
    >>> @require_non_empty("name")
    ... def f(name):
    ...     return name
    >>> f(name="  ")
    Traceback (most recent call last):
    ...
    ValueError: name ne može biti prazan
    """
    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            value = kwargs.get(attribute_name)
            
            if isinstance(value, str) and not value.strip():
                raise ValueError(f"{attribute_name} ne može biti prazan")
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator
