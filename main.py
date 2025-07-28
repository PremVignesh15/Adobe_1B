import fitz
import json
import re
from collections import Counter
import os

def extract_font_info(pdf_path):
    doc = fitz.open(pdf_path)
    elements = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    if text:
                        elements.append({
                            "text": text,
                            "font": span["font"],
                            "size": round(span["size"], 1),
                            "page": page_num
                        })
    return elements

def get_size_groups(elements):
    sizes = [e["size"] for e in elements]
    freq = Counter(sizes)
    sorted_sizes = sorted(freq.items(), key=lambda x: -x[0])
    size_to_tag = {}
    tags = ['title', 'h1', 'h2', 'h3']
    for i, (size, _) in enumerate(sorted_sizes[:len(tags)]):
        size_to_tag[size] = tags[i]
    return size_to_tag

def is_bullet(text):
    return re.match(r"^[-•*·]\s+.+", text) or re.match(r"^\d+[\.\)]\s+.+", text)

def build_structure(elements, size_to_tag):
    structured = {"title": "", "h1": []}
    current_h1 = None
    current_h2 = None
    current_h3 = None

    for e in elements:
        tag = size_to_tag.get(e["size"], "body")

        if tag == "title" and not structured["title"]:
            structured["title"] = e["text"]

        elif tag == "h1":
            current_h1 = {"heading": e["text"], "body": "", "bullets": [], "h2": []}
            structured["h1"].append(current_h1)
            current_h2 = None
            current_h3 = None

        elif tag == "h2" and current_h1:
            current_h2 = {"heading": e["text"], "body": "", "bullets": [], "h3": []}
            current_h1["h2"].append(current_h2)
            current_h3 = None

        elif tag == "h3" and current_h1 and current_h2:
            current_h3 = {"heading": e["text"], "body": "", "bullets": []}
            current_h2["h3"].append(current_h3)

        elif is_bullet(e["text"]):
            if current_h3:
                current_h3["bullets"].append(e["text"])
            elif current_h2:
                current_h2["bullets"].append(e["text"])
            elif current_h1:
                current_h1["bullets"].append(e["text"])

        elif tag == "body":
            if current_h3:
                current_h3["body"] += e["text"] + " "
            elif current_h2:
                current_h2["body"] += e["text"] + " "
            elif current_h1:
                current_h1["body"] += e["text"] + " "

    return structured

def save_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def main():
    input_path = "input/input.pdf"
    output_path = "output/output.json"

    print("Extracting text and font info...")
    elements = extract_font_info(input_path)

    print("Analyzing font sizes...")
    size_to_tag = get_size_groups(elements)

    print("Building document structure...")
    structured = build_structure(elements, size_to_tag)

    print("Saving output...")
    save_json(structured, output_path)

    print("Done! Output saved to:", output_path)

if __name__ == "__main__":
    main()
