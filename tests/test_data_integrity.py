#!/usr/bin/env python3
"""
tests/test_data_integrity.py

Validates the generated JSON data files, JSON-LD context resolution,
RDF expansion, SHACL conformance, and example SPARQL queries.
"""

import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
CONTEXT_DIR = ROOT / "context"
ONTOLOGY_DIR = ROOT / "ontology"
SHAPES_DIR = ROOT / "shapes"


# ════════════════════════════════════════════════════════════════════
# Fixtures
# ════════════════════════════════════════════════════════════════════

@pytest.fixture(scope="session")
def season_dirs():
    return sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])


@pytest.fixture(scope="session")
def all_season_jsons(season_dirs):
    results = []
    for sd in season_dirs:
        sf = sd / "season.json"
        if sf.exists():
            with open(sf) as f:
                results.append((sd.name, json.load(f)))
    return results


@pytest.fixture(scope="session")
def season_context():
    with open(CONTEXT_DIR / "season.jsonld") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def episode_context():
    with open(CONTEXT_DIR / "episode.jsonld") as f:
        return json.load(f)


# ════════════════════════════════════════════════════════════════════
# Structural tests
# ════════════════════════════════════════════════════════════════════

class TestDirectoryStructure:
    def test_data_dir_exists(self):
        assert DATA_DIR.exists(), "data/ directory missing"

    def test_fifty_seasons(self, season_dirs):
        assert len(season_dirs) == 50, (
            f"Expected 50 season dirs, found {len(season_dirs)}"
        )

    def test_each_season_has_season_json(self, season_dirs):
        missing = [d.name for d in season_dirs
                   if not (d / "season.json").exists()]
        assert not missing, f"Missing season.json in: {missing}"

    def test_each_season_has_episodes(self, season_dirs):
        empty = []
        for d in season_dirs:
            eps = list(d.glob("e*.json"))
            if not eps:
                empty.append(d.name)
        assert not empty, f"No episode files in: {empty}"

    def test_contexts_exist(self):
        for name in ["season.jsonld", "episode.jsonld", "provenance.jsonld"]:
            assert (CONTEXT_DIR / name).exists(), f"Missing {name}"

    def test_ontology_exists(self):
        assert (ONTOLOGY_DIR / "survivor.ttl").exists()

    def test_shapes_exist(self):
        assert (SHAPES_DIR / "survivor-shapes.ttl").exists()


# ════════════════════════════════════════════════════════════════════
# JSON data validation
# ════════════════════════════════════════════════════════════════════

class TestSeasonData:
    def test_season_numbers_sequential(self, all_season_jsons):
        nums = [s["season_number"] for _, s in all_season_jsons]
        assert nums == list(range(1, 51)), (
            f"Season numbers not 1-50: {nums}"
        )

    def test_all_seasons_have_winners(self, all_season_jsons):
        no_winner = [(name, s["season_number"])
                     for name, s in all_season_jsons
                     if not s.get("winner")]
        assert not no_winner, f"Seasons without winners: {no_winner}"

    def test_all_seasons_have_era(self, all_season_jsons):
        valid_eras = {"classic", "modern", "new_era"}
        bad = [(name, s.get("era"))
               for name, s in all_season_jsons
               if s.get("era") not in valid_eras]
        assert not bad, f"Invalid eras: {bad}"

    def test_era_boundaries(self, all_season_jsons):
        for _, s in all_season_jsons:
            n = s["season_number"]
            era = s["era"]
            if n <= 20:
                assert era == "classic", f"S{n} should be classic"
            elif n <= 40:
                assert era == "modern", f"S{n} should be modern"
            else:
                assert era == "new_era", f"S{n} should be new_era"

    def test_all_have_tribes(self, all_season_jsons):
        no_tribes = [(name, s["season_number"])
                     for name, s in all_season_jsons
                     if not s.get("tribes")]
        assert not no_tribes, f"Seasons without tribes: {no_tribes}"

    def test_ftc_vote_present(self, all_season_jsons):
        missing = [(name, s["season_number"])
                   for name, s in all_season_jsons
                   if not s.get("ftc_vote")]
        assert not missing, f"Missing FTC vote: {missing}"

    def test_prize_amounts(self, all_season_jsons):
        for _, s in all_season_jsons:
            prize = s.get("prize_amount", 0)
            assert prize in (1000000, 2000000), (
                f"S{s['season_number']} unexpected prize: {prize}"
            )

    def test_new_era_26_days(self, all_season_jsons):
        for _, s in all_season_jsons:
            if s["era"] == "new_era":
                assert s["num_days"] == 26, (
                    f"S{s['season_number']} New Era should be 26 days"
                )


