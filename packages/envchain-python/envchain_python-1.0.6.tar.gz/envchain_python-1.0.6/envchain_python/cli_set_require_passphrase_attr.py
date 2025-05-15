import argparse
import sys
from envchain_python import re_set_vars, EnvchainError
from envchain_python.config import __version__


def get_parser():
    parser = argparse.ArgumentParser(
        description="Change the 'require passphrase' attribute for all variables in one or more envchain namespaces."
    )
    parser.add_argument(
        "namespaces",
        nargs="*",
        help="Name(s) of namespace(s) to modify. If none provided, read from stdin, one per line.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--enable-require-passphrase",
        action="store_true",
        help="Set variables in the namespace(s) to REQUIRE a passphrase.",
    )
    group.add_argument(
        "--disable-require-passphrase",
        action="store_true",
        help="Set variables in the namespace(s) to NOT require a passphrase.",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.namespaces:
        namespaces_to_process = args.namespaces
    else:
        namespaces_to_process = [line.strip() for line in sys.stdin if line.strip()]

    if not namespaces_to_process:
        parser.error("No namespaces provided via arguments or stdin.")

    require_passphrase_value = False
    if args.enable_require_passphrase:
        require_passphrase_value = True
    elif args.disable_require_passphrase:
        require_passphrase_value = False
    # This else case should not be reached due to the mutually exclusive group being required.

    exit_code = 0
    action_verb = "enabled" if require_passphrase_value else "disabled"

    for ns in namespaces_to_process:
        try:
            print(
                f"Processing namespace '{ns}' to {action_verb} 'require passphrase'..."
            )
            re_set_vars(ns, require_passphrase=require_passphrase_value)
            print(
                f"Successfully {action_verb} 'require passphrase' for all variables in namespace '{ns}'."
            )
        except EnvchainError as e:
            print(
                f"Error processing namespace '{ns}': {e}",
                file=sys.stderr,
            )
            exit_code = 1
        except (
            Exception
        ) as e:  # Catch other potential errors like ValueError from re_set_vars
            print(
                f"An unexpected error occurred while processing namespace '{ns}': {e}",
                file=sys.stderr,
            )
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
