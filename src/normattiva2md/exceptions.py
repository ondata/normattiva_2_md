"""
Custom exceptions per normattiva2md.

Gerarchia:
    Exception
    └── Normattiva2MDError (base)
        ├── InvalidURLError
        ├── XMLFileNotFoundError
        ├── APIKeyError
        └── ConversionError

Strategia gestione errori:
- Errori GRAVI → Eccezioni (URL invalido, file non esiste)
- Errori SOFT → None (articolo non trovato, ricerca senza risultati)
"""


class Normattiva2MDError(Exception):
    """
    Eccezione base per tutti gli errori di normattiva2md.

    Tutti gli errori specifici del package derivano da questa classe.
    Permette di catturare tutti gli errori del package con un singolo except.

    Examples:
        >>> try:
        ...     result = convert_url("https://...")
        ... except Normattiva2MDError as e:
        ...     print(f"Errore normattiva2md: {e}")
    """

    pass


class InvalidURLError(Normattiva2MDError):
    """
    Sollevata quando URL non è valido o sicuro.

    Casi:
    - URL non è HTTPS
    - Dominio non è normattiva.it
    - URL contiene path traversal
    - URL malformato

    Examples:
        >>> from normattiva2md import convert_url, InvalidURLError
        >>>
        >>> try:
        ...     result = convert_url("http://invalid-domain.com/...")
        ... except InvalidURLError as e:
        ...     print(f"URL non valido: {e}")
    """

    pass


class XMLFileNotFoundError(Normattiva2MDError):
    """
    Sollevata quando file XML locale non esiste.

    Nota: Usa nome diverso da built-in FileNotFoundError per evitare
    conflitti e mantenere consistenza con gerarchia Normattiva2MDError.

    Examples:
        >>> from normattiva2md import convert_xml, XMLFileNotFoundError
        >>>
        >>> try:
        ...     result = convert_xml("/path/non/esistente.xml")
        ... except XMLFileNotFoundError as e:
        ...     print(f"File non trovato: {e}")
    """

    pass


class APIKeyError(Normattiva2MDError):
    """
    Sollevata quando Exa API key mancante o invalida.

    Casi:
    - API key non configurata (né ENV né parametro)
    - API key invalida (HTTP 401/403 da Exa)
    - API key scaduta

    Examples:
        >>> from normattiva2md import search_law, APIKeyError
        >>>
        >>> try:
        ...     results = search_law("legge stanca")
        ... except APIKeyError as e:
        ...     print(f"Configura EXA_API_KEY: {e}")
    """

    pass


class ConversionError(Normattiva2MDError):
    """
    Sollevata quando errore durante conversione XML → Markdown.

    Casi:
    - XML malformato/corrotto
    - Parsing XML fallito
    - Struttura XML non riconosciuta
    - Errore I/O durante conversione

    Examples:
        >>> from normattiva2md import convert_xml, ConversionError
        >>>
        >>> try:
        ...     result = convert_xml("corrupted.xml")
        ... except ConversionError as e:
        ...     print(f"Errore conversione: {e}")
    """

    pass
