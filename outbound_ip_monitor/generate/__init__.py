#!/usr/bin/env python

import argparse
import json
import sys
from collections import defaultdict

import dns.resolver


def get_entries(domain) -> list[str]:
    entries = list()

    try:
        answers = dns.resolver.resolve(domain, "A")
        for rdata in answers:
            entries.append(rdata.to_text())
    except dns.resolver.NoAnswer:
        print(f"No answer found for {domain} with record type A.")
        return []
    except dns.resolver.NXDOMAIN:
        print(f"Domain {domain} does not exist.")
        return []

    entries.sort()
    return entries


def generate(domains=list(), output="output.txt", format="txt"):
    if output == "-":
        f = sys.stdout
    else:
        f = open(output, "w")
    with f:
        all_entries = defaultdict(list)
        for domain in domains:
            all_entries[domain] = get_entries(domain)
        if format == "txt":
            for domain, records in all_entries.items():
                f.write(f"# {domain}\n")
                for record in records:
                    f.write(f"{record}\n")
        elif format == "json":
            f.write(json.dumps(all_entries))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--domains",
        default=[],
        help="List of domains",
        type=lambda t: [s.strip() for s in t.split(",")],
    )
    parser.add_argument("-o", "--output", default="output.txt", help="Output file")
    parser.add_argument("-f", "--format", default="txt", help="Output format")
    args = parser.parse_args()

    if len(args.domains) == 0:
        print("No domains provided")
        parser.print_help()
        sys.exit(1)

    generate(domains=args.domains, output=args.output, format=args.format)


if __name__ == "__main__":
    main()
