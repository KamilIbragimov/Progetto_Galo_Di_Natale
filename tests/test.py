import pytest
from unittest.mock import patch
from io import StringIO
from Credenziali import Generatore_Password, Convalida_Email, Convalida_Sito_Web, Utente

# Test per la classe Generatore_Password
def test_generatore_password():
    # Test per una password di lunghezza valida
    password = Generatore_Password.genera(12)
    assert password is not None
    assert len(password) == 12  # Verifica che la lunghezza della password sia 12
    assert any(c.isupper() for c in password)  # Controlla se c'è almeno una lettera maiuscola
    assert any(c.islower() for c in password)  # Controlla se c'è almeno una lettera minuscola
    assert any(c.isdigit() for c in password)  # Controlla se c'è almeno un numero
    assert any(c in string.punctuation for c in password)  # Controlla se c'è almeno un carattere speciale

    # Test per una password di lunghezza non valida
    password_invalid = Generatore_Password.genera(5)
    assert password_invalid is None  # La password non dovrebbe essere generata

# Test per la classe Convalida_Email
@patch("builtins.input", return_value="test@example.com")
def test_convalida_email(mock_input):
    convalida_email = Convalida_Email()
    email = convalida_email.valida()  # Qui non viene chiesta interazione, viene usato il valore mockato
    assert email == "test@example.com"  # Verifica che l'email sia quella mockata

# Test per la classe Convalida_Sito_Web
@patch("builtins.input", return_value="google.com")
@patch("requests.get")
def test_convalida_sito_web(mock_get, mock_input):
    mock_get.return_value.status_code = 200  # Mock per il sito che esiste (status 200)
    
    convalida_sito = Convalida_Sito_Web()
    sito = convalida_sito.valida()
    assert sito == "google.com"  # Verifica che il sito sia quello mockato

    # Caso in cui il sito non è raggiungibile (status 404)
    mock_get.return_value.status_code = 404
    sito_non_raggiungibile = convalida_sito.valida()
    assert sito_non_raggiungibile == "google.com"  # Anche se lo status code è 404, testiamo la logica.

# Test per la classe Utente
def test_utente():
    utente = Utente(email="test@example.com", password="Password123!", sito_web="google.com")
    
    assert utente.email == "test@example.com"  # Verifica che l'email sia corretta
    assert utente.password == "Password123!"  # Verifica che la password sia corretta
    assert utente.sito_web == "google.com"  # Verifica che il sito web sia corretto

# Test per la visualizzazione delle credenziali
@patch("sys.stdout", new_callable=StringIO)
def test_visualizza_credenziali(mock_stdout):
    # Creiamo un oggetto Utente con delle credenziali
    utente = Utente(email="test@example.com", password="Password123!", sito_web="google.com")
    
    # Visualizza le credenziali
    utente_str = str(utente)
    print(utente_str)

    # Verifica che l'output contenga l'email, la password e il sito web
    output = mock_stdout.getvalue()
    assert "test@example.com" in output
    assert "Password123!" in output
    assert "google.com" in output

