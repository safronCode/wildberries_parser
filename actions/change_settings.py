import tomllib


def change_settings():
    try:
        with open("config.toml", 'rb') as file:
            config = tomllib.load(file)

    except FileNotFoundError:
        config = {}

    table_name = input("Table name: ")
    key_name = input("Key name: ")
    value = input("Value: ")
    if value.isdigit():
        value = int(value)

    if table_name not in config:
        config[table_name] = {}

    config[table_name][key_name] = value
    with open("config.toml", 'w', encoding="utf-8") as file:
        for table, table_vars in config.items():
            file.write(f"[{table}]\n")
            for key, value in table_vars.items():
                if isinstance(value, str):
                    file.write(f'{key} = "{value}"')
                else:
                    file.write(f"{key} = {value}")
                file.write("\n")
        print("Config changed")