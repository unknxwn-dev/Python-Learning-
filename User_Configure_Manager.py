import re 

test_settings = {

    " ": " ",
}

def add_setting(setting, pair):
    pair_key = pair[0].lower()
    pair_value = pair[1].lower()

    if pair_key in setting:
        return(f"Setting \'{pair_key}\' already exists! Cannot add a new setting with this name.")
    else:
        setting[pair_key] = pair_value
        return(f"Setting \'{pair_key}\' added with value \'{pair_value}\' successfully!")

def update_setting(setting, pair):
    pair_key = pair[0].lower()
    pair_value = pair[1].lower()
    if pair_key in setting:
        setting[pair_key] = pair_value 
        return(f"Setting \'{pair_key}\' updated to \'{pair_value}\' successfully!")
    else:
        return(f"Setting \'{pair_key}\' does not exist! Cannot update a non-existing setting.")

def delete_setting(setting, pair):
    pair_key = pair.lower()

    if pair_key in setting:
        setting.pop(pair_key)
        return(f"Setting \'{pair_key}\' deleted successfully!")
    else:
        return(f"Setting not found!")

def view_settings(setting):
    if setting == {}:
        return("No settings available.")
    else:

        string = "Current User Settings:\n"

        for key, item in setting.items():
            string += key.capitalize()
            string += ": "
            string += item.lower()
            string += "\n"
        return string


print(add_setting({'HEY': "HI"}, ('THEME','DARK')))
