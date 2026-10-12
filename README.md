# COVID-19 Data Pipeline

![CI](https://github.com/prabhu2605/covid-pipeline/actions/workflows/ci.yml/badge.svg)

An ETL pipeline that turns the public cumulative COVID-19 case/death time
series into clean daily counts, a global daily summary, and a top-countries
ranking, loaded into a SQLite warehouse.

## Data source

[`datasets/covid-19`](https://github.com/datasets/covid-19): daily cumulative
Confirmed/Recovered/Deaths per country, Jan 2020 - Apr 2022, 199 countries,
about 160k rows.

## The data-quality problem this solves

Cumulative counts sometimes *decrease* when a country revises its reporting.
A plain `diff()` would then yield negative "new cases". The transform clips
these corrections to zero, then adds a 7-day rolling average to smooth
day-of-week reporting noise.

## Setup

```bash
git clone https://github.com/prabhu2605/covid-pipeline.git
cd covid-pipeline
pip install -r requirements.txt
cp .env.example .env
```

## Usage

```bash
python -m src.pipeline
```

## Output tables (in `data/warehouse.db`)

| Table | Contents |
|---|---|
| `country_daily` | date, country, new cases, new deaths, 7-day average |
| `global_daily` | worldwide new cases per day |
| `top_countries` | top N countries by latest confirmed count |

## Testing

```bash
ruff check .
pytest
```

## Engineering practices

- Issue-driven development: every change starts as an issue and ships as a PR
- Protected `main`: PR required, CI must pass, squash merges only
- GitHub Actions runs lint, tests, and a pipeline smoke test on every PR
- Dependabot keeps dependencies and Action versions current