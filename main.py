from actions import show_settings, change_settings, start_parsing

if __name__ == '__main__':
    actions = {
        "1": show_settings,
        "2": change_settings,
        "3": start_parsing,
        "0": exit
    }

    while True:
        print("\n====== Menu ======\n"
              "1. Show current settings\n"
              "2. Change settings\n"
              "3. Start parsing \n"
              "0. Exit \n")

        choice = input("Select an option: ").strip()

        action = actions.get(choice)
        if action:
            result = action()

        else:
            print("Invalid option. Try again.\n")
