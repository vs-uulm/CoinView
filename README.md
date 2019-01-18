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

### Gnuplot:

 * Heatmap: `gnuplot error_heatmap.gp`
 * Error Curve: `gnuplot error_fitting_curve.gp`
 * 

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

