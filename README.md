
## Set up test environment

### Installation

The test framework is running against Python 3, please make sure you have Python 3.7(or above) and Pip3 installed on your computer. Once you create a local copy from this repo, you can go into it and install dependent python libraries by shooting below command:

> pip3 install -r packages.txt

The command will install all required libraries like Pytest, PyHamcrest and Allure etc. to your computer. 

You need to use allure command-line to resolve allure results and present test report in browsers, you can install it with Homebrew

> brew install allure

To develope your test cases, you may choose Visual Studio Code(Recommended!) or PyCharm as your IDE

## Run test cases

Our test framework is built on Pytest which supports several ways to run and select tests from the command-line. (We put all our test code in the **tests** foler)

### Run tests in a module

Run all test classes and test methods in the module **test_ss_get_users.py**

>py.test tests/jaeger/v5/ads/ad_markup/test_ad_markup.py

### Run tests in a directory

Run all test cases in the auth component of Mission ctrl

>py.test tests/jaeger/v5

### Run a specific test within a module and a class

>py.test tests/jaeger/v5/ads/ad_markup/test_ad_markup.py::TestAdMarkup::test_ad_markup_expiry

### Run tests by keyword expression

This will run tests which contain names that match the given string expression, which can include Python operators that use filenames, class names and function names as variables

>py.test -k "test_ad_markup_expiry"

## Generate allure report

By default, Pytest will ouput test results to the terminal console directly, to generate descriptive allure report, firstly, you need to set Pytest to generate allure results while executing the tests

> py.test --alluredir=%allure_result_folder%

Then you can run allure command-line to review the test results in your local browser:

> allure serve %allure_result_folder%