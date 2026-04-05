# Show Rendering Optimization Results

This folder stores proof that the `show` rendering path was optimized.

## Machine-validated result

- Baseline Graphviz `dot` render of `i10.dot` to SVG: about `676.462` seconds
- First fast integrated ABC `show` render of `i10.aig` to SVG: about `3.411` seconds
- Readability-optimized integrated ABC `show` render of `i10.aig` to SVG: about `4.371` seconds

## Target

- Goal: under `240` seconds
- Achieved: `4.371` seconds with the readability-optimized layout

## What changed

- Windows `show` now writes SVG instead of PostScript
- Large DOT files automatically use Graphviz `sfdp` instead of `dot`
- Large graph rendering now removes the old DOT size cap so the SVG is not squeezed into a tiny canvas
- Large graph rendering uses spacing-oriented `sfdp` flags to spread nodes out more
- Graphviz path is configured in `abc.rc`
- Visualization limits were raised so larger graphs can be rendered

## Key artifacts

- `engine_benchmark.txt`
- `engine_benchmark_sfdp_variants.txt`
- `integrated_show_timing.txt`
- `integrated_show_timing_readable.txt`
- `i10_dot.svg`
- `i10_sfdp.svg`
- `i10_optimized.svg`
- `i10_readable_optimized.svg`
