# CTWedge Interface

This directory contains a simple parser for parsing the input models in the language of [CTWedge](https://github.com/fmselab/ctwedge), with the following features: 
- This parser is implemented in plain C++. 
- While CTWedge should have its own parser, this parser is an independent re-implementation and may be integrated into other projects. 
- This parser supports parsing the input model file and then converting the parsed model into CNF-encoded format by [Tseitin transformation](https://en.wikipedia.org/wiki/Tseytin_transformation), which can be then handled by combinatorial interaction testing tools like *SamplingCA* or *CAmpactor*. 

The language accepted by CTWedge is described in [its Github wiki page](https://github.com/fmselab/ctwedge/wiki/Grammar). 

## Known Issues

- Currently this parser can only recognize a subset of the full CTWedge language. Nonetheless, it is able to parse most of the regular input (*e.g.,* those in [this repository](https://github.com/fmselab/CIT_Benchmark_Generator)). 
- Sometimes the result of parsing will contain much redundancy, which may affact negatively the size of PCA. 
