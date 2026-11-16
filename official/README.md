# Official files fetched for Band Atlas

Fetched by `.github/workflows/fetch-official.yml` from the addresses in `manifest.json`. Raw files: release `official-data`.

| id | country | what | last result | fetched | file date |
|---|---|---|---|---|---|
| `fr-anfr-5w` | FR | Installations radioélectriques de plus de 5 watts, whole country (monthly ZIPs: stations, transmitters with their system such as '5G NR 3500', operators); summarised by tools/parse_anfr.py | ok | 2026-11-16 |  |
| `uk-ofcom-cn2025` | GB | Connected Nations 2025 data downloads: the mobile coverage files linked from the page | failed: HTTPError: HTTP Error 403: Forbidden | 2026-11-16 |  |
| `eu-eco-report03` | EU | ECO Report 03, the licensing of mobile bands in CEPT (PDF; a new edition changes the checksum) | ok | 2026-11-16 | Mon, 24 Aug 2026 13:05:35 GMT |
| `us-fcc-nbm-probe` | US | National Broadband Map: probe only (the data download needs choosing a provider; this records whether the listing answers) | failed: HTTPError: HTTP Error 403: Forbidden | 2026-11-16 |  |
