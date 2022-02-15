# package_install
Package Installation and System Dependencies


##### How to run locally
- Extract the `.tar` archive to the desired folder on your computer

- Open the project's root folder in your terminal

- Create a virtual environment using the following command `python3 -m venv env` . (If you have not yet installed Python, please see instructions [here](https://www.python.org/downloads/))

- Activate the environment using the following command if on MacOS or Linux `source env/bin/activate`. If on any other platform, please check activation instructions [here](https://www.python.org/downloads/)

- Install the required packages by running the following command `pip install -r requirements.txt`


##### Running Tests
The application includes unit and integration tests. To run them please open the project's root folder in your terminal and then run:
```
coverage run -m unittest discover
```

To check for code coverage, run the following command after the one above:
```
coverage report -m