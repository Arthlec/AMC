import os


if __name__ == '__main__':
    print(os.path.realpath(__file__))
    print(os.path.dirname(os.path.realpath(__file__)))