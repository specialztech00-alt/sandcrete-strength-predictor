# Model folder

This folder is empty on purpose. Copy these two files from the Colab
notebook's `export/` folder here before running the app:

- `sandcrete_pipeline.pkl`
- `requirements.txt` (use this to update the versions in the project's top-level requirements.txt)

Until `sandcrete_pipeline.pkl` is present, `/predict` and `/explain` will
return a 503 error — this is expected and matches the FileNotFoundError
message you'll see in the terminal.
