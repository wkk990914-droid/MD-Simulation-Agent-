#!/bin/bash


## Create conda enviroment and activate it
#conda create --prefix /groups/ycolon/group-envs/agentic-tutorials python=3.10.13
conda activate /groups/ycolon/group-envs/agentic-tutorials

## install dependencies from requirements.txt
pip install -r requirements.txt

## Install conda packages 
conda install mbuild==0.17.0 openMM==8.2.0
conda install -c conda-forge gmso

### Download and isntall Ollama (no-root). Skip this tep if ollama is installed
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
# Substitute any place you have write access for ~/.local
mkdir -p ~/.local
tar -C ~/.local -xzf ollama-linux-amd64.tgz
# Place this in your ~/.bashrc to persist
export PATH=$HOME/.local/bin:$PATH
export LD_LIBRARY_PATH=$HOME/.local/lib/ollama:$LD_LIBRARY_PATH
### Change the path here to store the models in a large disk
export OLLAMA_MODELS=/scratch365/$USER/Ollama_models

## remove downloaded file
rm ollama-linux-amd64.tgz