class TestEpisodeData:
    def test_episode_numbers_sequential(self, season_dirs):
        for sd in season_dirs:
            eps = sorted(sd.glob("e*.json"))
            nums = []
            for ep_file in eps:
                with open(ep_file) as f:
                    doc = json.load(f)
                nums.append(doc["episode_number"])
            expected = list(range(1, len(nums) + 1))
            assert nums == expected, (
                f"{sd.name}: episode numbers {nums} != {expected}"
            )

    def test_episode_has_season_ref(self, season_dirs):
        for sd in season_dirs:
            ep1 = sd / "e01.json"
            if ep1.exists():
                with open(ep1) as f:
                    doc = json.load(f)
                assert doc.get("season"), (
                    f"{sd.name}/e01.json missing season reference"
                )

    def test_episode_stubs_are_valid_json(self, season_dirs):
        for sd in season_dirs:
            for ep_file in sd.glob("e*.json"):
                with open(ep_file) as f:
                    doc = json.load(f)
                assert "type" in doc
                assert doc["type"] == "Episode"


# ════════════════════════════════════════════════════════════════════
# JSON-LD context validation
# ════════════════════════════════════════════════════════════════════

class TestContexts:
    def test_season_context_has_version(self, season_context):
        ctx = season_context.get("@context", {})
        assert ctx.get("@version") == 1.1

    def test_episode_context_has_version(self, episode_context):
        ctx = episode_context.get("@context", {})
        assert ctx.get("@version") == 1.1

    def test_season_context_defines_core_terms(self, season_context):
        ctx = season_context.get("@context", {})
        required = ["Season", "Contestant", "Tribe", "season_number",
                     "winner", "ftc_vote", "tribes"]
        missing = [t for t in required if t not in ctx]
        assert not missing, f"Season context missing: {missing}"

    def test_episode_context_defines_core_terms(self, episode_context):
        ctx = episode_context.get("@context", {})
        required = ["Episode", "Challenge", "TribalCouncil", "Vote",
                     "episode_number", "challenges", "tribal_councils"]
        missing = [t for t in required if t not in ctx]
        assert not missing, f"Episode context missing: {missing}"


# ════════════════════════════════════════════════════════════════════
# RDF expansion (requires rdflib + pyld)
# ════════════════════════════════════════════════════════════════════

class TestRDFExpansion:
    @pytest.fixture(scope="class")
    def rdflib_available(self):
        try:
            import rdflib
            import pyld
            return True
        except ImportError:
            pytest.skip("rdflib/pyld not installed")

    def test_single_season_expands(self, rdflib_available):
        from pyld import jsonld
        season_file = DATA_DIR / "season-01-borneo" / "season.json"
        with open(season_file) as f:
            doc = json.load(f)

        with open(CONTEXT_DIR / "season.jsonld") as f:
            ctx = json.load(f)["@context"]

        doc["@context"] = ctx
        nquads = jsonld.to_rdf(doc, {"format": "application/n-quads"})
        assert len(nquads) > 0, "No triples generated from S01"
        assert "seasonNumber" in nquads or "season" in nquads.lower()

    def test_single_episode_expands(self, rdflib_available):
        from pyld import jsonld
        ep_file = DATA_DIR / "season-01-borneo" / "e01.json"
        with open(ep_file) as f:
            doc = json.load(f)

        with open(CONTEXT_DIR / "episode.jsonld") as f:
            ctx = json.load(f)["@context"]

        doc["@context"] = ctx
        nquads = jsonld.to_rdf(doc, {"format": "application/n-quads"})
        assert len(nquads) > 0, "No triples generated from S01E01"


# ════════════════════════════════════════════════════════════════════
# Example SPARQL queries (run against the in-memory dataset)
# ════════════════════════════════════════════════════════════════════

