# File di Test

Questa directory contiene file di esempio utili per testare il convertitore Akoma Ntoso a Markdown (`akoma2md`).

*   `20050516_005G0104_VIGENZA_20250130.xml`: Un esempio di file XML Akoma Ntoso che può essere utilizzato come input per il tool `akoma2md`.

Per eseguire un test, puoi usare il seguente comando (dalla root del progetto):

```bash
python convert_akomantoso.py test_data/20050516_005G0104_VIGENZA_20250130.xml output.md
```

Questo genererà un file `output.md` nella directory corrente con il contenuto convertito.