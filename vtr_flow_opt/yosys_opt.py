import argparse
import sys

def gen_yosys_srcipt(
        verilogFiles: str, 
        output_script: str, 
        outputVerilog: str=None, 
        outputBlif: str=None,
        opt: bool=False, 
        topModule: str=None
    ):

    vtr_dir = "/mnt/c/Users/new/Desktop/vtr-verilog-to-routing/"
    script = ""


    script += f"read_verilog -sv {verilogFiles}/*.v\n"

    if opt:
        if topModule is not None:
            script += "hierarchy -check -top " + topModule + "\n"
        else:
            script += "hierarchy -check\n"
        script += "proc\n"
        script += "opt -nodffe -nosdff\n"  # this is to remove flip-flops
        # map reg[] to DFF, should be done before flatten and maps (because this will create new modules)
        script += "memory\n"
        script += f"techmap\n"
        script += "flatten -wb\n"
        script += "dfflibmap -liberty " + vtr_dir + "yosys/examples/cmos/cmos_cells.lib\n"
        script += "clean\n"
    else:
        script += "synth -top " + topModule + "\n"
    if outputVerilog is not None:
        script += "write_verilog " + outputVerilog + "\n"
    script += "stat\n"
    if outputBlif is not None:
        script += "write_blif " + outputBlif + "\n"
    
    file = open(output_script, 'w')
    file.write(script)
    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--v', type=str)
    parser.add_argument('--os', type=str)
    parser.add_argument('--ov', type=str, default=None)
    parser.add_argument('--ob', type=str, default=None)
    parser.add_argument('--opt', type=bool, default=False)
    parser.add_argument('--top', type=str, default=None)
    args = parser.parse_args()
    gen_yosys_srcipt(
        verilogFiles=args.v,
        output_script=args.os,
        outputVerilog=args.ov,
        outputBlif=args.ob,
        opt=args.opt,
        topModule=args.top,
    )
    