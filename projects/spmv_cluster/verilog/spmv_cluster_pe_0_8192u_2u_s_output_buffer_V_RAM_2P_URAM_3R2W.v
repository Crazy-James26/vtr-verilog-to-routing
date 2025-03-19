// ==============================================================
// Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2022.2 (64-bit)
// Version: 2022.2
// Copyright 1986-2022 Xilinx, Inc. All Rights Reserved.
// ==============================================================
`timescale 1 ns / 1 ps
module spmv_cluster_pe_0_8192u_2u_s_output_buffer_V_RAM_2P_URAM_3R2W (
     
    address0, ce0,
    
    q0, 
     
    address1, ce1,
    d1, we1, 
    
    
    reset, clk);

parameter DataWidth = 32;
parameter AddressWidth = 13;
parameter AddressRange = 8192;

input[AddressWidth-1:0] address0;
input ce0;

output wire[DataWidth-1:0] q0; 

input[AddressWidth-1:0] address1;
input ce1;
input[DataWidth-1:0] d1;
input we1; 


input reset;
input clk;

(* ram_style = "hls_ultra" , cascade_height = 1 *)reg [DataWidth-1:0] ram[0:AddressRange-1];

wire [AddressWidth-1:0] address0_t0; 
reg  [AddressWidth-1:0] address0_t1;
reg [DataWidth-1:0] q0_t0;
(* retiming_backward = 1 *)reg [DataWidth-1:0] q0_t1; // 

wire [AddressWidth-1:0] address1_t0; 
reg  [AddressWidth-1:0] address1_t1;
wire [DataWidth-1:0] d1_t0; 
wire we1_t0; 
reg [DataWidth-1:0] d1_t1;
reg we1_t1; 





assign address0_t0 = address0;


assign q0 = q0_t1;

assign address1_t0 = address1;

assign d1_t0 = d1;
assign we1_t0 = we1;





always @(posedge clk)  
begin

    if (ce0) 
    begin
        address0_t1 <= address0_t0; 


 
        q0_t1 <= q0_t0;

    end

    if (ce1) 
    begin
        address1_t1 <= address1_t0; 
 
        d1_t1 <= d1_t0;
        we1_t1 <= we1_t0;



    end

end 





always @(posedge clk) 
begin 
    if (ce0) begin
        q0_t0 <= ram[address0_t1];
    end
end 

 


always @(posedge clk)  
begin 
    if (ce1) begin
        if (we1_t1) 
            ram[address1_t1] <= d1_t1; 
    end
end 



 


endmodule

