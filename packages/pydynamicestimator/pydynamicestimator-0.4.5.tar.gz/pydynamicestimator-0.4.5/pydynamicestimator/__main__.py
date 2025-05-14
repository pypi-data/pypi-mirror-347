import argparse
from pydynamicestimator import __version__


def main():
    parser = argparse.ArgumentParser(description="PowerDynamicEstimator CLI")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )


if __name__ == "__main__":
    main()
