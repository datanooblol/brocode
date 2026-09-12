from pathlib import Path
import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description="Use this function when the person asks for reading only a single file"
    )
    parser.add_argument('--path', type=str, required=True, help='a file path')
    return parser

def main():
    args = get_args().parse_args()
    if args.path == 'memory/file1.md':
        text = 'I like the way you look at me.'
    elif args.path == 'memory/file2.md':
        text = 'Cat is the best.'
    else:
        text = "You are the best in the whole world."
    print(text)

if __name__=='__main__':
    main()