from argparse import ArgumentParser
from os import system, listdir
from os.path import isfile

parser = ArgumentParser(description="Конвертация .ui файла в .py файл")
parser.add_argument("--source_file", type=str, default="./windows/layouts/message.ui")
parser.add_argument("--resulting_file", type=str, default="./windows/layouts/ui_message.py")
args = parser.parse_args()


def main():
    system(f"pyuic5 {args.source_file} -o {args.resulting_file}")


def convert_all(path="./windows/layouts"):
    for name in listdir(path):
        if isfile(f"{path}/{name}") and name.endswith(".ui"):
            filename, _ = name.split(".")
            system(f"pyuic5 {path}/{filename}.ui -o {path}/ui_{filename}.py")


if __name__ == "__main__":
    # main()
    convert_all()
