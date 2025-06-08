"""Application constants."""
from enum import Enum


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MessageTemplate:
    CHECKING_SOURCE = "🔍 Sprawdzanie ofert z {source}..."
    NEW_OFFERS_SENT = "✅ Wysłano {count} nowych ofert z {source}."
    ERROR_FETCHING = "❌ Błąd podczas pobierania ofert z {source}: {error}"
    DAILY_RESET = "🔄 Reset listy wysłanych ofert (nowy dzień)."
    BOT_LOGGED_IN = "[BOT] Zalogowano jako {user}"
    BOT_STARTED = "[BOT] Rozpoczynam automatyczne wysyłanie ofert."

    OFFER_MESSAGE = (
        "**{title}**\n"
        "💸 Cena: {price}\n"
        "{publication_time}"
        "🔗 Link: {url}"
    )
    PUBLICATION_TIME_LINE = "⏰ Czas publikacji: {time}\n"


class ScraperName(str, Enum):
    """Scraper names."""
    OTOMOTO = "Otomoto"
    LENTO = "Lento"
    AUTOPLAC = "Autoplac"
    SPRZEDAJEMY = "Sprzedajemy"


class ErrorMessage:
    """Error messages."""
    NO_SEARCH_RESULTS = "Nie znaleziono wyników wyszukiwania."
    INVALID_RESPONSE = "Nieprawidłowa odpowiedź z serwera."
    CONNECTION_ERROR = "Błąd połączenia z serwerem."
    PARSING_ERROR = "Błąd parsowania danych."