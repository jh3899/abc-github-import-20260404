# Show Rendering Optimization Results

This folder stores proof that the `show` rendering path was optimized.

## Machine-validated result

- Baseline Graphviz `dot` render of `i10.dot` to SVG: about `676.462` seconds
- Optimized integrated ABC `show` render of `i10.aig` to SVG: about `3.411` seconds

## Target

- Goal: under `240` seconds
- Achieved: `3.411` seconds

## What changed

- Windows `show` now writes SVG instead of PostScript
- Large DOT files automatically use Graphviz `sfdp` instead of `dot`
- Graphviz path is configured in `abc.rc`
- Visualization limits were raised so larger graphs can be rendered

## Key artifacts

- `engine_benchmark.txt`
- `engine_benchmark_sfdp_variants.txt`
- `integrated_show_timing.txt`
- `i10_dot.svg`
- `i10_sfdp.svg`
- `i10_optimized.svg`
