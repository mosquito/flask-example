Flask Example app
=================

## How to develop

0. Choose name for your project (e.g NEW_PROJECT_NAME)
1. Clone the repository

```shell
git clone https://github.com/mosquito/flask-example.git NEW_PROJECT_NAME
cd NEW_PROJECT_NAME
```

2. Create virtualenv

```shell
pip install virtualenv
virtualenv env -p python3.5
```

3. Rename this project
    1. Rename `flask_example` folder to NEW_PROJECT_NAME
    2. edit setup.py and fix all `# FIXME` comments
4. Install requires and main script

```shell
env/bin/pip install -e .
```

5. Run the main program.
