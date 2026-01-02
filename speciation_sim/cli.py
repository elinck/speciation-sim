import argparse
import csv
import sys
from pathlib import Path
from speciation_sim.models import (
    run_allopatry,
    run_parapatry,
    run_periodic,
)

def write_result(path, result):
    path = Path(path)
    write_header = not path.exists()

    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=result.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(result)

def main():
    try:
        # existing argparse + simulation code
        ...
    except KeyboardInterrupt:
        print("\nSimulation interrupted by user.")
        return 130  # standard SIGINT exit code
    parser = argparse.ArgumentParser(
        description="Speciation simulations under allopatry, parapatry, and periodic migration")

    parser.add_argument("--model", choices=["allopatry", "parapatry", "periodic"], required=True, help="Speciation model")

    parser.add_argument("--N", type=int, metavar="<int>", required=True, help="Diploid population size")
    parser.add_argument("--mu", type=float, metavar="<float>", required=True, help="Mutation rate")
    parser.add_argument("--s", type=float, metavar="<float>", required=True, help="Selection coefficient")
    parser.add_argument("--gen-max", type=int, metavar="<int>", default=1000, help="Maximum generations to run")
    parser.add_argument("--m", type=float, metavar="<float>", default=0.0,
                        help="Migration rate (parapatry / periodic only)")
    parser.add_argument("--interval", type=int, metavar="<int>", default=50,
                        help="Generation interval for periodic switching")
    parser.add_argument("--out", type=Path, metavar="<Path>",  default=Path.cwd() / "results.csv",
                        help="Output CSV file path (default: ./results.csv)")

    args = parser.parse_args()

    if args.model == "allopatry":
        t, completed = run_allopatry(args.N, args.mu, args.s, args.gen_max)

    elif args.model == "parapatry":
        t, completed = run_parapatry(args.N, args.mu, args.s, args.m, args.gen_max)

    elif args.model == "periodic":
        t, completed = run_periodic(
            args.N, args.mu, args.s, args.m,
            args.interval, args.gen_max
        )

    result = {
            "regime": args.model,
            "N": args.N,
            "mu": args.mu,
            "s": args.s,
            "m": None,
            "interval": None,
            "speciation_gen": t,
            "completed": completed
    }

    if args.model == "parapatry":
        result["m"] = args.m

    elif args.model == "periodic":
        result["m"] = args.m
        result["interval"] = args.interval

    write_result(args.out, result)
    return 0

if __name__ == "__main__":
    main()


