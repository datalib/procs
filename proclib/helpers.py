import shlex


def dispatch_hook(hooks, hook, data):
    if hook in hooks:
        for item in hooks[hook]:
            item(data)
    return data


def str_parse(cmds):
    buff = []
    for item in shlex.split(cmds):
        if item == '|':
            yield buff
            buff = []
            continue
        buff.append(item)

    if buff:
        yield buff


def list_parse(cmds):
    for item in cmds:
        if isinstance(item, str):
            for item in str_parse(item):
                yield item
            continue
        yield list(item)