import sys
import inspect

def cli_this(module_name, f_prefix="", build_manual=False):

    if build_manual:
        all_f_map = {}
        for m,o in inspect.getmembers(sys.modules[module_name]):
            if inspect.isfunction(o) and m.startswith(f_prefix):
                f_name = m[len(f_prefix):]
                all_f_map[f_name] = o

        lines = []
        for f_current in sorted(all_f_map.keys()):
            f_sig = inspect.signature(all_f_map[f_current])
            f_doc = inspect.getdoc(all_f_map[f_current])
            lines.append("FUNCTION %s" % f_current)
            lines.append(str(f_sig))
            lines.append(str(f_doc))
            lines.append("")
        return "\n".join(lines)

    if len(sys.argv) <= 1:
        print("No args given")
        sys.exit(1)
        return

    action = sys.argv[1]
    opts = sys.argv[2:]
    f_actual = None

    for m,o in inspect.getmembers(sys.modules[module_name]):
        if inspect.isfunction(o) and m.startswith(f_prefix) and m == f_prefix+action:
            f_actual = o
            break

    if f_actual is not None:
        # f_actual()
        #print("would call %s with %s" % (f_actual, str(opts)))
        f_actual(*opts)
        sys.exit(0)
    else:
        print("unknown action %s" % action)
        sys.exit(1)
