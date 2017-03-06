# HiCOrient

__HiCOrient__ is a tool that uses HiC chromatin interaction data to orient a collection of ordered scaffolds. The process of achieving a 
chromosome scale assembly from a draft assembly often involves 3 steps:

1. Clustering of scaffolds into pseudo molecules/chromosomes
2. Ordering the scaffolds within each chromosome
3. Orienting the clustered and ordered scaffolds.

HiCOrient can be used when a genetic map was able to cluster and order most scaffolds, but not able to orient most scaffolds.

# Installing HiCOrient
## Platforms

- Linux
- Mac OSX

## Dependencies

- python2.7
- numpy
- cython
- A particular branch of scipy that includes functionality fo permutation F tests.

The following instructions are an example of how to install these dependencies,
and then HiCOrient. I recommend using a virtual environment, especially considering
the dependency on an unmerged branch of scipy.

## Installing From Source
The only way to install HiCOrient is from source. To install, execute the following commands:

```
$ virtualenv VE
$ . VE/bin/activate
(VE)$ pip install numpy
(VE)$ pip install cython
(VE)$ git clone -b anova https://github.com/malonge/scipy
(VE)$ cd scipy
(VE)$ python setup.py install
(VE)$ cd ..
(VE)$ git clone https://github.com/malonge/HiCOrient
(VE)$ cd HiCOrient
(VE)$ python setup.py install
```

# Command Line Usage
## HiCOrient.py
```
usage: HiCOrient.py [-h] [-n 30] [-m 100000] [--cheatWith orientations.txt]
                    <scaffolds.txt> <alignments.sam> [<alignments.sam> ...]

Orient anchored/ordered scaffolds with chromatin interaction data.

positional arguments:
  <scaffolds.txt>       An ordered list of scaffolds. First column is scaffold
                        header, second is scaffold length.
  <alignments.sam>      SAM files containing HiC alignments to the specified
                        scaffolds.

optional arguments:
  -h, --help            show this help message and exit
  -n 30                 The minimum HiC event sample size needed to perform a
                        F-test. Default = 30
  -m 100000             The minimum scaffold size for consideration in phase
                        2. Default = 100000
  --cheatWith orientations.txt
                        A tab delimited file with known orientations. 1st
                        column is scaffold name, 2nd column is +,-,?
```

## orient_fasta.py
```
usage: orient_fasta.py [-h] [--prefix PREFIX]
                       <scaffolds.fasta> <orientations.txt>

Orient scaffolds fasta file according to HiCOrient output.

positional arguments:
  <scaffolds.fasta>   Fasta file containing sequences to be oriented.
  <orientations.txt>  HiCOrient results tsv file.

optional arguments:
  -h, --help          show this help message and exit
  --prefix PREFIX     Prefix to use for output files.
```

# Elaboration

