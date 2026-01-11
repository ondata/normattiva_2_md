---
layout: default
title: Converti leggi italiane in Markdown AI-ready
---

<!-- Hero Section -->
<section class="bg-gradient-to-br from-blue-600 to-indigo-700 text-white py-20 lg:py-32">
    <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
            <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6">
                Converti le leggi italiane in testo semplice e strutturato per le intelligenze artificiali
            </h1>
            <p class="text-xl md:text-2xl text-blue-100 mb-8 leading-relaxed">
                Trasforma i contenuti di normattiva.it in formato Markdown AI-ready
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-12">
                <a href="#installation" class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition shadow-lg hover:shadow-xl transform hover:-translate-y-1">
                    Inizia ora
                </a>
                <a href="https://github.com/ondata/normattiva_2_md" target="_blank" class="bg-blue-500 bg-opacity-30 backdrop-blur-sm border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-opacity-40 transition">
                    <span class="flex items-center gap-2">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
                        </svg>
                        Vedi su GitHub
                    </span>
                </a>
                <a href="https://deepwiki.com/ondata/normattiva_2_md" target="_blank" class="bg-purple-500 bg-opacity-30 backdrop-blur-sm border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-opacity-40 transition">
                    <span class="flex items-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                        </svg>
                        DeepWiki
                    </span>
                </a>
            </div>
            <div class="bg-gray-900 bg-opacity-50 backdrop-blur-sm rounded-lg p-6 max-w-2xl mx-auto">
                <div class="text-left">
                    <div class="text-sm text-blue-200 mb-2">Quick Install</div>
                    <pre class="text-left"><code class="language-bash">pip install normattiva2md
normattiva2md "https://normattiva.it/..." output.md</code></pre>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Features Grid -->
<section id="features" class="py-20 bg-white">
    <div class="container mx-auto px-4">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Caratteristiche Principali</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Tutto ciò che serve per integrare le normative italiane nei tuoi sistemi AI
            </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Feature 1 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Supporto URL diretto</h3>
                <p class="text-gray-600 mb-4">
                    Processa direttamente URL da normattiva.it senza download manuale. Auto-detection e conversione immediata.
                </p>
                <div class="text-sm text-gray-500">
                    <code class="bg-gray-100 px-2 py-1 rounded">normattiva2md "URL"</code>
                </div>
            </div>

            <!-- Feature 2 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Ricerca in linguaggio naturale</h3>
                <p class="text-gray-600 mb-4">
                    Trova leggi per contenuto, non solo per riferimento normativo. Ricerca basata su <a href="https://docs.exa.ai/reference/getting-started" target="_blank" class="text-indigo-600 underline">Exa AI</a>.
                </p>
                <div class="text-sm text-gray-500">
                    <code class="bg-gray-100 px-2 py-1 rounded">-s "legge Stanca accessibilità"</code>
                </div>
            </div>

            <!-- Feature 3 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Riferimenti incrociati</h3>
                <p class="text-gray-600 mb-4">
                    Link automatici a leggi citate. Scarica automaticamente tutte le normative referenziate.
                </p>
                <div class="text-sm text-gray-500">
                    <code class="bg-gray-100 px-2 py-1 rounded">--with-references</code>
                </div>
            </div>

            <!-- Feature 4 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Ottimizzato per LLM</h3>
                <p class="text-gray-600 mb-4">
                    Output con YAML frontmatter e gerarchia book-style (H1→H4). Fino al 60% di riduzione token rispetto a XML.
                </p>
                <div class="text-sm text-gray-500">
                    Metadata + Markdown pulito
                </div>
            </div>

            <!-- Feature 5 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Estrazione articoli</h3>
                <p class="text-gray-600 mb-4">
                    Estrai singoli articoli specifici da una legge usando la sintassi ~art. Perfetto per analisi mirate.
                </p>
                <div class="text-sm text-gray-500">
                    <code class="bg-gray-100 px-2 py-1 rounded">~art3, ~art16bis</code>
                </div>
            </div>

            <!-- Feature 6 -->
            <div class="bg-white border border-gray-200 rounded-xl p-6 hover-lift">
                <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4" aria-hidden="true">
                    <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
                    </svg>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">Pronto per la produzione</h3>
                <p class="text-gray-600 mb-4">
                    Security features, CI/CD con GitHub Actions, binary precompilati. Testato e documentato.
                </p>
                
            </div>
        </div>
    </div>
</section>

