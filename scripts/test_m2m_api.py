#!/usr/bin/env python3
"""
Script di esplorazione per le API Machine-to-Machine di normattiva.it

Questo script implementa i test della Fase 1 descritti in docs/M2M_API_EVALUATION.md

Usage:
    python scripts/test_m2m_api.py
    python scripts/test_m2m_api.py --verbose
    python scripts/test_m2m_api.py --save-responses
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import requests
from typing import Dict, Any, Optional

# API Configuration
M2M_API_BASE_URL = "https://api.normattiva.it/t/normattiva.api/bff-mobile/v1/api/v1"
DETTAGLIO_ATTO_ENDPOINT = f"{M2M_API_BASE_URL}/atto/dettaglio-atto"

# Test cases - esempi di atti da testare
TEST_CASES = [
    {
        "name": "Legge Stanca (2004)",
        "params": {
            "dataGU": "2004-01-17",
            "codiceRedazionale": "004G0015",
            "versione": 0
        },
        "expected": {
            "tipo": "LEGGE",
            "numero": "4",
            "anno": 2004
        }
    },
    {
        "name": "Decreto Dignità (2018)",
        "params": {
            "dataGU": "2018-07-13",
            "codiceRedazionale": "018G00112",
            "versione": 0
        },
        "expected": {
            "tipo": "DECRETO-LEGGE",
            "numero": "87",
            "anno": 2018
        }
    },
    {
        "name": "CAD - Codice Amministrazione Digitale (2005)",
        "params": {
            "dataGU": "2005-05-16",
            "codiceRedazionale": "005G0104",
            "versione": 0
        },
        "expected": {
            "tipo": "DECRETO LEGISLATIVO",
            "numero": "82",
            "anno": 2005
        }
    }
]


class M2MAPITester:
    """Tester per API M2M di normattiva.it"""

    def __init__(self, verbose: bool = False, save_responses: bool = False):
        self.verbose = verbose
        self.save_responses = save_responses
        self.session = requests.Session()
        self.results = []
        self.responses_dir = Path("test_data/m2m_responses")

        if save_responses:
            self.responses_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str, level: str = "INFO"):
        """Log con colori per terminale"""
        colors = {
            "INFO": "\033[94m",    # Blue
            "SUCCESS": "\033[92m", # Green
            "WARNING": "\033[93m", # Yellow
            "ERROR": "\033[91m",   # Red
            "RESET": "\033[0m"
        }

        color = colors.get(level, colors["INFO"])
        reset = colors["RESET"]

        if self.verbose or level in ["SUCCESS", "ERROR", "WARNING"]:
            print(f"{color}[{level}]{reset} {message}")

    def test_endpoint_basic(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test 1: Verifica endpoint base

        Returns:
            Dict con risultati del test
        """
        self.log(f"\n{'='*60}")
        self.log(f"Testing: {test_case['name']}", "INFO")
        self.log(f"{'='*60}")

        result = {
            "test_name": test_case['name'],
            "params": test_case['params'],
            "success": False,
            "status_code": None,
            "error": None,
            "response_data": None,
            "headers": None,
            "timing_ms": None
        }

        try:
            # Misura timing
            start_time = datetime.now()

            self.log(f"POST {DETTAGLIO_ATTO_ENDPOINT}")
            self.log(f"Payload: {json.dumps(test_case['params'], indent=2)}")

            response = self.session.post(
                DETTAGLIO_ATTO_ENDPOINT,
                json=test_case['params'],
                headers={'Content-Type': 'application/json'},
                timeout=30
            )

            end_time = datetime.now()
            timing_ms = (end_time - start_time).total_seconds() * 1000

            result['status_code'] = response.status_code
            result['timing_ms'] = timing_ms
            result['headers'] = dict(response.headers)

            self.log(f"Status Code: {response.status_code}")
            self.log(f"Timing: {timing_ms:.2f}ms")

            # Analizza risposta
            if response.status_code == 200:
                try:
                    data = response.json()
                    result['response_data'] = data
                    result['success'] = True

                    self.log("✅ Response received successfully", "SUCCESS")

                    if self.verbose:
                        self.log(f"Response preview:\n{json.dumps(data, indent=2, ensure_ascii=False)[:500]}...")

                    # Salva risposta completa se richiesto
                    if self.save_responses:
                        filename = f"{test_case['params']['codiceRedazionale']}_{test_case['params']['versione']}.json"
                        filepath = self.responses_dir / filename
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        self.log(f"Response saved to: {filepath}")

                except json.JSONDecodeError as e:
                    result['error'] = f"Invalid JSON response: {e}"
                    self.log(f"❌ Invalid JSON response: {e}", "ERROR")

            elif response.status_code == 401:
                result['error'] = "Authentication required"
                self.log("🔐 Authentication required (401)", "WARNING")

            elif response.status_code == 403:
                result['error'] = "Access forbidden"
                self.log("🚫 Access forbidden (403) - May require API key", "ERROR")

            elif response.status_code == 429:
                result['error'] = "Rate limit exceeded"
                retry_after = response.headers.get('Retry-After', 'unknown')
                self.log(f"⏱️  Rate limit exceeded (429) - Retry after: {retry_after}", "WARNING")

            elif response.status_code == 404:
                result['error'] = "Endpoint not found"
                self.log("❌ Endpoint not found (404) - API may have changed", "ERROR")

            else:
                result['error'] = f"Unexpected status code: {response.status_code}"
                self.log(f"⚠️  Unexpected status: {response.status_code}", "WARNING")
                if self.verbose:
                    self.log(f"Response body: {response.text[:500]}")

            # Analizza headers interessanti
            self._analyze_headers(response.headers)

        except requests.exceptions.Timeout:
            result['error'] = "Request timeout"
            self.log("❌ Request timeout", "ERROR")

        except requests.exceptions.ConnectionError as e:
            result['error'] = f"Connection error: {e}"
            self.log(f"❌ Connection error: {e}", "ERROR")

        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            self.log(f"❌ Unexpected error: {e}", "ERROR")

        self.results.append(result)
        return result

    def _analyze_headers(self, headers: Dict[str, str]):
        """Analizza headers di risposta per informazioni utili"""
        interesting_headers = [
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Reset',
            'Retry-After',
            'Content-Type',
            'X-API-Version',
            'Cache-Control',
            'ETag'
        ]

        found_headers = {}
        for header in interesting_headers:
            value = headers.get(header)
            if value:
                found_headers[header] = value

        if found_headers:
            self.log("\nInteresting Headers:")
            for key, value in found_headers.items():
                self.log(f"  {key}: {value}")

    def test_authentication_methods(self):
        """Test 2: Prova diversi metodi di autenticazione"""
        self.log(f"\n{'='*60}")
        self.log("Testing Authentication Methods", "INFO")
        self.log(f"{'='*60}")

        test_params = TEST_CASES[0]['params']

        auth_methods = [
            {"name": "No Auth", "headers": {}},
            {"name": "API Key Header", "headers": {"X-API-Key": "test-key"}},
            {"name": "Bearer Token", "headers": {"Authorization": "Bearer test-token"}},
        ]

        for method in auth_methods:
            self.log(f"\nTrying: {method['name']}")
            headers = {'Content-Type': 'application/json', **method['headers']}

            try:
                response = self.session.post(
                    DETTAGLIO_ATTO_ENDPOINT,
                    json=test_params,
                    headers=headers,
                    timeout=10
                )

                self.log(f"Status: {response.status_code}")

                if response.status_code == 200:
                    self.log(f"✅ {method['name']} works!", "SUCCESS")
                elif response.status_code == 401:
                    self.log(f"🔐 {method['name']} requires authentication", "WARNING")

            except Exception as e:
                self.log(f"Error with {method['name']}: {e}", "ERROR")

    def test_article_filtering(self):
        """Test 3: Verifica filtro articolo specifico"""
        self.log(f"\n{'='*60}")
        self.log("Testing Article Filtering", "INFO")
        self.log(f"{'='*60}")

        base_params = TEST_CASES[0]['params'].copy()

        # Test con e senza idArticolo
        tests = [
            {"name": "Full document", "params": base_params},
            {"name": "Article 1", "params": {**base_params, "idArticolo": 1}},
            {"name": "Article 5", "params": {**base_params, "idArticolo": 5}},
        ]

        for test in tests:
            self.log(f"\nTesting: {test['name']}")
            result = self.test_endpoint_basic({
                "name": test['name'],
                "params": test['params'],
                "expected": {}
            })

            if result['success'] and result['response_data']:
                # Analizza se l'articolo è stato filtrato
                self._analyze_response_structure(result['response_data'], test['name'])

    def test_versioning(self):
        """Test 4: Verifica supporto versioni"""
        self.log(f"\n{'='*60}")
        self.log("Testing Version Support", "INFO")
        self.log(f"{'='*60}")

        base_params = TEST_CASES[0]['params'].copy()

        # Test diverse versioni
        for version in [0, 1, 2]:
            self.log(f"\nTesting version: {version}")
            params = {**base_params, "versione": version}

            result = self.test_endpoint_basic({
                "name": f"Version {version}",
                "params": params,
                "expected": {}
            })

    def _analyze_response_structure(self, data: Dict[str, Any], context: str):
        """Analizza struttura della risposta"""
        self.log(f"\n--- Response Structure Analysis ({context}) ---")

        def print_structure(obj, indent=0):
            prefix = "  " * indent
            if isinstance(obj, dict):
                for key, value in list(obj.items())[:10]:  # Limit to first 10 keys
                    value_type = type(value).__name__
                    if isinstance(value, (dict, list)):
                        self.log(f"{prefix}{key} ({value_type}):")
                        print_structure(value, indent + 1)
                    else:
                        value_preview = str(value)[:50]
                        self.log(f"{prefix}{key}: {value_preview}...")
            elif isinstance(obj, list):
                self.log(f"{prefix}[{len(obj)} items]")
                if obj:
                    print_structure(obj[0], indent + 1)

        print_structure(data)

        # Cerca campi interessanti
        interesting_fields = [
            'xml', 'akomaNtoso', 'contenuto', 'akn',
            'articoli', 'articolo', 'metadata', 'versione',
            'tipo', 'numero', 'anno', 'titolo'
        ]

        found = {}
        def search_fields(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    current_path = f"{path}.{key}" if path else key
                    if key.lower() in [f.lower() for f in interesting_fields]:
                        found[current_path] = type(value).__name__
                    search_fields(value, current_path)
            elif isinstance(obj, list) and obj:
                search_fields(obj[0], f"{path}[0]")

        search_fields(data)

        if found:
            self.log("\nInteresting fields found:")
            for path, value_type in found.items():
                self.log(f"  {path} ({value_type})")

    def generate_report(self):
        """Genera report finale"""
        self.log(f"\n{'='*60}")
        self.log("FINAL REPORT", "SUCCESS")
        self.log(f"{'='*60}")

        total_tests = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        failed = total_tests - successful

        self.log(f"\nTotal tests: {total_tests}")
        self.log(f"✅ Successful: {successful}")
        self.log(f"❌ Failed: {failed}")

        if successful > 0:
            avg_timing = sum(r['timing_ms'] for r in self.results if r['timing_ms']) / successful
            self.log(f"⚡ Average response time: {avg_timing:.2f}ms")

        # Salva report completo
        report_path = Path("test_data/m2m_api_test_report.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": total_tests,
                "successful": successful,
                "failed": failed
            },
            "results": self.results
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        self.log(f"\n📊 Full report saved to: {report_path}", "SUCCESS")

        # Raccomandazioni
        self.log("\n" + "="*60)
        self.log("RECOMMENDATIONS", "INFO")
        self.log("="*60)

        if successful > 0:
            self.log("✅ API M2M sembra funzionante!", "SUCCESS")
            self.log("\nNext steps:")
            self.log("1. Analizzare la struttura delle risposte in test_data/m2m_responses/")
            self.log("2. Verificare se il contenuto XML Akoma Ntoso è presente")
            self.log("3. Documentare il mapping campi in M2M_API_SPECIFICATION.md")
            self.log("4. Procedere con Fase 2: Proof of Concept")
        else:
            self.log("⚠️  API M2M non accessibile", "WARNING")
            self.log("\nPossibili cause:")
            self.log("- Richiede autenticazione (vedere errori 401/403)")
            self.log("- Endpoint cambiato o non pubblico")
            self.log("- Limitazioni di rete/firewall")
            self.log("\nRaccomandazione: Mantenere approccio attuale (HTML scraping)")


def main():
    parser = argparse.ArgumentParser(
        description="Test delle API M2M di normattiva.it",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic test
  python scripts/test_m2m_api.py

  # Verbose output
  python scripts/test_m2m_api.py --verbose

  # Save all responses for analysis
  python scripts/test_m2m_api.py --save-responses

  # Full exploration
  python scripts/test_m2m_api.py --verbose --save-responses --all-tests
        """
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output with detailed logs'
    )

    parser.add_argument(
        '--save-responses',
        action='store_true',
        help='Save all API responses to files for analysis'
    )

    parser.add_argument(
        '--all-tests',
        action='store_true',
        help='Run all exploratory tests (auth, articles, versions)'
    )

    args = parser.parse_args()

    # Inizializza tester
    tester = M2MAPITester(verbose=args.verbose, save_responses=args.save_responses)

    print("""
╔═══════════════════════════════════════════════════════════════╗
║   Normattiva.it M2M API Explorer                              ║
║   Testing Machine-to-Machine API endpoints                    ║
╚═══════════════════════════════════════════════════════════════╝
    """)

    # Test base per tutti i casi
    tester.log("Running basic endpoint tests for all test cases...", "INFO")
    for test_case in TEST_CASES:
        tester.test_endpoint_basic(test_case)

    # Test aggiuntivi se richiesto
    if args.all_tests:
        tester.test_authentication_methods()
        tester.test_article_filtering()
        tester.test_versioning()

    # Genera report finale
    tester.generate_report()

    print("\n✅ Testing completed!")
    print("See test_data/m2m_api_test_report.json for full results")

    # Exit code basato sui risultati
    successful = sum(1 for r in tester.results if r['success'])
    sys.exit(0 if successful > 0 else 1)


if __name__ == "__main__":
    main()
