# GEA1000: video games analysis

Code and output for our GEA1000 group project. Part B (Q2, Q3 and Q5) is in `part_b.ipynb`; Part C (multiplayer support and commercial success) is in `part_c.ipynb`. Both read `data/Video_games_dataset.csv` (one row per title–console record, sales in millions of copies).

Part C combines console versions of the same title before comparing groups, using the helpers in `part_c/`.

Quartiles, SD and outliers follow the GEA1000 lecture notes, not the pandas/matplotlib defaults. See the Setup cell.

## Running

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv sync
uv run jupyter nbconvert --to notebook --execute --inplace part_b.ipynb
uv run jupyter nbconvert --to notebook --execute --inplace part_c.ipynb
```

Or open either notebook in Jupyter / VS Code with the `.venv` kernel and Run All. Part B saves tables and charts to `output/q2/`, `output/q3/` and `output/q5/`; Part C saves them to `part_c/figures/` and `part_c/tables/`.
