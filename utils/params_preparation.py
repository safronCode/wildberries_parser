import tomllib

def _read_toml_configuration(path: str) -> dict:
    with open(path, "rb") as file:
        config = tomllib.load(file)
    return config

def _get_toml_table(name: str) -> dict:
    with open("config.toml", "rb") as file:
        configuration = tomllib.load(file)

    return configuration.get(name, {})

def get_toml_tables(tables: list[str], path: str = "config.toml") -> dict:
    config = _read_toml_configuration(path)

    return {k: v for k, v in config.items() if k in tables}
