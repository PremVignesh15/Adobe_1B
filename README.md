# Adobe_1B - Round 1B
---------------------------------------------------
Goal:
Extract document outline using only font size, font family, and layout — no LLMs.

Approach:
1. Parse PDF using PyMuPDF
2. Extract text spans with font size and name
3. Rank font sizes: largest as title, then h1, h2, etc.
4. Build hierarchy:
   - title, h1, h2, h3
   - Detect bullet points using regex
   - Collect normal text as body

Folder Structure:
round_1B_non_llm/
├── main.py
├── Dockerfile
├── requirements.txt
├── input/
│   └── input.pdf
└── output/
    └── output.json

How to Run:
Local:
  pip install -r requirements.txt
  python main.py

Docker:
  docker build -t pdf-outline-extractor .
  docker run --rm -v "$PWD/input":/app/input -v "$PWD/output":/app/output pdf-outline-extractor
