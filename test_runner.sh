#!/bin/bash
# To run all python tests
if [ "$1" == "-h" ]; then
  echo ""
  echo "Script to run tests from shell."
  echo ""
  echo "Options:"
  echo "    -h                                       show this help"
  echo "    -test                                    run only test_connection.py"
  echo "    -all                                     run every test"
  echo "    -project_name                            run tests in given project folder"
  echo "    <test_file_name>.py                      to run all tests from given file (optional)"
  echo "    <test_file_name>.py <test_case_name>     to run single test from given file (optional)"
  echo ""
  exit 0
fi


if [ "$#" -ne 4 ]; then
  if [[ $1 == "-test" ]]; then
    if [ "$#" -eq 1 ]; then
          venv/bin/python -m pytest Tests/test_projects_connections.py
    else
      echo "Illegal number of parameters (use -h for help)"
      exit 0
    fi
  fi

  if [[ $1 == "-all" ]]; then
    project=""
   elif [[ $1 == "-Webshop" ]]; then
      project="Webshop/"
   elif [[ $1 == "-Seraph" ]]; then
      project="Seraph/"
  else
    echo "No such parameter use: (all, Webshop, Seraph or use -h for help)"
    exit 0
  fi
  FOLDER_NAME=$(date '+%Y_%m_%d_(%H_%M)')
  mkdir -p Results
  find "./Tests/$project" -name "test_*.py" | while read file; do
    file_name=test_$(echo $file | sed 's/.*test_/''/g')
    project_name=$(echo $file | sed 's/.*Tests\//''/g' | sed 's/\/.*/''/g' | sed 's/.py/''/g')
    result_file="$FOLDER_NAME/$project_name"$(echo $file_name | sed 's/.py/.xml/g')

    if [ "$#" -eq 2 ]; then
      if [[ $file == *"$2"* ]]; then
        venv/bin/python -m pytest --reruns 1 --junitxml=Results/$result_file $file
      fi
    elif [ "$#" -eq 3 ]; then
      if [[ $file == *"$2"* ]]; then
        venv/bin/python -m pytest --reruns 1 --junitxml=Results/$result_file $file -k $2
      fi
    else
      venv/bin/python -m pytest --reruns 1 --junitxml=Results/$result_file $file
    fi
  done
else
  echo "Illegal number of parameters!!! (use -h for help)"
  exit 0
fi