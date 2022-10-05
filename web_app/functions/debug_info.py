from inspect import getframeinfo, stack


def debug_info(message):
    caller = getframeinfo(stack()[1][0])
    print(f'{caller.filename}: line {caller.lineno}, in {caller.function}\n\t{message}')
