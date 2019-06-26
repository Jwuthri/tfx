#!/usr/bin/env bash

if [[ ! -f venv/bin/activate ]]; then
    pip install virtualenv --user
    virtualenv venv --no-site-packages --python=python3
    source venv/bin/activate

    pip install -r requirements.txt
    pip install -r dev-requirements.txt
    pip install  https://github.com/tensorflow/tfx/archive/5373235fb5fcbeb8ff419b49293a7251ac967ce6.zip #fixme better handling of the tfx deps
fi
