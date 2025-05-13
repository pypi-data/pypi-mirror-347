import os
import pytest
@pytest.fixture(autouse=True)
def change_working_directory():
    original_directory = os.getcwd()  # Speichere das originale Verzeichnis
    #os.chdir(os.path.join(os.path.dirname(__file__), "tests"))  # Setze das Arbeitsverzeichnis auf 'tests'
    os.chdir(os.path.dirname(__file__))  # Setze das Arbeitsverzeichnis auf 'tests'
    yield  # Führe den Test aus
    os.chdir(original_directory)  # Setze das Arbeitsverzeichnis zurück, wenn der Test abgeschlossen ist
