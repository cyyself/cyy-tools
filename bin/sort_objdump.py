#!/usr/bin/env python3
import sys
import re

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sort objdump -S output by symbol name')
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file (default: stdin)')
    parser.add_argument('output_file', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                        help='Output file (default: stdout)')
    args = parser.parse_args()

    infile = args.input_file
    outfile = args.output_file

    symbol_re = re.compile(r'^([0-9a-fA-F]+)\s+<([^>]+)>:$')

    current_symbol = None
    symbols = {}
    content_before_symbols = []
    content_after_symbols = []
    in_symbol_section = False

    for line in infile:
        line = line.rstrip('\n')
        m = symbol_re.match(line)
        if m:
            address = m.group(1)
            symbol_name = m.group(2)
            current_symbol = symbol_name
            in_symbol_section = True
            if symbol_name not in symbols:
                symbols[symbol_name] = []
            symbols[symbol_name].append(line)
        else:
            if in_symbol_section and current_symbol:
                symbols[current_symbol].append(line)
            else:
                if not in_symbol_section:
                    content_before_symbols.append(line)
                else:
                    content_after_symbols.append(line)

    # Output content before symbols
    for line in content_before_symbols:
        print(line, file=outfile)

    # Sort the symbols by name
    for symbol_name in sorted(symbols.keys()):
        for line in symbols[symbol_name]:
            print(line, file=outfile)

    # Output any remaining content after symbols
    for line in content_after_symbols:
        print(line, file=outfile)

if __name__ == '__main__':
    main()
