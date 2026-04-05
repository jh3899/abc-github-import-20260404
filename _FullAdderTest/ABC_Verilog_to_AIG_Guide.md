# ABC Verilog-to-AIG Step-by-Step Guide

This guide shows how to convert a Verilog module into an AIG file with ABC on this machine.

Test workspace:

- `D:\abc-master\_FullAdderTest`

Files used in the test:

- `full_adder_1bit.v`
- `full_adder_1bit.aig`
- `abc_full_adder_transcript.txt`

Important note about Verilog support:

ABC does not accept full modern Verilog syntax. Its `read_verilog` command supports an older IWLS subset.
For that reason, the module header should use a plain port list and the `input`/`output` declarations should appear inside the module body.

Example of ABC-friendly Verilog:

```verilog
module full_adder_1bit (a, b, cin, sum, cout);

input a;
input b;
input cin;
output sum;
output cout;

assign sum = a ^ b ^ cin;
assign cout = (a & b) | (a & cin) | (b & cin);

endmodule
```

## Commands used

From `D:\abc-master`, run:

```powershell
.\_TEST\abc.exe -c "read_verilog _FullAdderTest\full_adder_1bit.v; print_stats; strash; print_stats; write_aiger _FullAdderTest\full_adder_1bit.aig"
```

What each command does:

1. `read_verilog _FullAdderTest\full_adder_1bit.v`
   Reads the Verilog file into ABC.
2. `print_stats`
   Shows the network statistics after import.
3. `strash`
   Converts the logic network into AIG form.
4. `print_stats`
   Shows the AIG statistics after conversion.
5. `write_aiger _FullAdderTest\full_adder_1bit.aig`
   Writes the final AIGER file.

## How to verify the generated AIG

Run:

```powershell
.\_TEST\abc.exe -c "read _FullAdderTest\full_adder_1bit.aig; print_stats"
```

If ABC reads the `.aig` file successfully and prints stats, the export worked.

## Expected result from this tested example

The tested full adder produced an AIG file with:

- 3 inputs
- 2 outputs
- 11 AND nodes
- logic depth 4

## Common pitfall

If you use ANSI-style Verilog such as:

```verilog
module full_adder_1bit (
    input wire a,
    ...
);
```

ABC may fail with an error similar to:

`Expected closing parenthesis after "module".`

If that happens, rewrite the module using the older port-list style shown above.
