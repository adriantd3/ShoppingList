from pathlib import Path


def test_no_app_tests_directory() -> None:
    project_root = Path(__file__).resolve().parents[3]
    assert not (project_root / "app" / "tests").exists()


def test_no_flat_tests_in_unit_or_integration_roots() -> None:
    project_root = Path(__file__).resolve().parents[3]
    flat_unit_tests = sorted((project_root / "tests" / "unit").glob("test_*.py"))
    flat_integration_tests = sorted((project_root / "tests" / "integration").glob("test_*.py"))

    assert flat_unit_tests == []
    assert flat_integration_tests == []