<!-- API Usage -->
<section id="api" class="py-20 bg-white">
    <div class="container mx-auto px-4">
        <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Uso delle API</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Dalla v2.1 puoi integrare normattiva2md direttamente nei tuoi script Python
            </p>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
            <div class="space-y-6">
                <div class="bg-white border border-gray-200 rounded-xl p-6">
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">API programmabile</h3>
                    <p class="text-gray-600 mb-4">
                        Moduli dedicati per conversione, modelli dati e gestione errori
                        (<code class="bg-gray-100 px-2 py-1 rounded">api.py</code>,
                        <code class="bg-gray-100 px-2 py-1 rounded">models.py</code>,
                        <code class="bg-gray-100 px-2 py-1 rounded">exceptions.py</code>).
                    </p>
                    <div class="text-sm text-gray-500">
                        Risultati strutturati con <code class="bg-gray-100 px-2 py-1 rounded">ConversionResult</code>
                        e <code class="bg-gray-100 px-2 py-1 rounded">SearchResult</code>
                    </div>
                </div>
                <div class="bg-white border border-gray-200 rounded-xl p-6">
                    <h3 class="text-xl font-semibold text-gray-900 mb-2">Funzioni standalone</h3>
                    <p class="text-gray-600 mb-4">
                        Tre entry point per partire subito: <code class="bg-gray-100 px-2 py-1 rounded">convert_url()</code>,
                        <code class="bg-gray-100 px-2 py-1 rounded">convert_xml()</code> e
                        <code class="bg-gray-100 px-2 py-1 rounded">search_law()</code>.
                    </p>
                    <div class="text-sm text-gray-500">
                        Ideale per pipeline, notebook e integrazioni rapide
                    </div>
                </div>
            </div>
            <div class="bg-gray-900 rounded-xl overflow-hidden shadow-lg">
                <pre class="text-sm"><code class="language-python">from normattiva2md import convert_url, convert_xml, search_law

# Conversione da URL
result = convert_url(
    "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53",
    article="3"
)
print(result.markdown[:500])

# Conversione da XML locale
xml_result = convert_xml("documento.xml")

# Ricerca con linguaggio naturale
hits = search_law("legge stanca accessibilità")
for hit in hits[:3]:
    print(hit.title, hit.urn)</code></pre>
            </div>
        </div>
    </div>
</section>

<!-- Demo: Before/After -->
<section id="demo" class="py-20 bg-gray-50">
    <div class="container mx-auto px-4">
        <div class="text-center mb-16">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Vedi la differenza</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Da XML Akoma Ntoso a Markdown pulito e LLM-friendly
            </p>
        </div>
        <div class="max-w-6xl mx-auto">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- Before: XML -->
                <div>
                    <div class="bg-red-50 border-l-4 border-red-500 px-4 py-2 mb-4">
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                            <span class="font-semibold text-red-700">XML Akoma Ntoso</span>
                        </div>
                    </div>
                    <div class="bg-gray-900 rounded-lg overflow-hidden">
                        <pre class="text-sm"><code class="language-xml">&lt;article eId="art_1"&gt;
  &lt;num&gt;1&lt;/num&gt;
  &lt;heading&gt;Definizioni&lt;/heading&gt;
  &lt;paragraph eId="art_1__para_1"&gt;
    &lt;num&gt;1&lt;/num&gt;
    &lt;list eId="art_1__para_1.__list_1"&gt;
      &lt;intro&gt;
        &lt;p&gt;Ai fini del presente codice
        si intende per:&lt;/p&gt;
      &lt;/intro&gt;
      &lt;point eId="art_1__para_1.__point_c"&gt;
        &lt;num&gt;c)&lt;/num&gt;
        &lt;content&gt;
          &lt;p&gt;carta d'identita' elettronica:
          il documento d'identita' munito di
          elementi per l'identificazione fisica
          del titolare rilasciato su supporto
          informatico dalle amministrazioni
          comunali con la prevalente finalita'
          di dimostrare l'identita' anagrafica
          del suo titolare;&lt;/p&gt;
        &lt;/content&gt;
      &lt;/point&gt;
    &lt;/list&gt;
  &lt;/paragraph&gt;
&lt;/article&gt;</code></pre>
                    </div>
                    <div class="mt-4 space-y-2 text-sm text-gray-600">
                        <div class="flex items-center gap-2">
                            <span class="text-red-500">❌</span>
                            <span>Verboso e difficile da leggere</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-red-500">❌</span>
                            <span>Alto consumo di token per LLM</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-red-500">❌</span>
                            <span>Richiede parsing XML complesso</span>
                        </div>
                    </div>
                </div>

                <!-- After: Markdown -->
                <div>
                    <div class="bg-green-50 border-l-4 border-green-500 px-4 py-2 mb-4">
                        <div class="flex items-center gap-2">
                            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                            </svg>
                            <span class="font-semibold text-green-700">Markdown LLM-ready</span>
                        </div>
                    </div>
                    <div class="bg-gray-900 rounded-lg overflow-hidden">
                        <pre class="text-sm"><code class="language-markdown">---
