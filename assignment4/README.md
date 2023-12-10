# Assigment 4

In this assigment i have worked with data mining, web scraping and used regex to filter trough HTML data. 
The tools i have used for solving the various tasks have been ```Python```, ```RegEx```, ```beautifulsoup``` and ```pandas```. 
A large part of the assigment involves retrieving HTML code from urls, parse trough it for relevant information and 
displaying the results. 

## Getting started

First off, you need to git clone the repository at: 

https://github.com/saabsingh1/IN3110.git

When this is done and you have the repository at your disposal,
navigate to the assignment4 folder. 

## Requiered dependencies and packages

Below are the dependencies and packages that i have used along with the versions:

```requests           2.28.1```
```matplotlib         3.6.1```
```beautifulsoup4     4.11.1```

Ran on the following operating system:

```macOS Big Sur      11.6```

Dependencies and packages can be installed with a packager installer such as pip:

```pip install requests```
```pip install matplotlib```
```pip install beautifulsoup4```

    
## Usage

Now that you have installed the requirments you are probably wondering
how you may use the programs!

None of the programs take any optional arguments. If one may want to change the test links and inputs, this can be done manually 
in the code. One can also save the outputs of the programs by manually entering a desired file or folder in the functions of the programs that have this optiion. 

To run the different programs: 
```python program_name.py"```

## Running tests

The package has been tested using the pytest framework. If you
wish to test the code, you can use the following command in the
```assigment4/test``` directory:

To test all the implementations: 

````pytest````

For testing a specific program:  
``` pytest test_program.py ```

## Other
  
For this assigment, i have done all the mandatory tasks for the course IN3110 and the optional bonus task 4 "Regular Expressions for finding Dates". I have not the optional bonus challenge "Wiki Race with URLs".