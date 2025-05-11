#stv_copy
#entry  point: cf
#copy from

from sys import argv, stdout, stderr
from base64 import b64encode

red = '\x1b[31m'
green = '\x1b[32m'
gold = yellow = '\x1b[33m'
purple = '\x1b[95m'
blue = '\x1b[34m'
cyan = '\x1b[96m'
grey = '\033[90m'
endc = '\x1b[0m'

def output(info, mode = None, e = None):
    e = '' if e is None else e
    if mode is None and e is None:
        stdout.write(f"{green}|>{info}\n")
    elif mode.lower() == 'error':
        stderr.write(f"{red}[{mode}] {purple}{info}\n{grey}{e}\n")
    elif mode.lower() != 'success':
        stdout.write(f"|>{green}{mode}: {endc}{info}\n")
    else:
        stdout.write(f"{gold}[{mode}] {cyan}{info}\n")
    stdout.write(f"{endc}")

def copy_to_clipboard(filename):
    try:
        with open(filename, 'rb') as f:
            content = f.read()
    except Exception as e:
        output(f"无法读取文件: '{argv[1]}'", mode = 'Error', e=e)
        return False

    b64_content = b64encode(content).decode('ascii')
    osc52_seq = f'\033]52;c;{b64_content}\a'

    try:
        stdout.write(osc52_seq)
        stdout.flush()
    except Exception as e:
        output(f"无法将内容复制到剪贴板", mode = 'Error', e=e)
        return False

    return True

def main():
    if len(argv) != 2:
        output(f"使用方法: {argv[0]} <filename>", mode = 'Tips')
        return

    if copy_to_clipboard(argv[1]):
        output("已将内容复制到剪贴板", mode = 'Success')
    return

        
if __name__ == '__main__':
    main()
