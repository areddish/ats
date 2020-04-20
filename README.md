# Automatic Trading system

## Required Software

[Python 3.6.3+](https://www.python.org/downloads/) *Currently testing with 3.6.3*

[*LATEST* TWS API for python](http://interactivebrokers.github.io/downloads/TWS%20API%20Install%20973.06.msi)

## Installation

To install the ats package for development, from the root of the git repo run this command:

```
pip install -e .
```

To install the ibapi, change to the <tws install location>\source\pythonclient and run the same command
i.e. on windows
```
cd "\tws api-latest\source\pythonclient"
pip install -e .
```



# Install TWS API package

git clone https://github.com/InteractiveBrokers/tws-api
cd source\pythonclient
pip install wheel
python setup.py bdist_wheel
python -m pip install --user --upgrade dist\ibapi-9.76.1-py3-none-any.whl

# Install ATS

cd ats
pip install -e
