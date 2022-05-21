import argparse
import sys

def main():
    args = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Scrap and Process Webpage Text')
    parser.add_argument("target")
    parser.add_argument("-o","--output",action="store")
    parser.add_argument("-a","--append",action="store_true")
    parser.add_argument("-b","--bold",action="store_true")

    arg_dict = vars(parser.parse_args(args))
    print("This is the main function")
    print("args: ", args)
    print("arg_dict: ", arg_dict)

if __name__ == "__main__":
    main()