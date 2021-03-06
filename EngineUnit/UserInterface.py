import argparse

def ui()-> argparse.Namespace:
    """
    function to run user interface in the cli to get user input
    :return: object contain the user input in the ui
    """
    menu = argparse.ArgumentParser(
        description='This project should score given open api spec and explain where is the vulnerable fields',
        epilog='\u00a9 2022')
    menu.add_argument('-v', '--verbose', action='store_true', help='show debug information')

    menu.add_argument('-a', '--api_scheme', required=True, type=str,
                      help='path for open api scheme (yaml file)')


    output_group = menu.add_mutually_exclusive_group()

    output_group.add_argument('-r', '--rules' , type=str, help='path for rules file (json file)')
    output_group.add_argument('-d', '--dir_rules', type=str,help='path for rules directory (json file)')

    return menu.parse_args()
