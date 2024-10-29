#!/usr/bin/env python3
import sys
import re

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Sort objdump -S output by symbol name')
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file (default: stdin)')
    args = parser.parse_args()

    infile = args.input_file

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

    for symbol_name in symbols.keys():
        outfile = open(symbol_name + '.s', 'w')
        for line in symbols[symbol_name]:
            print(line, file=outfile)

if __name__ == '__main__':
    main()
