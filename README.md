# eLearn Grace Crawler

Selenium-based crawler that logs into the University of Tehran eLearn portal, collects homework submission data, and calculates per-student grace-time usage. Outputs a consolidated Excel file plus per-homework CSVs.

## Features
- Logs in and locates a course by name + subtitle
- Matches homework names with a configurable fuzzy threshold
- Parses Persian dates and computes lateness/grace usage
- Exports `output/HW_grace.xlsx` and per-homework CSVs

## Requirements
- Python 3.10+
- Google Chrome + compatible ChromeDriver on PATH
- Python packages: see `requirements.txt`

Install:
```bash
pip install -r requirements.txt
```

## Setup
1) Copy the sample credentials file (this file is gitignored):
```bash
cp login_credentials_sample.json login_credentials.json
```

Then fill in your username/password:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

2) Copy the sample config and edit it:
```bash
cp crawler_config_sample.json crawler_config.json
```

`crawler_config.json` example:
```json
{
  "course_name": "پردازش زبان های طبیعی",
  "course_subtitle": "نیمسال اول سال تحصیلی 04 - 05",
  "HW_list": ["تمرین اول", "تمرین دوم"],
  "HW_name_threshold": 1,
  "headless": false
}
```

## Run
```bash
python main.py
```

Outputs:
- `output/HW_grace.xlsx` (all submissions)
- `output/<HW_name>_submissions.csv` (per homework)

## Notes
- This crawler depends on the current eLearn UI structure and may need updates if the site changes.
- `login_credentials.json` and `crawler_config.json` are intentionally excluded from git.
