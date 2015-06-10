import re
import sys
from glob import glob
from os.path import basename


def validate_file(file_path):
    file = open(file_path, "r", encoding="UTF-8")
    line_number = 0
    ok = True
    for line in file:
        try:
            line_text = line.replace('\n', '')
            line_number = line_number + 1
            split_text = line_text.split(' = ')
            left_text = split_text[0].strip('"')  # tira os espacos e as aspas do inicio e do fim da string
            right_text = split_text[1].strip('"')  # tira os espacos e as aspas do inicio e do fim da string

            count_percent_left = left_text.count('%')
            count_percent_right = right_text.count('%')

            if(count_percent_left != count_percent_right and right_text):
                ok = False
                print('#  ERROR: line [{0}] missing "%" char. See: {1}'.format(str(line_number), line_text).encode('utf8'))
        except UnicodeEncodeError as errUnicode:
            ok = False
            print("#  EXCEPTION: {0} at line [{0}] ".format(errUnicode, str(line_number)))

    file.close()
    if ok:
        print("  Translation OK")
        exit(0) 
    else:
        print()
        exit(-1) 


def main():
    args = sys.argv[1:]

    if len(args) > 1:
        print(re.sub('validateTra', sys.argv[0], __doc__))
        sys.exit(-1)

    if args:
        filename = args[0]
    else:
        filename = 0

    validate_file(filename)


if __name__ == "__main__":
    main()