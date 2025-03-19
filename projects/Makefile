# Customize the name
PROJECT_NAME = gemm

# Variables
VTR_DIR = /mnt/c/Users/new/Desktop/vtr-verilog-to-routing
YOSYS_DIR = $(VTR_DIR)/yosys
VPR_DIR = $(VTR_DIR)/vpr
ABC_DIR = $(VTR_DIR)/abc
PROJECT_DIR = $(VTR_DIR)/projects/$(PROJECT_NAME)
VERILOG_DIR = $(PROJECT_DIR)/verilog
YOSYS_SCRIPT = $(PROJECT_DIR)/$(PROJECT_NAME).ys
BLIF_FILE = $(PROJECT_DIR)/output/$(PROJECT_NAME)_yosys.blif
RE_BLIF_FILE = $(PROJECT_DIR)/output/$(PROJECT_NAME)_yosys_re.blif
ABC_BLIF_FILE = $(PROJECT_DIR)/output/$(PROJECT_NAME)_abc.blif
RE_ABC_BLIF_FILE = $(PROJECT_DIR)/output/$(PROJECT_NAME)_abc_re.blif
ARCH_FILE = $(VTR_DIR)/projects/vpr_arch_MOD8_tester.xml
TOP_MODULE = $(PROJECT_NAME)

all: env prep yosys abc vpr

# Environment setup
env:
	export PATH=$$PATH:$(YOSYS_DIR)
	export PATH=$$PATH:$(VPR_DIR)

# Prepare output directory
prep:
	mkdir -p $(PROJECT_DIR)/output

# Run Yosys and BLIF optimization
yosys: $(PROJECT_DIR)/output $(VERILOG_DIR) $(VTR_DIR)/vtr_flow_opt/yosys_opt.py $(VTR_DIR)/vtr_flow_opt/rewriteBLIF.py
	python $(VTR_DIR)/vtr_flow_opt/yosys_opt.py --v $(VERILOG_DIR) --os $(YOSYS_SCRIPT) --ob $(BLIF_FILE) --opt true --top $(TOP_MODULE)
	yosys $(YOSYS_SCRIPT)
	python $(VTR_DIR)/vtr_flow_opt/rewriteBLIF.py --ib $(BLIF_FILE) --ob $(RE_BLIF_FILE) --stage yosys

# Run ABC optimization
abc: $(RE_BLIF_FILE) $(VTR_DIR)/vtr_flow_opt/rewriteBLIF.py
	$(ABC_DIR)/abc -c 'read $(RE_BLIF_FILE); if -K 6; write_blif $(ABC_BLIF_FILE)'
	python $(VTR_DIR)/vtr_flow_opt/rewriteBLIF.py --ib $(ABC_BLIF_FILE) --ob $(RE_ABC_BLIF_FILE) --stage abc

# Run VPR
vpr: $(RE_ABC_BLIF_FILE)
	cd $(PROJECT_DIR)/output && vpr $(ARCH_FILE) $(RE_ABC_BLIF_FILE) --pack

# Clean output directory
clean:
	rm -rf $(PROJECT_DIR)/output
