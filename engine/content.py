"""AI phrase generation with permanent no-repeat history."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime

import requests

import config
from config import CATEGORIES, CATEGORIES_NATIVE, HISTORY_DIR, MAX_RECENT_CATEGORIES

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"

PHRASE_KEY = config.LANGUAGE["history_key"]
LANGUAGE_NAME = config.LANGUAGE["name"]
NATIVE_NAME = config.LANGUAGE["native_name"]

# ==== FALLBACK PHRASES START ====
FALLBACK_PHRASES = [
    {"english": "Hello, nice to meet you.", "native": "Zdravo, drago mi je.", "transliteration": "Zdravo, drago mi je."},
    {"english": "Thank you very much.", "native": "Hvala vam puno.", "transliteration": "Hvala vam puno."},
    {"english": "Good morning, have a great day.", "native": "Dobro jutro, lep dan.", "transliteration": "Dobro jutro, lep dan."},
    {"english": "I love learning new languages.", "native": "Volim da učim nove jezike.", "transliteration": "Volim da učim nove jezike."},
    {"english": "Never give up on your dreams.", "native": "Nikada ne odustajte od svojih snova.", "transliteration": "Nikada ne odustajte od svojih snova."},
    {"english": "Every day is a fresh start.", "native": "Svaki dan je novi početak.", "transliteration": "Svaki dan je novi početak."},
    {"english": "Believe in yourself always.", "native": "Uvek verujte u sebe.", "transliteration": "Uvek verujte u sebe."},
    {"english": "Small steps lead to big changes.", "native": "Mali koraci vode do velikih promena.", "transliteration": "Mali koraci vode do velikih promena."},
    {"english": "You are stronger than you think.", "native": "Jači ste nego što mislite.", "transliteration": "Jači ste nego što mislite."},
    {"english": "Happiness is a choice, choose it.", "native": "Sreća je izbor, izaberite je.", "transliteration": "Sreća je izbor, izaberite je."},
    {"english": "What time is it please.", "native": "Koliko je sati, molim.", "transliteration": "Koliko je sati, molim."},
    {"english": "Where is the train station.", "native": "Gde je železnička stanica.", "transliteration": "Gde je železnička stanica."},
    {"english": "How much does this cost.", "native": "Koliko ovo košta.", "transliteration": "Koliko ovo košta."},
    {"english": "Can you help me please.", "native": "Možete li mi pomoći, molim.", "transliteration": "Možete li mi pomoći, molim."},
    {"english": "I would like a coffee please.", "native": "Hteo bih kafu, molim.", "transliteration": "Hteo bih kafu, molim."},
    {"english": "The food is delicious today.", "native": "Hrana je ukusna danas.", "transliteration": "Hrana je ukusna danas."},
    {"english": "Have a wonderful weekend.", "native": "Lep vikend.", "transliteration": "Lep vikend."},
    {"english": "Take care of yourself.", "native": "Čuvajte se.", "transliteration": "Čuvajte se."},
    {"english": "See you tomorrow my friend.", "native": "Vidimo se sutra, prijatelju.", "transliteration": "Vidimo se sutra, prijatelju."},
    {"english": "The weather is beautiful outside.", "native": "Napolju je prelepo vreme.", "transliteration": "Napolju je prelepo vreme."},
    {"english": "I am very happy today.", "native": "Veoma sam srećan danas.", "transliteration": "Veoma sam srećan danas."},
    {"english": "Learning a language opens new doors.", "native": "Učenje jezika otvara nova vrata.", "transliteration": "Učenje jezika otvara nova vrata."},
    {"english": "Keep practicing every single day.", "native": "Vežbajte svakog dana.", "transliteration": "Vežbajte svakog dana."},
    {"english": "You can achieve anything you want.", "native": "Možete postići sve što želite.", "transliteration": "Možete postići sve što želite."},
    {"english": "Rest when you are tired.", "native": "Odmorite se kada ste umorni.", "transliteration": "Odmorite se kada ste umorni."},
    {"english": "Focus on the positive things.", "native": "Fokusirajte se na pozitivne stvari.", "transliteration": "Fokusirajte se na pozitivne stvari."},
    {"english": "Learn from your mistakes.", "native": "Učite iz svojih grešaka.", "transliteration": "Učite iz svojih grešaka."},
    {"english": "Trust the process completely.", "native": "Potpuno verujte procesu.", "transliteration": "Potpuno verujte procesu."},
    {"english": "Breathe deeply and stay calm.", "native": "Dišite duboko i ostanite mirni.", "transliteration": "Dišite duboko i ostanite mirni."},
    {"english": "Enjoy the little moments in life.", "native": "Uživajte u malim trenucima u životu.", "transliteration": "Uživajte u malim trenucima u životu."},
    {"english": "Smile more, worry less.", "native": "Smejte se više, brinite manje.", "transliteration": "Smejte se više, brinite manje."},
    {"english": "Be kind to everyone you meet.", "native": "Budite ljubazni prema svima koje sretnete.", "transliteration": "Budite ljubazni prema svima koje sretnete."},
    {"english": "Help others without expecting anything back.", "native": "Pomažite drugima bez očekivanja nečega zauzvrat.", "transliteration": "Pomažite drugima bez očekivanja nečega zauzvrat."},
    {"english": "Forgive yourself and move forward.", "native": "Oprostite sebi i krenite dalje.", "transliteration": "Oprostite sebi i krenite dalje."},
    {"english": "Stay strong in difficult times.", "native": "Ostanite jaki u teškim vremenima.", "transliteration": "Ostanite jaki u teškim vremenima."},
    {"english": "Every moment is a new beginning.", "native": "Svaki trenutak je novi početak.", "transliteration": "Svaki trenutak je novi početak."},
    {"english": "Listen to your heart always.", "native": "Uvek slušajte svoje srce.", "transliteration": "Uvek slušajte svoje srce."},
    {"english": "Do what makes you happy.", "native": "Radite ono što vas čini srećnim.", "transliteration": "Radite ono što vas čini srećnim."},
    {"english": "Your potential is unlimited.", "native": "Vaš potencijal je neograničen.", "transliteration": "Vaš potencijal je neograničen."},
    {"english": "Be brave and take risks.", "native": "Budite hrabri i rizikujte.", "transliteration": "Budite hrabri i rizikujte."},
    {"english": "Celebrate your progress every day.", "native": "Slavite svoj napredak svakog dana.", "transliteration": "Slavite svoj napredak svakog dana."},
    {"english": "Surround yourself with good people.", "native": "Okružite se dobrim ljudima.", "transliteration": "Okružite se dobrim ljudima."},
    {"english": "Read books and grow your mind.", "native": "Čitajte knjige i razvijajte svoj um.", "transliteration": "Čitajte knjige i razvijajte svoj um."},
    {"english": "Travel and discover new places.", "native": "Putujte i otkrivajte nova mesta.", "transliteration": "Putujte i otkrivajte nova mesta."},
    {"english": "Appreciate what you already have.", "native": "Cenite ono što već imate.", "transliteration": "Cenite ono što već imate."},
    {"english": "Dance like nobody is watching.", "native": "Plešite kao da vas niko ne gleda.", "transliteration": "Plešite kao da vas niko ne gleda."},
    {"english": "Sing from your heart out loud.", "native": "Pevajte iz srca glasno.", "transliteration": "Pevajte iz srca glasno."},
    {"english": "Plant seeds of kindness everywhere.", "native": "Sejte seme ljubaznosti svuda.", "transliteration": "Sejte seme ljubaznosti svuda."},
    {"english": "Let go of what you cannot control.", "native": "Pustite ono što ne možete kontrolisati.", "transliteration": "Pustite ono što ne možete kontrolisati."},
    {"english": "Be present in the here and now.", "native": "Budite prisutni u sadašnjem trenutku.", "transliteration": "Budite prisutni u sadašnjem trenutku."},
]
# ==== FALLBACK PHRASES END ====


def _load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_phrase_history():
    data = _load_json(PHRASE_HISTORY_FILE, {"phrases": [], "last_updated": None})
    data.setdefault("phrases", [])
    return data


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    _save_json(PHRASE_HISTORY_FILE, data)


def is_phrase_used(english):
    english_lower = english.lower().strip()
    for p in load_phrase_history()["phrases"]:
        if p.get("english", "").lower().strip() == english_lower:
            return True
    return False


def _history_native(p):
    for key in (PHRASE_KEY, "vietnamese", "native", "translation", "target"):
        value = p.get(key)
        if value:
            return str(value)
    return ""


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    for phrase in phrases:
        history["phrases"].append({
            "english": phrase["english"],
            PHRASE_KEY: phrase["native"],
            "transliteration": phrase.get("transliteration", ""),
            "category": category,
            "generated_at": datetime.now().isoformat(),
        })
    save_phrase_history(history)
    print(f"[content] Saved {len(phrases)} phrases (history total: {len(history['phrases'])})")


def get_available_category():
    data = _load_json(RECENT_CATEGORIES_FILE, {"recent_categories": [], "last_updated": None})
    recent = data.get("recent_categories", [])
    available = [c for c in CATEGORIES if c not in recent]
    if not available:
        recent = recent[-5:]
        available = [c for c in CATEGORIES if c not in recent]
        print("[rotation] Reset recent categories")
    selected = random.choice(available)
    recent.append(selected)
    data["recent_categories"] = recent[-MAX_RECENT_CATEGORIES:]
    data["last_updated"] = datetime.now().isoformat()
    _save_json(RECENT_CATEGORIES_FILE, data)
    print(f"[rotation] Category: {selected} ({len(available)} available)")
    return selected


def _normalize_phrase(item):
    if not isinstance(item, dict):
        return None
    english = str(item.get("english", "")).strip()
    native = str(
        item.get(PHRASE_KEY)
        or item.get("native")
        or item.get("vietnamese")
        or item.get("translation")
        or ""
    ).strip()
    translit = str(item.get("transliteration") or item.get("romanization") or item.get("romaji") or "").strip()
    if not english or not native:
        return None
    if len(english.split()) > 16:
        return None
    if "/" in native or "|" in native:
        native = native.split("/")[0].split("|")[0].strip()
    return {
        "english": english.replace("  ", " ").strip(),
        "native": native.strip(),
        "transliteration": translit.strip().strip("[]"),
    }


def _history_keys(history):
    used_en = set()
    used_nat = set()
    for p in history.get("phrases", []):
        en = str(p.get("english", "")).lower().strip()
        nat = _history_native(p).lower().strip()
        if en:
            used_en.add(en)
        if nat:
            used_nat.add(nat)
    return used_en, used_nat


def generate_phrases(category_english: str, num_phrases: int = 5) -> list:
    category_native = CATEGORIES_NATIVE[category_english]
    history = load_phrase_history()
    used_en, used_nat = _history_keys(history)
    recent_english = [
        p["english"] for p in history["phrases"] if p.get("category") == category_english
    ][-30:]

    models = [config.AI_MODEL]
    if "gemini-fast" not in models:
        models.append("gemini-fast")

    if config.POLLINATIONS_API_KEY:
        for attempt in range(5):
            model = models[0] if attempt < 3 else models[-1]
            try:
                phrases = _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model)
                unique = []
                for item in phrases:
                    p = _normalize_phrase(item)
                    if not p:
                        continue
                    key_en = p["english"].lower().strip()
                    key_nat = p["native"].lower().strip()
                    if key_en in used_en or key_nat in used_nat:
                        continue
                    if any(key_en == u["english"].lower().strip() for u in unique):
                        continue
                    used_en.add(key_en)
                    used_nat.add(key_nat)
                    unique.append(p)
                    if len(unique) >= num_phrases:
                        break
                if len(unique) >= num_phrases:
                    add_phrases_to_history(unique[:num_phrases], category_english)
                    return unique[:num_phrases]
                print(f"[content] Attempt {attempt + 1}: only {len(unique)} fresh phrases (need {num_phrases})")
            except Exception as exc:  # noqa: BLE001 - network boundary
                print(f"[content] Attempt {attempt + 1} failed ({model}): {exc}")
            time.sleep(1.5 * (attempt + 1))
    else:
        print("[content] No POLLINATIONS_API_KEY, using fallback phrases")

    fresh_fallback = []
    for p in FALLBACK_PHRASES:
        if p["english"].lower().strip() in used_en or p["native"].lower().strip() in used_nat:
            continue
        fresh_fallback.append(p)
    if not fresh_fallback:
        raise RuntimeError("Phrase API unavailable and no unused fallback phrases left; refusing to reuse phrases")
    chosen = fresh_fallback[:num_phrases]
    if len(chosen) < num_phrases:
        print(f"[content] Only {len(chosen)} fresh fallback phrases; building a shorter lesson")
    add_phrases_to_history(chosen, category_english)
    return chosen


def _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model=None):
    avoid = ""
    if recent_english:
        avoid = "\nDo NOT reuse any of these phrases:\n" + "\n".join(f"- {p}" for p in recent_english)

    prompt = f"""Create {num_phrases * 6} unique {category_english} phrases for English speakers learning {LANGUAGE_NAME}.
{avoid}

Rules:
1. Keep every phrase short and natural (4-11 words in English).
2. Use natural commas for TTS breathing pauses.
3. Each phrase must be speakable in 2-4 seconds.
4. Write clean {LANGUAGE_NAME} in {NATIVE_NAME} with correct accents and orthography. One translation only, no slashes.
5. Transliteration is a friendly Roman-script pronunciation guide for English speakers (not IPA).
6. Vary the sentence patterns and emotions. No duplicates.
7. Phrases must feel like real everyday language, not textbook filler.

Return ONLY a JSON array:
[{{"english": "...", "native": "...", "transliteration": "..."}}]"""

    response = requests.post(
        "https://gen.pollinations.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.POLLINATIONS_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or config.AI_MODEL,
            "messages": [
                {"role": "system", "content": f"You are a {LANGUAGE_NAME} teacher creating short, natural, varied bilingual phrases. Reply with JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": min(0.95 + attempt * 0.02, 1.0),
        },
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    if "```json" in content:
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in content:
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    start = content.find("[")
    end = content.rfind("]")
    if start >= 0 and end > start:
        content = content[start:end + 1]

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("AI did not return a JSON array")
    return data
