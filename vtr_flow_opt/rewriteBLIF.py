
def rewriteBlif(inputFile: str, outputFile: str):
    """
    Carmine's code (31.05.2024)
    """
    import re

    with open(inputFile, "r") as f:
        lines = f.readlines()

    with open(outputFile, "w") as f:
        change_count = 0
        for line in lines:
            if "DFF" in line:
                if "DFFSR" in line:
                    module_name = "DFFSR"
                    continuation = " R=(.+) S=(.+)"
                else:
                    module_name = "DFF"
                    continuation = ""

                reg_pattern = "\.subckt {0} C=(.+) D=(.+) Q=(.+){1}".format(
                    module_name, continuation
                )
                matches = re.findall(reg_pattern, line)
                change_count += 1
                clock = matches[0][0]
                input = matches[0][1]
                output = matches[0][2]
                line = ".latch {0} {1} re {2} 3\n".format(input, output, clock)
            f.write(line)
        print(f"{change_count} units have been changed!")
    # graph = read_blif(inputFile)
    # write_blif(graph, outputFile)

def rewriteBlifLatch(inputFile: str, outputFile: str):
    import re

    with open(inputFile, "r") as f:
        lines = f.readlines()

    with open(outputFile, "w") as f:
        change_count = 0
        for line in lines:
            if "latch" in line:
                # for example: .latch      n1132 cur_state[0]  2
                reg_pattern = "\.latch\s+(.+)\s+(.+)\s+(.+)"
                matches = re.findall(reg_pattern, line)
                input = matches[0][0]
                output = matches[0][1]
                type = matches[0][2]
                if type != "3":
                    change_count += 1
                    clock = "ap_clk"
                    line = ".latch {0} {1} re {2} 3\n".format(input, output, clock)

            f.write(line)
        print(f"{change_count} units have been changed!")


import sys
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--ib', type=str)
    parser.add_argument('--ob', type=str)
    parser.add_argument('--stage', type=str)
    args = parser.parse_args()
    if args.stage == "yosys":
        rewriteBlif(args.ib, args.ob)
    elif args.stage == "abc":
        rewriteBlifLatch(args.ib, args.ob)