title: Codice dell'amministrazione digitale
url: https://www.normattiva.it/...
dataGU: 20050516
codiceRedaz: 005G0104
dataVigenza: 20250130
---

# Art. 1 - Definizioni

1. Ai fini del presente codice si
   intende per:

   - c) carta d'identita' elettronica:
     il documento d'identita' munito di
     elementi per l'identificazione fisica
     del titolare rilasciato su supporto
     informatico dalle amministrazioni
     comunali con la prevalente finalita'
     di dimostrare l'identita' anagrafica
     del suo titolare;</code></pre>
                    </div>
                    <div class="mt-4 space-y-2 text-sm text-gray-600">
                        <div class="flex items-center gap-2">
                            <span class="text-green-500">✅</span>
                            <span>Pulito e immediatamente leggibile</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-green-500">✅</span>
                            <span>~60% riduzione token rispetto a XML</span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-green-500">✅</span>
                            <span>Metadata YAML + gerarchia H1-H4</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
                <p class="text-lg text-gray-700">
                    <span class="font-semibold text-blue-600">Risultato:</span>
                    Token ottimizzati per LLM, struttura book-style perfetta per RAG, metadata completi per tracciabilità
                </p>
            </div>
        </div>
    </div>
</section>

<!-- Installation -->
<section id="installation" class="py-20 bg-white">
    <div class="container mx-auto px-4">
        <div class="text-center mb-12">
            <h2 class="text-4xl font-bold text-gray-900 mb-4">Inizia in 60 secondi</h2>
            <p class="text-xl text-gray-600 max-w-2xl mx-auto">
                Scegli il tuo metodo di installazione preferito
            </p>
        </div>
        <div class="max-w-4xl mx-auto">
            <!-- Tabs -->
            <div class="flex border-b border-gray-300 mb-6" role="tablist" aria-label="Metodi di installazione">
                <button class="tab-button active px-6 py-3 font-medium text-gray-600" data-tab="tab-pip" role="tab" aria-selected="true" aria-controls="tab-pip" id="tab-pip-button">
                    pip install
                </button>
                <button class="tab-button px-6 py-3 font-medium text-gray-600" data-tab="tab-uv" role="tab" aria-selected="false" aria-controls="tab-uv" id="tab-uv-button">
                    uv tool
                </button>
                <button class="tab-button px-6 py-3 font-medium text-gray-600" data-tab="tab-source" role="tab" aria-selected="false" aria-controls="tab-source" id="tab-source-button">
                    From Source
                </button>
            </div>

            <!-- Tab Content: pip -->
            <div id="tab-pip" class="tab-content active" role="tabpanel" aria-labelledby="tab-pip-button">
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Installazione con pip</h3>
                    <p class="text-gray-600 mb-6">
                        Il metodo più comune. Funziona con Python 3.7+
                    </p>
                    <div class="bg-gray-900 rounded-lg overflow-hidden mb-6">
                        <pre><code class="language-bash"># Installa da PyPI
pip install normattiva2md

# Verifica installazione
normattiva2md --version

# Uso base: da URL normattiva.it
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2022;53" output.md

# Uso base: da file XML locale
normattiva2md input.xml output.md

# Output a stdout (per piping)
normattiva2md input.xml > output.md</code></pre>
                    </div>
                </div>
            </div>

            <!-- Tab Content: uv -->
            <div id="tab-uv" class="tab-content" role="tabpanel" aria-labelledby="tab-uv-button">
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Installazione con uv</h3>
                    <p class="text-gray-600 mb-6">
                        Metodo raccomandato per gestione tool isolati. Richiede <a href="https://github.com/astral-sh/uv" target="_blank" class="text-blue-600 hover:underline">uv</a>
                    </p>
                    <div class="bg-gray-900 rounded-lg overflow-hidden mb-6">
                        <pre><code class="language-bash"># Installa uv (se non già installato)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installa normattiva2md come tool
uv tool install normattiva2md

# Uso
normattiva2md "URL" output.md</code></pre>
                    </div>
                </div>
            </div>

            <!-- Tab Content: Source -->
            <div id="tab-source" class="tab-content" role="tabpanel" aria-labelledby="tab-source-button">
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h3 class="text-2xl font-bold text-gray-900 mb-4">Installazione da sorgenti</h3>
                    <p class="text-gray-600 mb-6">
                        Per sviluppatori o per contribuire al progetto
                    </p>
                    <div class="bg-gray-900 rounded-lg overflow-hidden mb-6">
                        <pre><code class="language-bash"># Clone repository
git clone https://github.com/ondata/normattiva_2_md.git
cd normattiva_2_md

# Installa in development mode
pip install -e .

# Oppure installa direttamente
pip install .

