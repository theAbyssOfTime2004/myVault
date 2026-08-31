# Academic transcript generator

Turns the `GPA.csv` grade export from the university portal into a formal,
bilingual (Vietnamese / English) A4 transcript PDF suitable for job applications.

## Usage

```bash
pip install reportlab
python3 generate_transcript.py GPA.csv Academic_Transcript.pdf student_info.json
```

- `GPA.csv` — the portal export (columns: course, credits, score, letter grade,
  4.0 grade, term, class, notes). Summary rows at the end are ignored.
- `student_info.json` — personal details the export does not contain. Copy
  `student_info.example.json` and fill it in. Any field left empty is rendered
  as a dotted line to be completed by hand.

## What it produces

- Courses grouped by academic term, in chronological order, with per-term
  credits and term GPA on both the 10.0 and 4.0 scales.
- English course titles alongside the Vietnamese originals.
- A summary panel (total credits, cumulative GPA on both scales, classification)
  and a grading-system legend.
- Typeset in Liberation Serif, which has full Vietnamese diacritic coverage.

All figures are recomputed from the course rows and cross-checked against the
summary lines in the export.

## Note

`GPA.csv`, `student_info.json` and generated PDFs are git-ignored: this
repository is public and those files contain personal academic records.