class TestExampleQueries:
    @pytest.fixture(scope="class")
    def dataset(self):
        try:
            from rdflib import Dataset, URIRef
            from pyld import jsonld
        except ImportError:
            pytest.skip("rdflib/pyld not installed")

        ds = Dataset()
        # Load just S01 for speed
        season_file = DATA_DIR / "season-01-borneo" / "season.json"
        with open(season_file) as f:
            doc = json.load(f)
        with open(CONTEXT_DIR / "season.jsonld") as f:
            ctx = json.load(f)["@context"]
        doc["@context"] = ctx
        nquads = jsonld.to_rdf(doc, {"format": "application/n-quads"})
        g = ds.graph(URIRef("https://survivor-kg.github.io/graph/season/1"))
        g.parse(data=nquads, format="nquads")
        return ds

    def test_query_season_number(self, dataset):
        q = """
        PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?num WHERE {
            GRAPH ?g { ?s surv:seasonNumber ?num }
        }
        """
        results = list(dataset.query(q))
        assert len(results) >= 1
        assert int(results[0][0]) == 1

    def test_query_winner_name(self, dataset):
        q = """
        PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?name WHERE {
            GRAPH ?g {
                ?s surv:winner ?w .
                ?w foaf:name ?name .
            }
        }
        """
        results = list(dataset.query(q))
        assert len(results) >= 1
        names = [str(r[0]) for r in results]
        assert "Richard Hatch" in names


# ════════════════════════════════════════════════════════════════════
# Extended SPARQL query tests (v0.4.0)
# ════════════════════════════════════════════════════════════════════

