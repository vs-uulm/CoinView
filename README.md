# CoinView Code and Evaluation Tools

Quite a few things only work on unix like system.

## Overview

This repository consists of the tools and code used to collect timestamp data of transactions in the bitcoin network and prepare the data for visual consumtion and use in papers.

See also: https://github.com/vs-uulm/btcmon

### Technologies used:

 * a slightly modified version of bitcoinj 0.14.7
 * Python3 with matplotlib and pyplot
 * gnuplot
 * Java-11

The modifications of bitcoinj 0.14.7 are:

 * Creation of a logging file and a  message digest
 * Generation of a runtime key as hash of a random number.
 * For inv message of transactions, the following information is logged as a single csv line (in order)
    * Current timestamp in milliseconds
    * sha256 hash of: client IP+Port concatenated with runtime key (this allows tracking of transactions for clients, but hides the identity and makes data publishable)
    * hash of the transaction

### The directories are named after the steps supported:

 * collection: bitcoinj patch and application code
 * modeling: python scripts used for the initial modeling of the data and analysis for different kinds of distributions
 * evaluation: python scripts and gnuplot scripts used to create evaluations and respective plots used in the paper
 * datasets: some of the smaller result datasets to create images
 * gnuplot: gnuplot scripts to visualise some results

## Usage

### Data Collection

The data collection is based on the [bitcoinj](https://github.com/bitcoinj/bitcoinj/tree/b131cc77384ed398b205d3e2e932d1d8228c4edb) library in version 0.14.7.

Apply the patch to bitcoinj:

```
git clone https://github.com/bitcoinj/bitcoinj.git
git fetch --all --tags
git checkout tags/v0.14.7
git apply bitcoinj_0.14.7.patch
mvn clean package

# to make sure all works, you may also use docker with (windows powershell: ${PWD} linux: $(pwd))
# docker run -it --rm -v ${PWD}:/usr/src/btcj -w /usr/src/btcj maven:3-openjdk-8 mvn clean package
```

The resulting bitcoinj-core-0.14.7-bundled.jar in core/target will be built with our data collection application.

```
cd collection/application
# compile
javac -cp ./bitcoinj-core-0.14.7-bundled.jar .\research\*.java
```

To run the example code to collect data:

```
# linux:
java -cp ".:./bitcoinj-core-0.14.7-bundled.jar" research/Main

# windows:
java -cp ".;./bitcoinj-core-0.14.7-bundled.jar" research/Main
```

Data will be writte to a file of the form: "crawler-dd.mm.yyyy hh.mm.ss.csv" where date and time shortages are replaced by the current date and time.

If trouble occurs, these commands can also be run from within a docker container:

```
docker run -it --rm -v ${PWD}:/usr/src/btccol -w /usr/src/btccol --rm openjdk:8 /bin/bash
```

### Gnuplot:

 * Heatmap: `gnuplot error_heatmap.gp`
 * Error Curve: `gnuplot error_fitting_curve.gp`
 * tracking mu plot for example dataset: `gnuplot eval_mu_1m_ulm.gp`
 * tracking si plot for example dataset: `gnuplot eval_si_1m_ulm.gp`

### Modelling:

The main modeling script is `run.py` and consists of 4 stages:

 1. Run split.py splits up the dataset by transaction 
 2. Run stat.py aggregates descriptive statistics of generated datasets.
 3. Run data.py and combine.sh, computes histograms of transactions and probability density function parameters.
 4. Run pdf_printer.py, creates graphs of the computed pdf parameters

Stages will try to delete their result files before running.

The script takes mandatory paramters:

 * stages to apply: 1, 2, 3, 4 or all
 * input file: a csv file of the required structure to analyse (This is required even if the file is not used)
 * postfix: the first string not viable for any other parameter is used as a postfix for folders

An example call might be `python3 run.py 1 2 xyz.csv XY` and will append XY to all folders it creates, and run stages 1 and 2 using the file xyz.csv

### Evaluation:

 * split to split a log by transaction
 * randommerge to merge a given amount of connections (e.g. 8) to a virtual log as if connected to those 8 based on the split transactions, e.g., `./randommerge.sh 1000 8 split-1m-GBS`
 * apply to apply btcmon to the given datasets, generate and parse results
 * txapply to apply parameter estimation to gain a ground truth

Example workflow to create the ground truth dataset for the last 1 mio seen transactions:

```
tail -n 1000000 crawler-06-02-2019-03-13-04-GBS-SIMUL.csv > 1m-GBS.csv
python3 txsplit.py 1m-GBS.csv
./txapply.sh txsplit-1m-GBS/
sort --field-separator=',' --key=1 truth.csv > txsplit-1m-GBS.truth.sort.csv
```