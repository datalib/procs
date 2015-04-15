from contextlib import contextmanager
from subprocess import Popen, PIPE
from procs.response import Response


def dispatch_hook(hooks, hook, data):
    if hook in hooks:
        for item in hooks[hook]:
            item(data)
    return data


class Process(object):
    def __init__(self, command, hooks={}, data=None, **opts):
        self.popen = Popen(args=command, **opts)
        self.command = command
        self.hooks = hooks
        self.data = data

    def dispatch(self, hook):
        dispatch_hook(self.hooks, hook, self.popen)

    @contextmanager
    def popen_context(self):
        yield self.popen
        if self.popen.returncode != 0:
            self.dispatch('error')
            return
        self.dispatch('success')

    def run(self):
        with self.popen_context() as popen:
            stdout, stderr = popen.communicate(self.data)
            status = popen.wait()
            return Response(
                    command=self.command,
                    process=popen,
                    stdout=stdout,
                    stderr=stderr,
                    returncode=status,
                    pid=popen.pid,
                    )

    def __repr__(self):
        return '<Process [%s]>' % ' '.join(self.command)
