If you are using `uv`, you can run any example with the following command:
```sh
uv run --group examples path/to/example
```

The `--group examples` option tells `uv` to use the additional dependencies specified in the `examples` dependency group in `pyproject.toml`. For example:
```sh
uv run --group examples ./examples/full_workflow.py
```
