# Roadmap Phase 5: Documentation, Dashboards, and Deployment

**Goal**: Build a polished documentation site with interactive analytics, SPARQL query examples, and automated CI/CD; host on GitHub Pages.

## 5.1 Documentation site (MkDocs Material)

Structure:

```
docs/
  mkdocs.yml
  index.md                 # Project overview (report-style, not code-docs)
  methodology.md           # How data was collected and validated
  data-model.md            # Ontology walkthrough with diagrams
  season-profiles/         # One page per season with key stats
    s01-borneo.md
    s20-heroes-vs-villains.md
    ...
  query-cookbook.md         # SPARQL examples with results
  api-reference.md         # Python script usage
  changelog.md
  roadmap/
    phase-1-data-foundation.md
    phase-2-deep-research.md
    phase-3-extraction-mapping.md
    phase-4-ontology-refinement.md
    phase-5-docs-deployment.md
```

The site should read more like a research report than API documentation. Each season profile includes a narrative summary, key statistics, and embedded visualizations.

## 5.2 Interactive analytics

### Option A: JupyterLite + Voila (preferred)

JupyterLite runs entirely in the browser (no server needed for GitHub Pages). Notebooks:

1. **Season overview dashboard**: bar charts of viewership, vote margins, days played, idol plays per season
2. **Contestant network**: force-directed graph of who voted for whom across all seasons
3. **Challenge type distribution**: treemap of challenge categories over 50 seasons
4. **Era comparison**: side-by-side metrics for Classic/Modern/New Era
5. **Winner profiles**: radar charts of winner attributes (immunities won, idols played, votes against, etc.)
6. **Tribal Council explorer**: interactive table filtering by season, episode, vote count

### Option B: Static Plotly charts

If JupyterLite proves too complex for GitHub Pages, pre-render Plotly charts as HTML files and embed them in the MkDocs site.

### Implementation

```python
# notebooks/dashboard.py (or .ipynb)
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

# Load all season.json files
seasons = []
for d in sorted(Path("data").iterdir()):
    sf = d / "season.json"
    if sf.exists():
        with open(sf) as f:
            seasons.append(json.load(f))

df = pd.DataFrame([{
    "season": s["season_number"],
    "subtitle": s["subtitle"],
    "winner": s["winner"]["name"],
    "ftc_vote": s["ftc_vote"],
    "num_castaways": s["num_castaways"],
    "num_days": s["num_days"],
    "era": s["era"],
    "prize": s["prize_amount"],
    "num_tribes": len(s.get("tribes", [])),
    "num_mechanics": len(s.get("mechanics", [])),
    "completeness": s.get("data_completeness", "stub"),
} for s in seasons])
```

## 5.3 SPARQL query cookbook

Example queries to include:

### All two-time winners
```sparql
PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name (COUNT(?s) AS ?wins) WHERE {
  GRAPH ?g {
    ?s surv:winner ?w .
    ?w foaf:name ?name .
  }
}
GROUP BY ?name
HAVING (COUNT(?s) > 1)
```

### Seasons with unanimous FTC votes
```sparql
PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>

SELECT ?num ?subtitle ?vote WHERE {
  GRAPH ?g {
    ?s a surv:Season ;
       surv:seasonNumber ?num ;
       surv:subtitle ?subtitle ;
       surv:ftcVote ?vote .
    FILTER(CONTAINS(?vote, "-0"))
  }
}
ORDER BY ?num
```

### All idol plays (when data is filled)
```sparql
PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?season ?episode ?player_name ?played_for_name ?negated WHERE {
  GRAPH ?g {
    ?ep surv:hasTribalCouncil ?tc .
    ?tc surv:hasIdolPlay ?play .
    ?play surv:idolPlayer ?player ;
          surv:idolPlayedFor ?target ;
          surv:votesNegated ?negated .
    ?player foaf:name ?player_name .
    ?target foaf:name ?played_for_name .
    ?ep surv:inSeason ?s .
    ?s surv:seasonNumber ?season .
    ?ep surv:episodeNumber ?episode .
  }
}
ORDER BY ?season ?episode
```

## 5.4 CI/CD (GitHub Actions)

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: make install
      - run: make test
      - run: make expand
      - run: make validate
      - run: make stats

  deploy-docs:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install mkdocs-material
      - run: cd docs && mkdocs build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: docs/site
```

## 5.5 Data download endpoints

The GitHub Pages site should offer direct downloads:

- `output/survivor.trig` (full dataset, TriG format)
- `output/survivor.nq` (full dataset, N-Quads)
- `data/` tree as a zip archive
- Individual season JSON files

## 5.6 Testing strategy

| Test Category | Tool | Coverage |
|---|---|---|
| Data integrity | pytest | All 50 seasons, all episodes |
| JSON-LD expansion | pytest + pyld | Sample expansion per era |
| SHACL conformance | pyshacl | Full dataset |
| SPARQL queries | pytest + rdflib | Cookbook queries return expected results |
| Documentation build | mkdocs build | No broken links |
| CI pipeline | GitHub Actions | End-to-end on every push |

## Completion criteria

Phase 5 is complete when:
- MkDocs site builds and deploys to GitHub Pages
- At least 3 interactive dashboards are functional
- SPARQL cookbook has 10+ working queries
- CI passes on every push
- README links to the live documentation site
