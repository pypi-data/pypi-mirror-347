import os
import sys
import cmd
import optparse
import bucho

# Only supports Python 3.10 and later
import importlib.metadata as metadata

description = """
Actions are commands like "show", "latest_status" and "all_status".
If -i is specified or no action is specified on the command line, a
"shell" interpreting actions typed interactively is started. Use the
action "help" to find out about available actions.
"""

bucho_encoding = sys.stdout.encoding
if not bucho_encoding:
    bucho_encoding = "utf-8"


def load_plugins(group_name, distribution_name=None):
    """Plugin loader for Python 3.10 and later

    Args:
        group_name (str): The entry point group name
        distribution_name (str, optional): Specified when filtering by a specific package name

    Returns:
        dict: Mapping of plugin names to loaded functions
    """
    plugins = {}
    entry_points = metadata.entry_points().select(group=group_name)

    if distribution_name:
        entry_points = [
            ep
            for ep in entry_points
            if ep.dist is not None and ep.dist.name == distribution_name
        ]

    # Load plugins
    for ep in entry_points:
        plugins[ep.name] = ep.load()

    return plugins


class BuchoOptions:
    def __init__(self):
        programname = os.path.basename(sys.argv[0])
        base, ext = os.path.splitext(programname)
        if ext == ".py":
            if base.endswith("-script"):
                base = base[:-7]
            programname = base
        sys.argv[0] = programname

        usage = "usage: %prog [options] command"
        parser = optparse.OptionParser(usage=usage, description=description)
        parser.add_option(
            "-i",
            "--interactive",
            help="start an interactive shell after executing commands",
            dest="interactive",
            action="store_true",
            default=False,
        )

        parser.add_option(
            "-p",
            "--prompt",
            help="prompt string",
            dest="prompt",
            action="store",
            default=(programname + ">"),
        )
        parser.add_option(
            "--plugin", help="command plugin", dest="plugin", action="store"
        )
        self.options, self.args = parser.parse_args()

        if not self.args and not self.options.interactive:
            self.options.interactive = 1

    def __getattr__(self, name):
        if hasattr(self.options, name):
            return getattr(self.options, name)
        raise AttributeError(name)

    def __add__(self, obj):
        return obj


class BuchoCmd(cmd.Cmd):
    def __init__(self, options):
        self.options = options
        self.prompt = self.options.prompt + " "
        if getattr(self.options, "plugin"):
            cls = self.__class__
            dist_name = self.options.plugin
            plugin_functions = load_plugins("bucho.commands", dist_name)
            for name, func in plugin_functions.items():
                setattr(cls, "do_" + name, makeplugincmd(name, func))

        cmd.Cmd.__init__(self)

    def do_quit(self, arg):
        return 1


def makeplugincmd(n, func):
    def f(self, arg):
        t = func()
        print(t)
        return 0

    return f


def makecmd(n):
    def f(self, arg):
        t = getattr(bucho, n)()
        print(t)
        return 0

    return f


for name in ["show", "latest_status", "all_status", "torumemo", "show_gui"]:
    setattr(BuchoCmd, "do_" + name, makecmd(name))


def main(options=None, cmdclass=BuchoCmd):
    try:
        if options is None:
            options = BuchoOptions()
        c = cmdclass(options)
    except Exception as e:
        print(e)
        return

    if options.args:
        c.onecmd(" ".join(options.args))

    if options.interactive:
        import importlib.util

        if importlib.util.find_spec("readline"):
            import readline  # noqa
        c.cmdloop()


def console():
    main()


if __name__ == "__main__":
    main()
