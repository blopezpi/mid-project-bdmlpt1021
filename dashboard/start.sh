#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[server]
headless = true
enableCORS=false
port = $PORT

[theme]
base=\"dark\"
" > ~/.streamlit/config.toml

streamlit run main.py
