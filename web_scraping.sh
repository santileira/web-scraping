#!/bin/bash
# set -eo pipefail
# IFS=$'\n\t'

webscraping () {

  install () {
    pip3 install virtualenv
    if [ ! -d "./web_scraping_env" ]
    then
      virtualenv web_scraping_env
    fi
    # activate environment
    source ./web_scraping_env/bin/activate
    python setup.py install
    echo "Succesfuly instaled web-scraping in virtual env web_scraping_env. Run source ./web_scraping_env/bin/activate to switch web_scraping_env."

  }


  help_message () {
    cat <<-EOF
adsystem commands:
  install            -> install web-scraping in a new python environment "web_scraping_env"
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