# Usa normalmente
normattiva2md input.xml output.md</code></pre>
                    </div>
                </div>
            </div>

            <!-- Quick Examples -->
            <div class="mt-12 bg-white rounded-lg shadow-lg p-8">
                <h3 class="text-2xl font-bold text-gray-900 mb-6">Esempi Rapidi</h3>
                <div class="space-y-6">
                    <!-- Example 1 -->
                    <div>
                        <div class="text-sm font-semibold text-gray-500 mb-2">Conversione da URL</div>
                        <div class="bg-gray-900 rounded-lg overflow-hidden">
                            <pre><code class="language-bash">normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82" cad.md</code></pre>
                        </div>
                    </div>

                    <!-- Example 2 -->
                    <div>
                        <div class="text-sm font-semibold text-gray-500 mb-2">Ricerca con AI (richiede <a href="https://docs.exa.ai/reference/getting-started" target="_blank" class="text-blue-600 hover:underline">Exa API key</a>)</div>
                        <div class="bg-gray-900 rounded-lg overflow-hidden">
                            <pre><code class="language-bash"># Configura API key
export EXA_API_KEY='your-api-key'

# Ricerca in linguaggio naturale
normattiva2md -s "legge stanca accessibilità" output.md

# Debug mode con selezione interattiva
normattiva2md -s "GDPR italiano" output.md --debug-search</code></pre>
                        </div>
                    </div>

                    <!-- Example 3 -->
                    <div>
                        <div class="text-sm font-semibold text-gray-500 mb-2">Estrazione articolo specifico</div>
                        <div class="bg-gray-900 rounded-lg overflow-hidden">
                            <pre><code class="language-bash"># Estrai solo articolo 3
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82~art3" articolo3.md

# Articoli con bis/ter
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82~art6bis" art6bis.md</code></pre>
                        </div>
                    </div>

                    <!-- Example 4 -->
                    <div>
                        <div class="text-sm font-semibold text-gray-500 mb-2">Download con riferimenti</div>
                        <div class="bg-gray-900 rounded-lg overflow-hidden">
                            <pre><code class="language-bash"># Scarica legge + tutte le leggi citate
normattiva2md "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2005-03-07;82" output.md --with-references</code></pre>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Documentation Links -->
            <div class="mt-8 text-center">
                <p class="text-gray-600 mb-4">
                    Hai bisogno di aiuto? Consulta la documentazione completa
                </p>
                <div class="flex flex-wrap justify-center gap-4">
                    <a href="https://github.com/ondata/normattiva_2_md/blob/main/README.md" target="_blank" class="inline-flex items-center gap-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                        </svg>
                        Documentazione
                    </a>
                    <a href="https://github.com/ondata/normattiva_2_md/blob/main/docs/API_REFERENCE.md" target="_blank" class="inline-flex items-center gap-2 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                        </svg>
                        API Reference
                    </a>
                    <a href="https://pypi.org/project/normattiva2md/" target="_blank" class="inline-flex items-center gap-2 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
                        </svg>
                        PyPI Package
                    </a>
                    <a href="https://github.com/ondata/normattiva_2_md/issues" target="_blank" class="inline-flex items-center gap-2 bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"></path>
                        </svg>
                        Segnala Issue
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Riconoscimento Normattiva -->
<section class="py-16 bg-gray-50">
    <div class="container mx-auto px-4">
        <div class="max-w-3xl mx-auto text-center">
            <div class="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-6">
                <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
            </div>
            <h2 class="text-3xl font-bold text-gray-900 mb-4">Possibile grazie a Normattiva</h2>
            <p class="text-lg text-gray-600 mb-6 leading-relaxed">
                Questo progetto si basa sul servizio di <strong>Normattiva</strong>, che rende disponibili le norme italiane in formato XML strutturato (Akoma Ntoso). Senza questo normattiva2md non sarebbe stato possibile.
            </p>
            <p class="text-gray-600 mb-6">
                Normattiva eroga un servizio completo di informazione sulle leggi italiane, garantendo accessibilità e trasparenza normativa per tutte le persone.
            </p>
            <a href="https://www.normattiva.it/" target="_blank" class="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-semibold transition">
                <span>Visita Normattiva.it</span>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
                </svg>
            </a>
        </div>
    </div>
</section>

<!-- CTA Final -->
<section class="py-20 bg-gradient-to-br from-blue-600 to-indigo-700 text-white">
    <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-6">
            Pronto per iniziare?
        </h2>
        <p class="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Inizia a convertire le normative italiane in formato AI-ready in meno di un minuto
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a href="#installation" class="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-50 transition shadow-lg">
                Installa ora
            </a>
            <a href="https://github.com/ondata/normattiva_2_md" target="_blank" class="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:bg-opacity-20 transition">
                Vedi su GitHub
            </a>
        </div>
    </div>
</section>
