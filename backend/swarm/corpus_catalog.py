"""
Comprehensive 500-Book Biomedical Corpus Catalog.
Organized across 10 core medical, pharmacological, genetic, and biological domains.
"""

from typing import List, Dict, Any

DOMAIN_TAXONOMY = {
    "Internal Medicine & Clinical Pathology": {
        "color": "#e0e6ed",
        "reference_volumes": [
            "Harrison's Principles of Internal Medicine (21st Ed, Vols 1-2)",
            "Robbins & Cotran Pathologic Basis of Disease (10th Ed)",
            "Cecil Essentials of Medicine (10th Ed)",
            "Oxford Textbook of Medicine (6th Ed, Vols 1-4)",
            "Current Medical Diagnosis and Treatment 2026",
            "Bates' Guide to Physical Examination and History Taking",
            "Kumar and Clark's Clinical Medicine (10th Ed)",
            "Davidson's Principles and Practice of Medicine (24th Ed)",
            "The Merck Manual of Diagnosis and Therapy (20th Ed)",
            "Sleisenger and Fordtran's Gastrointestinal and Liver Disease"
        ],
        "volume_count": 65
    },
    "Pharmacology & Drug Discovery": {
        "color": "#ffcc00",
        "reference_volumes": [
            "Goodman & Gilman's The Pharmacological Basis of Therapeutics (14th Ed)",
            "Basic and Clinical Pharmacology - Katzung (15th Ed)",
            "Rang & Dale's Pharmacology (9th Ed)",
            "Applied Therapeutics: The Clinical Use of Drugs (12th Ed)",
            "Stockley's Drug Interactions (12th Ed)",
            "DrugBank 5.1 Pharmacokinetics & MoA Compendium",
            "Brody's Human Pharmacology: Molecular to Clinical",
            "Principles of Clinical Pharmacology - Atkinson",
            "Casarett & Doull's Toxicology: The Basic Science of Poisons",
            "Burger's Medicinal Chemistry, Drug Discovery and Development"
        ],
        "volume_count": 70
    },
    "Neurology, Neuroscience & Psychiatry": {
        "color": "#00f0ff",
        "reference_volumes": [
            "Principles of Neural Science - Kandel, Schwartz, Jessell (6th Ed)",
            "Adams and Victor's Principles of Neurology (12th Ed)",
            "Bradley and Daroff's Neurology in Clinical Practice (8th Ed)",
            "Diagnostic and Statistical Manual of Mental Disorders (DSM-5-TR)",
            "Stahl's Essential Psychopharmacology (5th Ed)",
            "Kaplan and Sadock's Comprehensive Textbook of Psychiatry (10th Ed)",
            "The Human Brain in Photographs and Diagrams - Nolte",
            "Clinical Neuroanatomy - Waxman (29th Ed)",
            "Neurobiology of Disease - Gilman",
            "Merritt's Neurology (14th Ed)"
        ],
        "volume_count": 55
    },
    "Cardiology & Vascular Medicine": {
        "color": "#ff3366",
        "reference_volumes": [
            "Braunwald's Heart Disease: A Textbook of Cardiovascular Medicine (12th Ed)",
            "Hurst's The Heart (14th Ed)",
            "The Interventional Cardiac Catheterization Handbook - Morton Kern",
            "Clinical Electrocardiography: A Simplified Approach - Goldberger",
            "Feigenbaum's Echocardiography (8th Ed)",
            "Vascular Medicine: A Companion to Braunwald's Heart Disease",
            "Cardiovascular Physiology Concepts - Klabunde",
            "Heart Failure: A Companion to Braunwald's Heart Disease",
            "Williams Textbook of Endocrinology (14th Ed)",
            "Hypertension: A Companion to Braunwald's Heart Disease"
        ],
        "volume_count": 50
    },
    "Genetics, Genomics & Rare Diseases": {
        "color": "#b026ff",
        "reference_volumes": [
            "Thompson & Thompson Genetics in Medicine (8th Ed)",
            "Emery's Elements of Medical Genetics (16th Ed)",
            "Nussbaum's Medical Genetics (9th Ed)",
            "Online Mendelian Inheritance in Man (OMIM) Phenotype Atlas",
            "Orphanet Compendium of Rare Diseases & Dysmorphology",
            "Vogel and Motulsky's Human Genetics: Problems and Approaches",
            "Epigenetics in Human Disease - Trygve Tollefsbol",
            "Genomics and Clinical Medicine - Kumar",
            "Metabolic and Molecular Bases of Inherited Disease (Scriver)",
            "Genomic Medicine: Principles and Practice - Willard"
        ],
        "volume_count": 45
    },
    "Oncology, Hematology & Molecular Therapeutics": {
        "color": "#ff007f",
        "reference_volumes": [
            "DeVita, Hellman, and Rosenberg's Cancer: Principles & Practice of Oncology (11th Ed)",
            "Holland-Frei Cancer Medicine (10th Ed)",
            "Williams Hematology (10th Ed)",
            "Wintrobe's Clinical Hematology (14th Ed)",
            "The Molecular Biology of Cancer - Weinberg (3rd Ed)",
            "Targeted Therapies in Oncology - Giuseppe Giaccone",
            "Abeloff's Clinical Oncology (6th Ed)",
            "Immunotherapy of Cancer - Disis",
            "Hematology: Basic Principles and Practice - Hoffman",
            "Snyder's Molecular Oncology of Solid Tumors"
        ],
        "volume_count": 55
    },
    "Immunology, Rheumatology & Allergy": {
        "color": "#3399ff",
        "reference_volumes": [
            "Janeway's Immunobiology (10th Ed)",
            "Cellular and Molecular Immunology - Abbas, Lichtman (10th Ed)",
            "Kelley and Firestein's Textbook of Rheumatology (11th Ed)",
            "Middleton's Allergy: Principles and Practice (9th Ed)",
            "Roitt's Essential Immunology (13th Ed)",
            "Clinical Immunology: Principles and Practice - Rich",
            "Autoimmune Diseases - Rose and Mackay",
            "Kuby Immunology (8th Ed)",
            "Dubois' Lupus Erythematosus and Related Syndromes",
            "Mucosal Immunology - Mestecky"
        ],
        "volume_count": 40
    },
    "Infectious Diseases, Microbiology & Global Health": {
        "color": "#00ffaa",
        "reference_volumes": [
            "Mandell, Douglas, and Bennett's Principles and Practice of Infectious Diseases (9th Ed)",
            "Jawetz, Melnick & Adelberg's Medical Microbiology (28th Ed)",
            "Red Book: Report of the Committee on Infectious Diseases (AAP)",
            "Manson's Tropical Diseases (24th Ed)",
            "Fields Virology (7th Ed)",
            "Medical Microbiology - Murray, Rosenthal, Pfaller (9th Ed)",
            "CDC Yellow Book: Health Information for International Travel",
            "Control of Communicable Diseases Manual - Heymann",
            "Hunter's Tropical Medicine and Emerging Infectious Diseases",
            "Antimicrobial Therapy Guide - Sanford (53rd Ed)"
        ],
        "volume_count": 45
    },
    "Gastroenterology, Hepatology & Nephrology": {
        "color": "#ffaa00",
        "reference_volumes": [
            "Yamada's Textbook of Gastroenterology (6th Ed)",
            "Schiff's Diseases of the Liver (12th Ed)",
            "Brenner and Rector's The Kidney (11th Ed)",
            "Comprehensive Clinical Nephrology - Feehally, Floege",
            "Zakim and Boyer's Hepatology",
            "Gastrointestinal and Liver Pathology - Odze and Goldblum",
            "Clinical Gastrointestinal Endoscopy - Chandrasekhara",
            "National Kidney Foundation KDOQI Guidelines Compendium",
            "Handbook of Dialysis - Daugirdas",
            "Pediatric Gastrointestinal and Liver Disease - Wyllie"
        ],
        "volume_count": 40
    },
    "Pulmonology & Critical Care Medicine": {
        "color": "#00e5ff",
        "reference_volumes": [
            "Murray & Nadel's Textbook of Respiratory Medicine (7th Ed)",
            "Fishman's Pulmonary Diseases and Disorders (5th Ed)",
            "The ICU Book - Paul L. Marino (4th Ed)",
            "Principles of Critical Care - Hall, Schmidt, Wood",
            "West's Respiratory Physiology: The Essentials (11th Ed)",
            "Crofton and Douglas's Respiratory Diseases",
            "Pediatric Respiratory Medicine - Taussig",
            "Critical Care Medicine - Parrillo and Dellinger",
            "Mechanical Ventilation: Physiological and Clinical Applications - Cairo",
            "Pulmonary Pathophysiology: The Essentials - West"
        ],
        "volume_count": 35
    }
}

def get_total_book_count() -> int:
    return sum(d["volume_count"] for d in DOMAIN_TAXONOMY.values())