class TestSPARQLAnalytical:
    """Test the analytical SPARQL queries against the live dataset."""

    @pytest.fixture(scope="class")
    def full_dataset(self):
        try:
            from rdflib import Dataset, URIRef
            from pyld import jsonld
        except ImportError:
            pytest.skip("rdflib/pyld not installed")

        ds = Dataset()
        season_ctx = json.load(open(CONTEXT_DIR / "season.jsonld"))["@context"]
        episode_ctx = json.load(open(CONTEXT_DIR / "episode.jsonld"))["@context"]

        # Load S1 + S20 for cross-graph testing
        for sn in [1, 20]:
            sd = None
            for d in DATA_DIR.iterdir():
                if d.name.startswith(f"season-{sn:02d}-"):
                    sd = d; break
            if not sd: continue

            with open(sd / "season.json") as f:
                s = json.load(f)
            doc = dict(s); doc["@context"] = season_ctx
            nq = jsonld.to_rdf(doc, {"format": "application/n-quads"})
            ds.graph(URIRef(f"urn:s:{sn}")).parse(data=nq, format="nquads")

            for ef in sorted(sd.glob("e*.json")):
                with open(ef) as f:
                    ep = json.load(f)
                en = ep.get("episode_number", 0)
                epc = dict(ep); epc["@context"] = episode_ctx
                enq = jsonld.to_rdf(epc, {"format": "application/n-quads"})
                ds.graph(URIRef(f"urn:e:{sn}:{en}")).parse(
                    data=enq, format="nquads")
        return ds

    def test_season_numbers_via_sparql(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?num WHERE { GRAPH ?g { ?s surv:seasonNumber ?num } }"""
        results = list(full_dataset.query(q))
        nums = {int(r[0]) for r in results}
        assert 1 in nums and 20 in nums

    def test_winner_name_via_sparql(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?name WHERE {
            GRAPH ?g { ?s surv:winner ?w . ?w foaf:name ?name . }
        }"""
        results = list(full_dataset.query(q))
        names = {str(r[0]) for r in results}
        assert "Richard Hatch" in names
        assert "Sandra Diaz-Twine" in names

    def test_episode_titles_in_graph(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?title WHERE {
            GRAPH ?g { ?ep surv:episodeTitle ?title . }
        }"""
        results = list(full_dataset.query(q))
        titles = {str(r[0]) for r in results}
        assert "The Marooning" in titles

    def test_tribal_council_data(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        SELECT ?name WHERE {
            GRAPH ?g {
                ?tc surv:personEliminated ?p .
                ?p foaf:name ?name .
            }
        }"""
        results = list(full_dataset.query(q))
        names = {str(r[0]) for r in results}
        assert "Sonja Christopher" in names
        assert "Sugar Kiper" in names

    def test_cross_graph_join(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?season_num ?ep_num ?title WHERE {
            GRAPH ?g1 {
                ?ep surv:episodeTitle ?title ;
                    surv:episodeNumber ?ep_num ;
                    surv:inSeason ?s .
            }
            GRAPH ?g2 {
                ?s surv:seasonNumber ?season_num .
            }
        }
        ORDER BY ?season_num ?ep_num"""
        results = list(full_dataset.query(q))
        assert len(results) >= 20
        # Check S1E1 is "The Marooning"
        s1e1 = [r for r in results
                if int(r[0]) == 1 and int(r[1]) == 1]
        assert len(s1e1) >= 1
        assert "Marooning" in str(s1e1[0][2])

    def test_viewership_data(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?viewers WHERE {
            GRAPH ?g { ?ep surv:viewershipMillions ?viewers . }
        }
        ORDER BY DESC(?viewers)
        LIMIT 1"""
        results = list(full_dataset.query(q))
        assert len(results) >= 1
        top = float(str(results[0][0]))
        assert top > 40  # S1 finale was 51.69M

    def test_era_distribution(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?era (COUNT(?s) AS ?c) WHERE {
            GRAPH ?g { ?s a surv:Season ; surv:era ?era . }
        }
        GROUP BY ?era"""
        results = list(full_dataset.query(q))
        eras = {str(r[0]): int(r[1]) for r in results}
        # We only loaded S1 and S20, both classic
        assert "classic" in eras

    def test_challenge_types(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?type (COUNT(?ch) AS ?c) WHERE {
            GRAPH ?g { ?ch surv:challengeType ?type . }
        }
        GROUP BY ?type"""
        results = list(full_dataset.query(q))
        types = {str(r[0]) for r in results}
        assert "immunity" in types

    def test_tribe_names(self, full_dataset):
        q = """PREFIX surv: <https://survivor-kg.github.io/ontology/survivor#>
        SELECT ?name WHERE {
            GRAPH ?g { ?t a surv:Tribe ; surv:tribeName ?name . }
        }"""
        results = list(full_dataset.query(q))
        names = {str(r[0]) for r in results}
        assert "Tagi" in names or "Heroes" in names


# ════════════════════════════════════════════════════════════════════
# Provenance quality tests (v0.4.0)
# ════════════════════════════════════════════════════════════════════

class TestProvenance:
    """Validate provenance records for data traceability."""

    def test_all_season_provenance_files_exist(self):
        prov_dir = ROOT / "research" / "provenance"
        for sn in range(1, 51):
            pf = prov_dir / f"s{sn:02d}-provenance.jsonld"
            assert pf.exists(), f"Missing provenance for S{sn}"

    def test_source_registry_exists(self):
        reg = ROOT / "research" / "provenance" / "source-registry.jsonld"
        assert reg.exists()
        with open(reg) as f:
            data = json.load(f)
        assert len(data.get("sources", [])) >= 10

    def test_enrichment_chain_exists(self):
        chain = ROOT / "research" / "provenance" / "enrichment-chain.jsonld"
        assert chain.exists()
        with open(chain) as f:
            data = json.load(f)
        assert len(data.get("activities", [])) >= 7

    def test_season_files_have_provenance(self):
        missing = []
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir():
                continue
            sf = sd / "season.json"
            if not sf.exists():
                continue
            with open(sf) as f:
                s = json.load(f)
            if not s.get("_provenance"):
                missing.append(s.get("season_number"))
        assert len(missing) == 0, f"Seasons missing _provenance: {missing}"

    def test_episode_files_have_provenance(self):
        missing_count = 0
        total = 0
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir():
                continue
            for ef in sorted(sd.glob("e*.json")):
                total += 1
                with open(ef) as f:
                    ep = json.load(f)
                if not ep.get("_provenance"):
                    missing_count += 1
        assert missing_count == 0, f"{missing_count}/{total} episodes missing _provenance"

    def test_provenance_has_field_level_sources(self):
        """Each episode _provenance should map populated fields to sources."""
        ef = DATA_DIR / "season-01-borneo" / "e01.json"
        with open(ef) as f:
            ep = json.load(f)
        prov = ep.get("_provenance", {})
        fields = prov.get("fields", {})
        assert "episode_title" in fields
        assert "source" in fields["episode_title"]
        assert "confidence" in fields["episode_title"]

    def test_provenance_not_in_rdf(self):
        """_provenance should be stripped before RDF expansion."""
        from pyld import jsonld
        ctx = json.load(open(CONTEXT_DIR / "episode.jsonld"))["@context"]
        ep = json.load(open(DATA_DIR / "season-01-borneo" / "e01.json"))
        # Strip underscore keys as expand_to_rdf.py does
        clean = {k: v for k, v in ep.items() if not k.startswith("_")}
        clean["@context"] = ctx
        nq = jsonld.to_rdf(clean, {"format": "application/n-quads"})
        assert "provenance" not in nq.lower()

    def test_provenance_confidence_range(self):
        """All confidence scores should be between 0.0 and 1.0."""
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir():
                continue
            for ef in list(sd.glob("e*.json"))[:3]:  # spot-check
                with open(ef) as f:
                    ep = json.load(f)
                prov = ep.get("_provenance", {})
                c = prov.get("avg_confidence", 0)
                assert 0 <= c <= 1.0, f"{ef}: confidence {c} out of range"

    def test_enrichment_chain_triple_progression(self):
        """Triple counts should monotonically increase across phases."""
        chain = ROOT / "research" / "provenance" / "enrichment-chain.jsonld"
        with open(chain) as f:
            data = json.load(f)
        prev = 0
        for act in data["activities"]:
            after = act.get("triples_after", 0)
            assert after >= prev, f"{act['id']}: triples_after ({after}) < previous ({prev})"
            prev = after


class TestIdolData:
    """Validate idol play enrichment data."""

    def test_idol_plays_present(self):
        idol_count = 0
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir(): continue
            for ef in sorted(sd.glob("e*.json")):
                with open(ef) as f: ep = json.load(f)
                if ep.get("idol_plays"): idol_count += 1
        assert idol_count >= 100, f"Expected 100+ episodes with idol data, got {idol_count}"

    def test_idol_event_types_valid(self):
        valid = {"idol_played","idol_found","idol_not_played","fake_idol_played",
                 "fake_idol_found","idol_given","idol_refused","idol_stolen",
                 "idol_nullifier_played","knowledge_is_power","advantage_played",
                 "beware_idol_found","fake_idol_crafted","idol_destroyed"}
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir(): continue
            for ef in sorted(sd.glob("e*.json")):
                with open(ef) as f: ep = json.load(f)
                for ip in ep.get("idol_plays", []):
                    assert ip.get("type") in valid, f"Invalid idol type: {ip.get('type')} in {ef}"

    def test_first_idol_in_s11(self):
        ef = DATA_DIR / "season-11-guatemala" / "e08.json"
        with open(ef) as f: ep = json.load(f)
        ips = ep.get("idol_plays", [])
        assert len(ips) >= 1
        assert any(ip["type"] == "idol_found" for ip in ips)
        assert any("first" in ip.get("notes","").lower() for ip in ips)

    def test_no_idols_before_s11(self):
        for sn in range(1, 11):
            sd = None
            for d in DATA_DIR.iterdir():
                if d.name.startswith(f"season-{sn:02d}-"): sd = d; break
            if not sd: continue
            for ef in sorted(sd.glob("e*.json")):
                with open(ef) as f: ep = json.load(f)
                assert not ep.get("idol_plays"), f"S{sn} should not have idol data (pre-idol era)"

    def test_votes_negated_range(self):
        for sd in sorted(DATA_DIR.iterdir()):
            if not sd.is_dir(): continue
            for ef in sorted(sd.glob("e*.json")):
                with open(ef) as f: ep = json.load(f)
                for ip in ep.get("idol_plays", []):
                    vn = ip.get("votes_negated")
                    if vn is not None:
                        assert 0 <= vn <= 12, f"votes_negated {vn} out of range in {ef}"
