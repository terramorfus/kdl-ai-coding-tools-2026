# kdl-ai-coding-tools

Repository for Day 4 workshop **Working Critically with AI Coding Tools** at the DH & RSE Summer School 2026.

## Overview

This project performs text analysis on Shakespeare's *Hamlet*. It reads the play, removes stop words, detects bigrams and trigrams, lemmatizes tokens using spaCy, and generates a top-10 word frequency bar chart.

## Project Structure

```
├── text_analysis_notebook.ipynb   # Main analysis notebook
├── example.ipynb                   # Tutorial notebook (example workflow)
├── data/
│   ├── Hamlet.txt                  # Input text (Shakespeare's Hamlet)
│   ├── earlyModernStopword.txt     # Custom stop words
│   └── test_data.txt               # Test data for validation
├── results/                        # Output charts are saved here
├── requirements.txt                # Python dependencies
└── opencode.json                   # AI coding tool configuration
```

## Getting Started

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd kdl-ai-coding-tools
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the notebook**

   ```bash
   jupyter notebook text_analysis_notebook.ipynb
   ```

   Or execute it non-interactively:

   ```bash
   jupyter nbconvert --to notebook --execute text_analysis_notebook.ipynb
   ```

## Testing

Run the notebook with the provided test data to verify the pipeline works:

```bash
# Update the documentName variable in the notebook to "test_data.txt"
# then execute:
jupyter nbconvert --to notebook --execute text_analysis_notebook.ipynb
```

The output histogram will be saved to the `results/` directory.

## Example Notebook

See `example.ipynb` for a self-contained tutorial that runs the text analysis pipeline on the test data file and explains the input/output flow.

## Software Quality Checklist

Self-assessment against the [FAIR software checklist](https://fairsoftwarechecklist.net/v0.2/):

| Principle | Assessment | Notes |
|---|---|---|
| **Findable** | Partial | Repository hosted on GitHub (SEO-enabled platform). Identified by URL. |
| **Accessible** | Good | Code retrievable via HTTPS. MIT license permits reuse. |
| **Interoperable** | Partial | Input/output uses plain text and HTML (open formats). Dependencies listed in `requirements.txt`. Versioned via git. |
| **Reusable** | Good | Source files available with documentation and a permissive license. Dependencies installable via pip. |

## Contributing

Contributions are welcome. If you find a bug or have an idea for improvement, please open an issue or submit a pull request.
