import sys
import doctest
from pathlib import Path
import unittest


sys.path.insert(0, str(Path(__file__).parent))

from src import models
from src.business import decorators
from src.business import filters


#doctests
def run_doctests() -> None:
    print("=" * 70)
    print("POKRETANJE DOCTEST TESTOVA")
    print("=" * 70)
    
    modules_to_test = [
        ("models", models),
        ("decorators", decorators),
        ("filters", filters)
    ]
    
    total_failures = 0
    total_tests = 0
    
    for name, module in modules_to_test:
        print(f"\n Testiranje {name}...")
        result = doctest.testmod(module, verbose=False)
        total_tests += result.attempted
        total_failures += result.failed
        
        if result.failed == 0:
            print(f"✓ Svi testovi prošli ({result.attempted} testova)")
        else:
            print(f"✗ Neuspješno! ({result.failed}/{result.attempted} testova)")
    
    print(f"\n Ukupno: {total_tests} testova, {total_failures} greške")
    return total_failures == 0


#unittests
def run_unittests() -> None:
    print("\n" + "=" * 70)
    print("POKRETANJE UNITTEST TESTOVA")
    print("=" * 70 + "\n")
    
    # Pronađi sve test datoteke
    loader = unittest.TestLoader()
    start_dir = "tests"
    suite = loader.discover(start_dir, pattern="test_*.py")
    
    # Pokreni testove
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main() -> int:
    """Glavna funkcija."""
    print("\n" + "FINANCE TRACKER - TESTOVI".center(70) + "\n")
    
    # Pokreni sve testove
    doctest_ok = run_doctests()
    unittest_ok = run_unittests()
    
    # Ispis rezultata
    print("\n" + "=" * 70)
    print("SAŽETAK REZULTATA")
    print("=" * 70)
    
    status = "✓ SVE JE OK" if (doctest_ok and unittest_ok) else "✗ GREŠKE DETEKTIRANE"
    print(f"\nStatus: {status}")
    
    return 0 if (doctest_ok and unittest_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
