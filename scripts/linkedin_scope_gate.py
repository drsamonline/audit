#!/usr/bin/env python3
"""HARD GATE for the daily LinkedIn post.

Decides whether a repo may be posted about, from state/linkedin-scope.json and the
repo's own README. Fails closed: anything it cannot place confidently is DENIED.

    python3 linkedin_scope_gate.py <repo> <readme.md> [--scope scope.json]

Exit 0 = ALLOW (category on stdout), 1 = DENY, 2 = scope file unreadable/invalid.
"""
import json, os, re, sys, urllib.request

SCOPE_URL = "https://raw.githubusercontent.com/drsamonline/audit/main/state/linkedin-scope.json"

ALLOW_TERMS = {
    "medical-health": [
        "repertory", "repertories", "materia medica", "homeopath", "symptom", "symptoms",
        "patient", "patients", "case taking", "case-taking", "prescription", "prescribing",
        "remedy", "remedies", "potency", "potencies", "clinic", "clinical", "opd", "diagnos",
        "medical", "medicine", "anatomy", "pharmacology", "drug", "dose", "dosage", "organon",
        "aphorism", "miasm", "constitution", "constitutional", "health record", "case sheet",
        "consultation", "physician", "doctor", "nurse", "nursing", "triage", "icd",
    ],
    "mind-mental-health": [
        "mood", "anxiety", "anxious", "depress", "calm", "breath", "breathing", "meditat",
        "mindful", "journal", "journaling", "gratitude", "sleep", "insomnia", "attention",
        "focus", "memory", "psycholog", "mental", "wellbeing", "well-being", "stress",
        "mind-body", "mind body", "cbt", "reflection", "self-care", "grounding",
    ],
    "lifestyle-wellness": [
        "diet", "nutrition", "calorie", "calories", "macros", "fitness", "workout", "exercise",
        "steps", "habit", "hydration", "water intake", "fasting", "yoga", "posture", "stretch",
        "weight", "bmi", "menstrual", "cycle", "pregnan", "elder", "elderly", "caregiv",
        "wellness", "lifestyle", "health tracking", "sleep tracking", "meal",
    ],
}

DENY_TERMS = [
    "fps", "first-person shooter", "first person shooter", "shooter", "arena shooter",
    "roguelike", "platformer", "game", "games", "gaming", "gameplay", "player", "players",
    "enemy", "enemies", "weapon", "weapons", "level editor", "wave", "waves", "score",
    "high score", "boss", "dungeon", "sprite", "sprites", "texture", "textures", "render loop",
    "three.js", "webgl", "raylib", "pygame", "godot", "unity", "unreal",
    "compiler", "interpreter", "bundler", "linter", "cli", "command line tool", "terminal",
    "shell", "framework", "library", "sdk", "package manager", "regex engine", "database engine",
    "container", "kubernetes", "docker", "ci/cd", "pipeline", "deploy", "infrastructure",
    "astrolog", "horoscope", "numerolog", "zodiac", "tarot", "kundli", "rashi",
    "stock", "trading", "portfolio", "invoice", "payroll", "accounting", "tax filing",
    "browser", "web browser", "scraper", "crawler", "spreadsheet app", "text editor",
    "note-taking for developers", "chat app", "social network", "url shortener",
]

DENY_STRONG = {"fps", "shooter", "arena shooter", "roguelike", "platformer", "gameplay",
               "level editor", "high score", "astrolog", "numerolog", "horoscope", "kundli"}


def load_scope(path):
    try:
        if path:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        with urllib.request.urlopen(SCOPE_URL, timeout=20) as r:
            return json.load(r)
    except Exception as exc:  # fail closed
        print(f"DENY (scope unreadable: {exc})")
        sys.exit(2)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    scope_path = None
    for i, a in enumerate(argv[1:]):
        if a == "--scope" and i + 2 <= len(argv[1:]):
            scope_path = argv[1:][i + 1]
    if len(args) < 2:
        print("DENY (usage: <repo> <readme.md>)")
        return 1

    repo, readme_path = args[0], args[1]
    scope = load_scope(scope_path)

    if scope.get("mode") != "allowlist-only" or scope.get("on_uncertain") != "skip":
        print("DENY (scope file is not in allowlist-only / skip mode)")
        return 2

    if repo in scope.get("deny_repos", []):
        print(f"DENY {repo} (named in deny_repos)")
        return 1

    try:
        with open(readme_path, encoding="utf-8", errors="replace") as fh:
            text = fh.read(400_000).lower()
    except Exception as exc:
        print(f"DENY (README unreadable: {exc})")
        return 1

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)

    strong = [t for t in DENY_STRONG if re.search(r"\b" + re.escape(t), text)]
    if strong:
        print(f"DENY {repo} (game/occult language: {', '.join(sorted(strong)[:4])})")
        return 1

    scores = {cat: sum(len(re.findall(r"\b" + re.escape(t), text)) for t in terms)
              for cat, terms in ALLOW_TERMS.items()}
    deny_hits = sum(len(re.findall(r"\b" + re.escape(t), text)) for t in DENY_TERMS)

    best = max(scores, key=scores.get)
    best_score = scores[best]
    total = sum(scores.values())

    if best_score < 3 or total < 3:
        print(f"DENY {repo} (not enough in-scope evidence: {scores})")
        return 1
    if deny_hits > best_score:
        print(f"DENY {repo} (out-of-scope language outweighs in-scope: deny={deny_hits} vs {best}={best_score})")
        return 1

    print(f"ALLOW {repo} {best} (scores={scores}, deny={deny_hits})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
