import os
import re
import sys
import json
import requests
from .normattiva_api import is_normattiva_url, is_normattiva_export_url # Per la validazione URL

def lookup_normattiva_url(
    search_query, debug_json=False, auto_select=True, exa_api_key=None
):
    """
    Usa Exa AI API per cercare l'URL normattiva.it corrispondente alla query di ricerca.

    Args:
        search_query (str): La stringa di ricerca naturale (es. "legge stanca")
        debug_json (bool): Se True, mostra il JSON completo della risposta
        auto_select (bool): Se True, seleziona automaticamente il miglior risultato
        exa_api_key (str): Exa API key (se None, usa EXA_API_KEY environment variable)

    Returns:
        str or None: L'URL trovato, oppure None se non trovato o errore
    """
    try:
        # Verifica che l'API key di Exa sia configurata
        if not exa_api_key:
            exa_api_key = os.getenv("EXA_API_KEY")
        if not exa_api_key:
            print("❌ Exa API key non configurata", file=sys.stderr)
            print(
                "   Configura con: --exa-api-key 'your-api-key' oppure export EXA_API_KEY='your-api-key'",
                file=sys.stderr,
            )
            print("   Registrati su: https://exa.ai", file=sys.stderr)
            return None

        # Prepara la richiesta per Exa API
        url = "https://api.exa.ai/search"
        headers = {"x-api-key": exa_api_key, "Content-Type": "application/json"}

        # Payload per Exa API - filtro dominio tramite includeDomains
        payload = {
            "query": search_query,
            "includeDomains": ["normattiva.it"],
            "numResults": 5,
            "type": "auto",
        }

        # Effettua la chiamata API
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code != 200:
            print(
                f"❌ Errore Exa API (HTTP {response.status_code}): {response.text}",
                file=sys.stderr,
            )
            return None

        # Parse JSON response
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            print(f"❌ Errore nel parsing JSON da Exa API: {e}", file=sys.stderr)
            return None

        # Debug: mostra JSON completo se richiesto
        if debug_json:
            print(f"🔍 JSON completo da Exa API:", file=sys.stderr)
            print(json.dumps(data, indent=2, ensure_ascii=False), file=sys.stderr)
            print(file=sys.stderr)

        # Estrai risultati
        results = data.get("results", [])
        if not results:
            print(f"❌ Nessun risultato trovato per: {search_query}", file=sys.stderr)
            return None

        # Debug: mostra tutti i risultati ricevuti solo in debug mode
        if debug_json:
            print(f"🔍 Risultati ricevuti da Exa ({len(results)}):", file=sys.stderr)
            for i, result in enumerate(results, 1):
                url = result.get("url", "N/A")
                title = result.get("title", "N/A")[:100]  # Tronca titolo lungo
                score = result.get("score", "N/A")
                print(f"  [{i}] URL: {url}", file=sys.stderr)
                print(f"      Titolo: {title}...", file=sys.stderr)
                print(f"      Score: {score}", file=sys.stderr)
                print(file=sys.stderr)

        # Logica di selezione migliorata: preferisci URL senza riferimenti ad articoli specifici
        valid_results = []
        query_lower = search_query.lower()

        # Controlla se l'utente vuole un articolo specifico
        import re

        # Riconosce: "articolo 7", "art 7", "art. 7", "articolo 16bis", etc.
        article_match = re.search(
            r"\b(?:articolo|art\.?|art)\s+(\d+(?:\s*(?:bis|ter|quater|quinquies|sexies|septies|octies|novies|decies|vices|tricies|quadragies))?)\b",
            query_lower,
            re.IGNORECASE,
        )
        requested_article = (
            article_match.group(1).replace(" ", "") if article_match else None
        )

        for i, result in enumerate(results):
            url = result.get("url")
            if url and is_normattiva_url(url) and not is_normattiva_export_url(url):
                # Calcola un punteggio di preferenza
                preference_score = 0
                title = result.get("title", "").lower()

                # Skippa risultati con "errore" nel titolo (pagine di errore di normattiva.it)
                if "errore" in title:
                    continue

                # Penalizza URL caricaDettaglioAtto (restituiscono HTML, non XML)
                if "/caricaDettaglioAtto?" in url:
                    preference_score -= 50

                # Bonus forte per URL uri-res/N2Ls (funzionano sempre)
                if "/uri-res/N2Ls?" in url:
                    preference_score += 15

                # Bonus per il primo risultato (probabilmente il più rilevante)
                if i == 0:
                    preference_score += 3
                    # Bonus extra se non è richiesto un articolo specifico
                    if not requested_article:
                        preference_score += 10

                # Logica specifica per articoli richiesti
                if requested_article:
                    # Se l'utente vuole un articolo specifico, dai bonus agli URL che lo contengono
                    if f"~art{requested_article}" in url.lower():
                        preference_score += 20  # Bonus enorme per l'articolo esatto
                    elif "~art" in url:
                        preference_score -= 5  # Penalizza altri articoli
                else:
                    # Se l'utente NON vuole un articolo specifico, penalizza URL con articoli
                    if "~art" in url:
                        preference_score -= 10
                    else:
                        # Bonus extra per URL di leggi complete
                        preference_score += 2

                # Bonus per titoli che sembrano leggi complete
                if any(
                    word in title
                    for word in ["legge", "decreto-legge", "decreto legislativo"]
                ):
                    preference_score += 5

                # Bonus se il titolo contiene parole chiave della query
                query_words = set(query_lower.split())
                title_words = set(title.split())
                common_words = query_words.intersection(title_words)
                if common_words:
                    preference_score += len(common_words) * 2

                # Bonus extra se il titolo contiene la query quasi completa
                if query_lower in title or title in query_lower:
                    preference_score += 10

                # Penalizza titoli che sembrano articoli specifici (solo se non richiesti)
                if not requested_article and any(
                    word in title for word in ["articolo", "art.", "comma"]
                ):
                    preference_score -= 5

                valid_results.append(
                    {
                        "url": url,
                        "title": result.get("title", ""),
                        "score": result.get("score", 0),
                        "preference_score": preference_score,
                        "rank": i + 1,
                    }
                )

        if not valid_results:
            print(
                f"❌ Nessun URL normattiva.it valido trovato nei risultati",
                file=sys.stderr,
            )
            return None

        # Ordina per punteggio di preferenza decrescente prima di mostrare
        valid_results.sort(
            key=lambda x: (x["preference_score"], x["score"]), reverse=True
        )

        # Se auto_select è False, mostra i risultati e chiedi all'utente di scegliere
        if not auto_select:
            print(f"🔍 Risultati trovati per: {search_query}", file=sys.stderr)
            print(
                f"Seleziona il numero del risultato desiderato (1-{len(valid_results)}), o 0 per annullare:",
                file=sys.stderr,
            )
            for i, result in enumerate(valid_results, 1):
                print(f"  [{i}] {result['title'][:80]}...", file=sys.stderr)
                print(f"      URL: {result['url']}", file=sys.stderr)
                print(
                    f"      Preferenza: {result['preference_score']}", file=sys.stderr
                )
                print(file=sys.stderr)

            try:
                choice = int(input("Scelta: ").strip())
                if choice == 0:
                    print("❌ Ricerca annullata dall'utente", file=sys.stderr)
                    return None
                elif 1 <= choice <= len(valid_results):
                    selected = valid_results[choice - 1]
                    print(
                        f"✅ URL selezionato manualmente: {selected['url']}",
                        file=sys.stderr,
                    )
                    return {"url": selected["url"], "title": selected["title"]}
                else:
                    print(f"❌ Scelta non valida: {choice}", file=sys.stderr)
                    return None
            except (ValueError, EOFError, KeyboardInterrupt):
                print("\r❌ Ricerca annullata dall'utente", file=sys.stderr)
                return None

        # Selezione automatica
        # Ordina per punteggio di preferenza decrescente, poi per score Exa
        valid_results.sort(
            key=lambda x: (x["preference_score"], x["score"]), reverse=True
        )

        selected = valid_results[0]

        # Se l'utente non ha specificato un articolo ma il risultato selezionato è un articolo specifico,
        # convertilo automaticamente nella legge completa
        if not requested_article and "~art" in selected["url"]:
            complete_url = selected["url"].split("~art")[0]
            if (
                not debug_json
            ):  # Solo in modalità non-debug mostra il messaggio di conversione
                print(
                    f"🔄 Convertito URL articolo specifico in URL legge completa: {complete_url}",
                    file=sys.stderr,
                )
            selected["url"] = complete_url

        if debug_json:
            print(
                f"✅ URL selezionato automaticamente (preferenza: {selected['preference_score']}, score: {selected['score']}): {selected['url']}",
                file=sys.stderr,
            )
            print(f"   Titolo: {selected['title']}", file=sys.stderr)

        return selected["url"]

    except requests.exceptions.Timeout:
        print("❌ Timeout nella chiamata a Exa API", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di connessione a Exa API: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Errore nella ricerca URL: {e}", file=sys.stderr)
        return None
