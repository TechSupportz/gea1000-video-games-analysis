# GEA1000 Part B: video games analysis

Code and output for Part B Q2, Q3 and Q5 of our GEA1000 group project. Everything is in `analysis.ipynb`, which reads `data/Video_games_dataset.csv` (one row per title–console record, sales in millions of copies).

Quartiles, SD and outliers follow the GEA1000 lecture notes, not the pandas/matplotlib defaults. See the Setup cell.

## Running

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run jupyter nbconvert --to notebook --execute --inplace analysis.ipynb
```

Or open `analysis.ipynb` in Jupyter / VS Code with the `.venv` kernel and Run All. Tables and charts are saved to `output/q2/`, `output/q3/` and `output/q5/`.
