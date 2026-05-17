def load_keywords(file_path):
    with open(file_path, "r") as f:
        return [line.strip() for line in f]

def analyze(content, keywords):
    findings = []
    for word in keywords:
        if word.lower() in content.lower():
            findings.append(word)
    return findings
