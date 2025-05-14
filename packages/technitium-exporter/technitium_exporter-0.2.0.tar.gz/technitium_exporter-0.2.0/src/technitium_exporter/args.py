from configargparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--address", help="Interface to listen on", default="0.0.0.0", env_var="ADDRESS")
    parser.add_argument("--port", help="Port number to listen on", type=int, default=9080, env_var="PORT")
    parser.add_argument("--token", help="Technitium API token", required=True, env_var="TECHNITIUM_TOKEN")
    parser.add_argument("--url", help="Technitium server URL", required=True, env_var="TECHNITIUM_URL")
    parser.add_argument("--all-record-types", help="Include counts for all record types, not just the common ones",
                        action="store_true", default=False)
    return parser.parse_args()
