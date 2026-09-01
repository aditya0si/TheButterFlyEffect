"""
Colloquial-to-Clinical Lexicon.
Maps everyday plain-language phrases ("my tummy hurts", "throwing up") to clinical
terms understood by the biomedical knowledge graph. Longest phrases are matched
first so specific expressions win over generic ones.
"""

import re
from typing import Dict, List

COLLOQUIAL_LEXICON: Dict[str, List[str]] = {
    # --- Fever / systemic ---
    "running a temperature": ["fever", "pyrexia"],
    "burning up": ["fever", "pyrexia"],
    "burning fever": ["fever", "pyrexia"],
    "high temp": ["fever", "pyrexia"],
    "high temperature": ["fever", "pyrexia"],
    "got a fever": ["fever", "pyrexia"],
    "feverish": ["fever", "pyrexia"],
    "temperature": ["fever", "pyrexia"],
    "fever": ["fever", "pyrexia"],
    "shivering": ["chills", "rigors"],
    "shakes and chills": ["chills", "rigors"],
    "rigors": ["rigors", "chills"],
    "chills": ["chills", "rigors"],
    "no energy at all": ["fatigue"],
    "wiped out": ["fatigue"],
    "exhausted all the time": ["chronic fatigue"],
    "so tired": ["fatigue"],
    "tired all the time": ["chronic fatigue"],
    "body aches": ["muscle pain", "myalgias"],
    "aching all over": ["muscle pain", "myalgias"],
    "body pain": ["muscle pain", "myalgias"],
    "whole body hurts": ["muscle pain", "myalgias"],

    # --- Pain (generic) ---
    "hurts": ["pain"],
    "aching": ["pain"],
    "sore": ["pain"],

    # --- Head / neuro ---
    "splitting headache": ["headache", "migraine"],
    "bad headache": ["headache"],
    "head is pounding": ["headache", "migraine"],
    "pounding headache": ["headache", "migraine"],
    "throbbing head": ["headache", "migraine"],
    "headache": ["headache"],
    "migraine": ["migraine", "headache"],
    "light sensitivity": ["photophobia"],
    "lights bother my eyes": ["photophobia"],
    "sensitive to light": ["photophobia"],
    "seeing flashing lights": ["visual aura", "scintillating scotoma"],
    "flashing lights in vision": ["visual aura", "scintillating scotoma"],
    "zigzag lines in vision": ["visual aura", "scintillating scotoma"],
    "dizzy spells": ["dizziness", "vertigo"],
    "feel dizzy": ["dizziness", "vertigo"],
    "dizzy": ["dizziness", "vertigo"],
    "room is spinning": ["vertigo", "dizziness"],
    "lightheaded": ["dizziness", "pre-syncope"],
    "about to faint": ["fainting", "pre-syncope"],
    "fainted": ["syncope", "fainting"],
    "passed out": ["syncope", "fainting"],
    "brain fog": ["brain fog", "memory fog"],
    "cant think straight": ["brain fog"],
    "can't sleep": ["insomnia"],
    "trouble sleeping": ["insomnia"],
    "cant sleep": ["insomnia"],
    "pins and needles": ["paresthesia"],
    "numbness and tingling": ["paresthesia"],
    "slurred speech": ["dysarthria"],
    "confused easily": ["confusion"],

    # --- Chest / cardio / breathing ---
    "chest tightness": ["chest tightness", "chest pain"],
    "tightness in my chest": ["chest tightness", "chest pain"],
    "chest feels tight": ["chest tightness", "chest pain"],
    "chest is tight": ["chest tightness", "chest pain"],
    "tight chest": ["chest tightness", "chest pain"],
    "chest pressure": ["chest tightness", "chest heaviness"],
    "pressure on my chest": ["chest heaviness", "chest tightness"],
    "heavy chest": ["chest heaviness", "chest tightness"],
    "chest pain": ["chest pain"],
    "chest hurts": ["chest pain"],
    "heart racing": ["palpitations", "tachycardia"],
    "heart is racing": ["palpitations", "tachycardia"],
    "heart pounding": ["palpitations"],
    "fluttering heart": ["palpitations"],
    "palpitations": ["palpitations"],
    "short of breath": ["shortness of breath", "dyspnea"],
    "shortness of breath": ["shortness of breath", "dyspnea"],
    "can't catch my breath": ["dyspnea", "breathlessness"],
    "cant catch my breath": ["dyspnea", "breathlessness"],
    "cant breathe properly": ["dyspnea", "breathlessness"],
    "hard to breathe": ["dyspnea", "breathlessness"],
    "out of breath easily": ["exertional dyspnea"],
    "breathless when walking": ["exertional dyspnea"],
    "swollen ankles": ["peripheral edema", "ankle swelling"],
    "coughing up blood": ["hemoptysis"],
    "coughing a lot": ["cough"],
    "bad cough": ["cough"],
    "wheezing": ["wheezing"],
    "blue lips or fingers": ["cyanosis"],

    # --- Stomach / GI ---
    "tummy ache": ["abdominal pain", "stomach pain"],
    "tummy hurts": ["abdominal pain", "stomach pain"],
    "belly pain": ["abdominal pain"],
    "stomach ache": ["abdominal pain", "stomach pain"],
    "stomach hurts": ["abdominal pain", "stomach pain"],
    "stomach pain": ["abdominal pain"],
    "abdominal pain": ["abdominal pain"],
    "throwing up": ["vomiting"],
    "throw up": ["vomiting"],
    "threw up": ["vomiting"],
    "been sick": ["vomiting", "nausea"],
    "puking": ["vomiting"],
    "puke": ["vomiting"],
    "feel like throwing up": ["nausea", "vomiting"],
    "want to throw up": ["nausea", "vomiting"],
    "queasy": ["nausea"],
    "feel sick to my stomach": ["nausea"],
    "nauseous": ["nausea"],
    "nausea": ["nausea"],
    "acid reflux": ["reflux", "heartburn", "dyspepsia"],
    "heartburn": ["heartburn", "reflux", "dyspepsia"],
    "burning in stomach": ["epigastric pain", "dyspepsia"],
    "burning stomach": ["epigastric pain", "dyspepsia"],
    "acid after eating": ["reflux", "dyspepsia"],
    "cant keep food down": ["vomiting", "nausea"],
    "diarrhea": ["diarrhea"],
    "the runs": ["diarrhea"],
    "loose stools": ["diarrhea"],
    "constipated": ["constipation"],
    "blood in stool": ["melena", "rectal bleeding"],
    "black stools": ["melena"],
    "vomiting blood": ["hematemesis"],
    "yellow eyes": ["jaundice"],
    "yellow skin": ["jaundice"],
    "gassy and bloated": ["bloating"],
    "bloated": ["bloating"],
    "full quickly when eating": ["early satiety"],
    "trouble swallowing": ["dysphagia"],

    # --- Skin / allergy ---
    "itchy rash": ["rash", "pruritus"],
    "rash": ["rash"],
    "hives": ["urticaria", "rash"],
    "butterfly rash on face": ["malar rash"],
    "facial rash": ["malar rash", "rash"],
    "skin looks yellow": ["jaundice"],

    # --- Metabolic / endocrine ---
    "always thirsty": ["excessive thirst", "polydipsia"],
    "peeing a lot": ["polyuria", "frequent urination"],
    "peeing all the time": ["polyuria", "frequent urination"],
    "losing weight without trying": ["weight loss"],
    "unexplained weight loss": ["weight loss"],
    "cant tolerate cold": ["cold intolerance"],
    "always hot": ["heat intolerance"],
    "night sweats": ["night sweats"],

    # --- Joints / muscles ---
    "joints hurt": ["joint pain", "arthralgia"],
    "stiff joints in the morning": ["morning stiffness", "arthritis"],
    "swollen joints": ["joint swelling", "arthritis"],
    "back hurts": ["back pain"],
    "neck feels stiff": ["neck stiffness", "nuchal rigidity"],
    "stiff neck": ["neck stiffness", "nuchal rigidity"],
    "very flexible joints": ["joint hypermobility"],
}

