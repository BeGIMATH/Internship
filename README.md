# Benchmark of embedded python code on C++

## How to compile

Create and activate appropriate conda environment

```bash
conda env create -f environment.yml
```
Compile the benchmark

```bash
cd task1
mkdir build ; cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make -j 8
```

Execute the benchmark
''
```bash
cd ../run
bash execute.sh
```
