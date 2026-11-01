download:
    uv run python3 -m script.download
    @echo "Next: optionally trim intros/outros manually, then run 'just rename' to clean the metadata and rename the files."

rename:
    uv run python3 -m script.add_metadata
    @echo "Next: verify the files in the output directory. You can now move the tracks into your backup playlist."
