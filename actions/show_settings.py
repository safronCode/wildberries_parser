import tomllib


def show_settings():
    """"""
    try:
        with open("config.toml", "rb") as file:
            config = tomllib.load(file)
    except FileNotFoundError:
        config = dict()

    for table, table_vars in config.items():
        print(f"*{table}*\n")
        for key, value in table_vars.items():
            print(f"{key} = {value}")
        print("\n")
    print("\n"*2)
