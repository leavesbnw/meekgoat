from core import base


def main():
    banner = """
                      __                         __   
 _____   ____   ____ |  | __  ____   _________ _/  |_ 
/     \_/ __ \_/ __ \|  |/ / / ___\ /  _ \__  \\\\   __\\
|  Y Y  \  ___/\  ___/|    < / /_/  >  <_> ) __ \|  |
|__|_|  /\___  >\___  >__|_ \\___  / \____(____  /__|
      \/     \/     \/     \/_____/            \/

                 Welcome to MeekGoat Console!
"""
    mg = base.Base()
    mg.cmdloop(intro=banner)

if __name__ == '__main__':
    main()
