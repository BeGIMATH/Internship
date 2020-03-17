# Internship
Internship tests

## How to compile

Create and activate appropriate conda environment

```bash
conda env create -f environment.yml
```
Compile task1

```bash
cd task1
mkdir build ; cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make -j 8
```

Execute 

```bash
./task1
```