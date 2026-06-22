import json
from src.semantic.domain_taxonomy import DOMAIN_CONCEPTS

def extract_domains(obj: any, discovered_domains: set):
    if isinstance(obj, dict):
        for v in obj.values():
            extract_domains(v, discovered_domains)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            extract_domains(item, discovered_domains)
    elif isinstance(obj, str):
        val = obj.lower()
        for domain, keywords in DOMAIN_CONCEPTS.items():
            if any(kw.lower() == val for kw in keywords) or any(kw.lower() in val.split() for kw in keywords):
                discovered_domains.add(domain)

with open('candidates.jsonl', 'r') as f:
    for line in f:
        payload = json.loads(line)
        discovered_domains = set()
        extract_domains(payload, discovered_domains)
        print("Candidate", payload.get('candidate_id'), "Domains:", discovered_domains)
        break