# Canonical node IDs in the graph that correspond to the most common clinical
# concepts. Used to deterministically anchor multi-symptom expansion when the
# concept exists; otherwise the pipeline falls back to vector search.
CANONICAL_NODE_HINTS: Dict[str, str] = {
    "fever": "sym_high_fever",
    "pyrexia": "sym_high_fever",
    "vomiting": "sym_vomiting",
    "nausea": "sym_nausea",
    "migraine": "sym_headache_unilateral",
    "headache": "sym_headache_unilateral",
    "chest tightness": "sym_chest_tightness",
    "chest pain": "sym_chest_tightness",
    "epigastric pain": "sym_epigastric_pain",
    "dyspepsia": "sym_epigastric_pain",
    "exertional dyspnea": "sym_dyspnea_exertional",
    "palpitations": "sym_palpitations",
    "rigors": "sym_rigors",
    "chills": "sym_rigors",
    "chronic fatigue": "sym_chronic_fatigue",
    "fatigue": "sym_chronic_fatigue",
    "photophobia": "sym_photophobia",
    "phonophobia": "sym_phonophobia",
    "visual aura": "sym_visual_aura",
    "scintillating scotoma": "sym_visual_aura",
    "muscle pain": "sym_infe_5_446",
    "myalgias": "sym_infe_5_446",
    "tachycardia": "sym_palpitations",
    "shortness of breath": "sym_dyspnea_exertional",
    "dyspnea": "sym_dyspnea_exertional",
    "breathlessness": "sym_dyspnea_exertional",
    "joint swelling": "sym_joint_swelling",
    "joint hypermobility": "sym_joint_hypermobility",
    "weight loss": "sym_unintentional_weight_loss",
    "early satiety": "sym_early_satiety",
}


def match_clinical_terms(text: str, max_terms: int = 8) -> List[str]:
    """Scans free text and returns an ordered, de-duplicated list of clinical terms.

    Longer phrases always win over shorter ones they contain ("tummy hurts"
    suppresses the generic "hurts"), and results are ordered by where they
    appear in the sentence so the first-mentioned symptom becomes primary.
    """
    lowered = " " + " ".join(text.lower().split()) + " "

    accepted = []
    for phrase in sorted(COLLOQUIAL_LEXICON.keys(), key=len, reverse=True):
        m = re.search(r"(?<![a-z])" + re.escape(phrase) + r"(?![a-z])", lowered)
        if not m:
            continue
        # Skip phrases fully contained inside an already-accepted longer phrase
        if any(start <= m.start() and m.end() <= end for start, end, _ in accepted):
            continue
        accepted.append((m.start(), m.end(), phrase))

    accepted.sort(key=lambda item: item[0])

    found: List[str] = []
    for _, _, phrase in accepted:
        for term in COLLOQUIAL_LEXICON[phrase]:
            if term not in found:
                found.append(term)
        if len(found) >= max_terms:
            break

    return found[:max_terms]
