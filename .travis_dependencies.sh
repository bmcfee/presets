#!/bin/sh

ENV_NAME="test-environment"
set -e

conda_create ()
{

    hash -r
    conda config --set always_yes yes --set changeps1 no
    conda update -q conda
    conda config --add channels pypi
    conda info -a
    deps='six nose coverage'

    conda create -q -n $ENV_NAME "python=$1" $deps
}

if [ ! -f "$HOME/env/miniconda2.sh" ]; then
    mkdir -p $HOME/env
    pushd $HOME/env
    
        # Download miniconda packages
        wget http://repo.continuum.io/miniconda/Miniconda-3.8.3-Linux-x86_64.sh -O miniconda2.sh;
        wget http://repo.continuum.io/miniconda/Miniconda3-3.8.3-Linux-x86_64.sh -O miniconda3.sh;

        # Install both environments
        bash miniconda2.sh -b -p $HOME/env/miniconda2
        bash miniconda3.sh -b -p $HOME/env/miniconda3

        for version in 2.7 3.4 ; do
            if [[ "$version" == "2.7" ]]; then
                src="$HOME/env/miniconda2"
            else
                src="$HOME/env/miniconda3"
            fi
            OLDPATH=$PATH
            export PATH="$src/bin:$PATH"
            conda_create $version

            source activate $ENV_NAME

            pip install python-coveralls
            
            source deactivate

            export PATH=$OLDPATH
        done
    popd
else
    echo "Using cached dependencies"
fi
