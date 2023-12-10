# Instapy package

Instapy is a package that can be used to filter a given image 
with either a gray - or sepia filter. When applying the filters 
you can choose between three different implementations that
provide different runtimes for the code. The implementations 
are written with the use of pure python, numpy or numba. After
applying a filter one can choose to have the filtered image 
either displayed or saved to a specific filename. 


## Installation

To install the package you need to git clone the repository at: 

https://github.com/saabsingh1/IN3110.git

When this is done and you have the repository at your disposal,
navigate to the assignment3 folder. When you are in this 
directory you may install it using a package installer such as pip. 

Example:

```pip install instapy```

After this installment you should be ready to filter your images!
    
## Usage

Now that you have installed the package you are probably wondering
how you may use it!

To run the code you can either run it with:

``` python3 -m instapy <arguments> ``` 

or directly:

``` instapy <arguments> ```

When running the commands, you have to apply at least one argument, 
and that is the filename of whichever image you wish to filter. 
If you choose to just give this one argument, your image will by
defualt be filtered with the gray filter with the pure python 
implementation and scaled true to given size. The default will 
also only display the image. 

If you wish to alter the defualt filtration, please give additional
arguments. For information regarding the optional arguments please
type ``` instapy -h ``` when running the code. 

Valid arguments: 

``` -h, --help ```
Shows the help board with the different arguments.

``` -o OUT, --out OUT ``` 
Arguments must be given along with a filename for the saved 
filtered image.

``` -g, --gray ```
The arguments selects the gray filter for the image.

``` -se, --sepia ```
The argument selects the sepia filter for the image. 

``` -sc SCALE, --scale SCALE ```
The arguments scales the filtered image with a given scale factor.

```-i {python,numba,numpy,cython}, --implementation {python,numba,numpy,cython} ``` 
The arguments must be given with an implementation from the list.

```-r, --runtime ```
Select the argument to show the average runtime over 3 runs. 



## Running tests

The package has been tested using the pytest framework. If you
wish to test the code, you can use the following command in the
```assigment3/test``` directory:

To test all the implementations: 

````pytest````

For testing a specific implementation:  
``` pytest test_implementation.py ```





## Other

When testing or applying filters to images, one may run into trouble if 
using a filename without the whole path of the file. 
If this occurs, please apply the full source path of the file name or image. 
 
For this task, the cython implementation has not been done. 
This was only mandatory for those doing the course IN4110.
Neither is it possible to tune the amount of sepia filtering. 
