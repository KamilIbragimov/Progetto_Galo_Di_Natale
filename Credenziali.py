import random
import string
import requests
import re
from email_validator import validate_email, EmailNotValidError
from termcolor import colored  


# Classe per la convalida dell'email
class Email():
    """Classe per convalidare un indirizzo email."""

    def valida(self) -> str:
        """Convalida un indirizzo email fornito dall’utente."""
        while True:
            try:
                indirizzo_email = input("Inserisci un indirizzo email: ")
                print("\n")
                validato = validate_email(indirizzo_email)
                print(f"L'indirizzo email '{indirizzo_email}' è valido.\n")  
                return indirizzo_email
            except EmailNotValidError as e:
                print("Inserisci un indirizzo email valido.\n")  


# Classe per la convalida del sito web
class Sito_Web():
    """Classe per verificare se un sito web esiste."""
    @staticmethod
    def valida() -> str:
        """Verifica se un sito web inserito dall'utente esiste."""
        while True:
            sito_collegato = input("Inserisci il sito collegato alle credenziali (es. google.com): ")
            print("\n")

            if re.match(r"^[a-zA-Z0-9.-]+$", sito_collegato):
                try:
                    response = requests.get(f"https://{sito_collegato}", timeout=5)
                    if response.status_code == 200:
                        print(f"Il sito {sito_collegato} esiste!\n")  
                        return sito_collegato
                    else:
                        print(f"Il sito {sito_collegato} non è raggiungibile (status code: {response.status_code}).\n")  
                except requests.exceptions.RequestException as e:
                    print(f"Errore nella connessione al sito: {e}\n")  
            else:
                print("Inserisci un sito valido (solo caratteri dell'alfabeto, punti e trattini).\n")  


# Classe per la gestione delle credenziali dell'utente
class Utente:
    """Classe per gestire l'utente con attributi email, password e sito web."""

    def __init__(self, email: str = None, password: str = None, sito_web: str = None):
        """Inizializza l'utente con i suoi attributi."""
        self._email = email
        self._password = password
        self._sito_web = sito_web

    # Getter e Setter per email
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    # Getter e Setter per password
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password

    # Getter e Setter per sito_web
    @property
    def sito_web(self):
        return self._sito_web

    @sito_web.setter
    def sito_web(self, sito_web: str):
        self._sito_web = sito_web

    def __str__(self):
        """Restituisce una rappresentazione stringa delle credenziali dell'utente."""
        return f"Email: {self.email}\nPassword: {self.password}\nSito Web: {self.sito_web}"

class Password:
    """Classe per generare una password casuale."""
    @staticmethod
    def valida() -> int:
        """Chiede la lunghezza della password e la valida."""
        while True:
            try:
                lunghezza = int(input("Inserisci la lunghezza desiderata per la password (minimo 8, massimo 20): "))
                if lunghezza < 8 or lunghezza > 20:
                    print("Errore: La lunghezza della password deve essere tra 8 e 20 caratteri.\n")
                    continue
                return lunghezza
            except ValueError:
                print("Errore: Inserisci un numero intero valido.\n")

    @staticmethod
    def genera(lunghezza: int) -> str:
        """Genera una password casuale in base alla lunghezza specificata."""
        try:
            # Caratteri disponibili per la password
            caratteri = string.ascii_letters + string.digits + string.punctuation

            # Aggiungi almeno un carattere maiuscolo, uno minuscolo, un numero e un carattere speciale
            password = random.choice(string.ascii_uppercase) + random.choice(string.ascii_lowercase) + random.choice(string.digits) + random.choice(string.punctuation)

            # Genera il resto della password casualmente
            lunghezza_rimanente = lunghezza - 4
            password += ''.join(random.choice(caratteri) for _ in range(lunghezza_rimanente))

            # Mescola la password per renderla più casuale
            lista_password = list(password)
            random.shuffle(lista_password)
            password = ''.join(lista_password)

            return password
        except ValueError:
            print("Errore: Inserisci un valore intero positivo per la lunghezza della password.\n")  
            return None

# Classe principale per gestire la creazione delle credenziali utente
class Credenziali_Utente:
    """Classe principale per gestire la creazione delle credenziali utente."""
    def __init__(self):
        """Crea i vari oggetti presi da le altre Classi."""
        self.Utente = Utente()  # Oggetto Utente
        self.Password = Password()  # Oggetto GeneratorePassword
        self.Email = Email()  # Oggetto ConvalidaEmail
        self.Sito_web = Sito_Web()  # Oggetto ConvalidaSitoWeb

    def crea_credenziali_utente(self):
        """Crea le credenziali dell'utente."""
        # Chiedi l'email dell'utente
        self.Utente.email = self.Email.valida()

        # Chiedi il sito web
        self.Utente.sito_web = self.Sito_web.valida()

        # Chiedi la lunghezza della password e genera la password
        lunghezza = self.Password.valida()  
        self.Utente.password = self.Password.genera(lunghezza) 
         
    def visualizza_credenziali(self):
        """Visualizza le credenziali finali."""
        print("\n" * 80)
        print(colored(f"Ecco le credenziali!", 'green'))
        print("\n" * 3)
        # Colorazione delle credenziali
        print(colored(f"Email:    {self.Utente.email}", 'yellow'))
        print(colored(f"Password: {self.Utente.password}", 'red'))
        print(colored(f"Sito Web: {self.Utente.sito_web}", 'blue'))
        print("\n" * 1)

if __name__ == "__main__":
    credenziali_utente = Credenziali_Utente()
    credenziali_utente.crea_credenziali_utente()
    credenziali_utente.visualizza_credenziali()
