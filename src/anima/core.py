import cmd
import traceback
from bdb import BdbQuit
from importlib.metadata import version

from anima import commands


def parse(args: str) -> tuple[int, ...]:
    """Convert a series of zero or more numbers to an argument tuple."""
    return tuple(map(int, args.split()))


class AnimaShell(cmd.Cmd):
    intro = f"Engaging Anima toolkit (v{version('anima-utils')})"
    prompt = "(anima) "

    def default(self, usr_str: str) -> None:
        print(f"Input '{usr_str}' not recognized.")

    def do_atk(self, args: str) -> None:
        "usage: atk attack_roll defense_roll [armor] [base_damage]"
        print(commands.attack.calc_attack(*parse(args)))

    def do_combo(self, _: str) -> None:
        "usage: combo"
        print(commands.combo())

    def do_crit(self, args: str) -> None:
        "usage: crit level phr_roll [location_id]"
        print(commands.crit(*parse(args)))

    def do_mass(self, args: str) -> None:
        "usage: mass [num] [lp] [damage_resistant = 0 | 1]"
        count, lp, dr = parse(args)
        if str(dr) in ["1", "true", "True"]:
            result = commands.mass(count, lp, dr=True)
        elif str(dr) in ["0", "false", "False"]:
            result = commands.mass(count, lp, dr=False)
        else:
            raise ValueError(f"Value for `dr` must be truthy or falsy. Got: {dr}")
        print(result)

    def do_powers(self, args: str) -> None:
        "usage: powers [num_powers = 5]"
        print(commands.powers(*parse(args)))

    def do_shuffle(self, args: str) -> None:
        "usage: shuffle [targets...]"
        print(commands.shuffle(args.split(" ")))

    def do_exit(self, _: str) -> None:
        "terminate session"
        print("Ending session")
        raise KeyboardInterrupt


def main() -> None:
    while True:
        try:
            AnimaShell().cmdloop()
        except (KeyboardInterrupt, BdbQuit):
            raise SystemExit(0)
        except:
            traceback.print_exc()


if __name__ == "__main__":
    main()
