import re


def clear_text(s: str, allow_digits: bool = True, allow_spaces: bool = True, allow_rus: bool = False,
               allow_other: str = '') -> str:
    """
    Leaves only necessary symbols in the string.
    Necessary symbols by default: big and small English characters

    In any case all leading and ending spaces deleted and more then 1 space in the middle.

    Options:

    allow_digits: allow digits 0-9
    allow_spaces: allow 1 space in string
    allow_rus: allow russian letters а-яА-Я
    other_allow: string of  another allowed symbols

    """
    allows = "[^A-Za-z{}{}{}{}]"
    digits = '\d' if allow_digits else ''
    rus = 'а-яА-Я' if allow_rus else ''
    spaces = ' ' if allow_spaces else ''
    # other = ''.join(allow_other)

    allows = allows.format(digits, spaces, rus, allow_other)
    # print(allows)

    if allow_spaces:
        s = ' '.join(s.split())

    return re.sub(allows, '', s).strip()


def main():
    s = ' N(*y9hoЛРЛл         лллл igu   jgkjkU*Y    '
    print(clear_text(s, allow_digits=True, allow_rus=True, allow_spaces=True, allow_other='*'))


if __name__ == "__main__":
    main()
