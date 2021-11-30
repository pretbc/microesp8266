# microesp8266
small python project to set controller


To run this project

1. Install `python3.9`
2. Clone repo -> ` git clone <repo_name>`
3. Cd to local project -> `cd <cloned_dir>`
4. Create venv -> `python3.9 -m venv <name_of_virtualenv>`
5. Enter venv -> `source <name_of_virtualenv>/bin/activate`
6. Install requirements -> `pip install -r requirements.txt`
7. Run `python -m main.py --<some_args>` -> please check main args to know more


This project works with python version >= 3.7

To check current version type:
1. `python -V` or `python3 -V`


Possible examples of run option:

1. with custom config: `python -m main.py --custom_config my_custome_name`
2. with args: `python -m main.py --boot 2 --bin 1 --size 3`
3. with default args: `python -m main.py`
