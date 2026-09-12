from pathlib import Path
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description="Use this function when the person asks for reading all files in a directory"
    )
    parser.add_argument('--path', type=str, required=True, help='a directory path')
    return parser

def main():
    args = get_args().parse_args()
    text = "file1.md: I like the way you look at me.\nfile2.md: Cat is the best."
    print(text)

if __name__=='__main__':
    main()