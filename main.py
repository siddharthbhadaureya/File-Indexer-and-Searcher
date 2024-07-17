import sys

import cli as _cli


def main(args: list[str]) -> None:
    cli = _cli.FileIndexerCLI()
    cli.show_results(cli.parse_args(args))


if __name__ == '__main__':
    main(sys.argv[1:])
