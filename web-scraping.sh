#!/bin/bash
# set -eo pipefail
# IFS=$'\n\t'

webscraping () {

  install () {
    pip3 install virtualenv
    if [ ! -d "./web-scraping-env" ]
    then
      virtualenv web-scraping-env
    fi
    # activate environment
    source ./web-scraping-env/bin/activate
    python setup.py install
    echo "Succesfuly instaled web-scraping in virtual env web-scraping-env. Run source ./web-scraping-env/bin/activate to switch web-scraping-env."

  }


  help_message () {
    cat <<-EOF
adsystem commands:
  install            -> install web-scraping in a new python environment "web-scraping-env"
EOF
  }


  case $1 in
    install)
      install $@
      ;;
    help)
      help_message $@
      ;;
  esac
}

webscraping $@

