# Near-Earth Objects

A command-line tool to inspect and query close approaches of near-Earth objects (NEOs),
using data from NASA/JPL's Center for Near Earth Object Studies. It reads NEO data from
a CSV file and close-approach data from a JSON file, builds structured Python objects,
and supports filtering, result limiting, and structured export.

## Usage

```bash
python main.py inspect --pdes 433
python main.py inspect --name Halley

python main.py query --date 2020-01-01 --max-distance 0.1 --min-velocity 5 --hazardous
python main.py query --start-date 2020-01-01 --end-date 2020-12-31 --limit 20 --outfile results.csv

python main.py interactive
```

### Query filters

| Filter | Meaning |
|--------|---------|
| `--date` / `--start-date` / `--end-date` | Approach occurs on / on-or-after / on-or-before a date |
| `--min-distance` / `--max-distance` | Approach distance in astronomical units |
| `--min-velocity` / `--max-velocity` | Relative velocity in km/s |
| `--min-diameter` / `--max-diameter` | NEO diameter in km |
| `--hazardous` / `--not-hazardous` | Whether NASA flags the NEO as potentially hazardous |
| `--limit` | Cap the number of results |
| `--outfile` | Write results to a `.csv` or `.json` file (otherwise print) |

Data files default to `data/neos.csv` and `data/cad.json`; override with `--neofile`
and `--cadfile`.

## Structure

```
main.py        # CLI entry point and argument parsing
extract.py     # Read NEOs and close approaches from CSV/JSON
models.py      # NearEarthObject and CloseApproach classes
database.py    # In-memory database linking NEOs to their approaches
filters.py     # Attribute filters and result limiting
write.py       # Export results to CSV/JSON
helpers.py     # Datetime parsing/formatting helpers
tests/         # Unit tests
```

## Tests

```bash
python -m unittest
```
