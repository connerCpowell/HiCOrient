# HiCOrient

<b>HiCOrient</b> is a tool that uses HiC chromatin interaction data to orient a collection of ordered scaffolds. The process of achieving a 
chromosome scale assembly from a draft assembly often involves 3 steps:

1. Clustering of scaffolds into pseudo molecules/chromosomes
2. Ordering the scaffolds within each chromosome
3. Orienting the clustered and ordered scaffolds.

HiCOrient can be used when a genetic map was able to cluster and order most scaffolds, but not able to orient most scaffolds.

# Installing HiCOrient
## Platforms
<ul>
  <li>Linux</li>
  <li>Mac OSX</li>
</ul>
## Dependencies
python2.7
scipy (see specific branch in requirements.txt)
numpy

## Installing From Source
The only way to install HiCOrient is from source. To install, execute the following commands:

```
$git clone https://github.com/malonge/HiCOrient
$cd HiCOrient
$pip install -r requirements.txt
$python setup.py install
```

# Command Line Usage
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
