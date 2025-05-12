# IBM Git Log Stat

A lightweight CLI tool to track your **git commits** and **GitHub pull requests** within a date range, across multiple
repositories.

## 🔧 Installation

```bash
pip install ibm-git-log-stat
```

## Usage

```bash
export GITHUB_TOKEN="provide_your_github_token_here"
ibm-git-log-stat \
  --base-dir ~/projects \
  --author "you@example.com" \
  --github-user yourgithubusername \
  --start-date 2025-04-01 \
  --end-date 2025-04-30 \
  --output-format xls,txt,pdf,docx,ppt,all \
  --check-pr true (remove the argument if u want to disable PR)
  --use-nlp true (remove the argument if u want to disable NLP)

Remember using NLP for the first time can be very slow depending on the
internet speed. It downloads the model for summarization and can take time.
In case it is slow, it is advisable to disable NLP.

Arguments can also be set using environment variables:

BASE_DIR
AUTHOR
GITHUB_USER
START_DATE
END_DATE
OUTPUT_FORMAT

Just export before running if you dont want to specify everytime in parameter
```

## Output Formats

If you want to generate all supported formats then specify in param `--output-format all`

### DOCX, PDF, PPT
Contains a summary of work done with commits grouped by author per page.

Note: Summary is created using NLP and LLM Models. 
For the first time this operation will be slow as the model has to be downloaded locally. 
Depending on internet speed, the maximum time is spent in downloading model.
Either have a good connection to download faster or disable NLP and summary feature.

### TXT, XLS, CSV, TSV
Contains the git commit output in tabular form.

Date | Author  | Commit Hash | Message
---  |---------|-------------| ---
2025-04-29 | Faizan Fordkar | wehfbdhd | Implemented FIXMEs.


