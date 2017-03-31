# Calculations

--------------------------------------------------------------------------------

**Lucas M. Hale**, 
[lucas.hale@nist.gov](mailto:lucas.hale@nist.gov?Subject=ipr-demo), 
*Materials Science and Engineering Division, NIST*.

**Chandler A. Becker**, 
[chandler.becker@nist.gov](mailto:chandler.becker@nist.gov?Subject=ipr-demo), 
*Office of Data and Informatics, NIST*.

**Zachary T. Trautt**, 
[zachary.trautt@nist.gov](mailto:zachary.trautt@nist.gov?Subject=ipr-demo), 
*Materials Measurement Science Division, NIST*.

Version: 2017-03-23

[Disclaimers](http://www.nist.gov/public_affairs/disclaimer.cfm) 
 
--------------------------------------------------------------------------------

## Contents

- [Introduction](#introduction)

- [Calculation folders](#folders)

    - [Location](#location)
  
    - [Contents](#contents)

- [How to run](#run)

    - [Single calculation](#single)
    
    - [High-throughput prepare](#high-throughput)

- [Input parameter files](#input)

    - [Formatting rules](#input-rules)
    
    - [Formatting example](#input-example)
    
    - [Easy creation](#input-easy)

--------------------------------------------------------------------------------

## <a name="introduction"></a>Introduction

The iprPy framework was designed with the intent of allowing for easy 
implementation of a wide variety of calculations. The structure and format of 
the calculations allows for the following features:

- The calculation constitutes a unit of work independent from all other 
  calculations.

- The calculation exists as a Python script that can executed outside the iprPy 
  framework.

- The calculation script reads in parameters from a simple input parameter file, 
  and produces a structured results record.

- The calculation's methodology is documented using a demonstration Jupyter 
  Notebook containing the same functions as the calculation script.

- Components of the calculation can be accessed from Python through the 
  iprPy.Calculation class. 

- Calculations are modular: new calculations are automatically recognized by 
  iprPy if they are placed in the appropriate directory.

- The calculations can be prepared for high-throughput runs using parameter 
  combinations unique to each calculation.

- Preparing high-throughput runs can be done either using the iprPy.Calculation 
  class, a stand-alone Python script, or from the command line.

--------------------------------------------------------------------------------

## <a name="folders"></a>Calculation folders

Each calculation exists as a folder containing all of the relevant files. In 
this way, the treatment of the calculations is modular allowing for the easy 
addition, removal and modification of one or more without affecting the others.

The name of the folder is the calculation's name, calcname, which is how it is 
referred to when loaded by the iprPy Python package.


### <a name="location"></a>Location

The calculation folders can be found in the iprPy/calculations directory. 

The demonstration Notebook versions of the calculations can be found in the 
docs/calculation-demonstration directory.


### <a name="location"></a>Contents

The contents of each calculation folder are similar:

- __README.md__: A Markdown formatted text file that describes what the 
  calculation does and outlines all of the input parameters recognized by the 
  calc\_[calcname].py and the prepare\_[calcname].py scripts.

- __calc\_[calcname].py__: The Python script for the calculation.

- __calc\_[calcname].template__: A template version of the calculation input 
  parameter file. 

- __prepare\_[calcname].py__: The Python script for high-throughput preparing 
  of the calculation.

- __\_\_init\_\_.py__: Tells the iprPy package to load the calculation folder 
  as a submodule, and defines the necessary functions for the iprPy.Calculation
  class.

- Any other files that the calculation script needs in order to run properly, 
  such as LAMMPS input script templates. 

For the calculations with corresponding demonstration notebooks, the 
docs/calculation-demonstration directory contains:
  
- __calc\_[calcname].ipynb__: The Jupyter Notebook demonstration version of the
  calculation. This is where to look if you want to understand a calculation's 
  methodology.
  
- __calc\_[calcname]__: Subdirectory for the files used or created by the 
  calculation Notebook.
--------------------------------------------------------------------------------

## <a name="run"></a>How to run

The design supports calculations being executed either individually or en mass 
for high-throughput investigations.


### <a name="single"></a>Single calculation

Running a single calculation is easy!

1. Copy the calculation folder to another location (this keeps the original 
   folder from becoming cluttered).

2. Create an [input parameter file](#input) "calc\_[calcname].in" using a text 
   editor. Save it in the copy of the calculation folder.

3. In a terminal, cd to the calculation folder you created, and enter:
        
        python calc_[calcname].py calc_[calcname].in
        
4. When the calculation finishes successfully, a "record.json" record file will 
   be created containing the processed results.


### <a name="high-throughput"></a>High-throughput prepare

The cool thing is that running multiple instances of the calculation is almost 
as easy as running a single calculation.

1. Set up a database and access parameters for loading it as an 
   [iprPy.Database]().

2. Create an [input parameter file](#input) "prepare\_[calcname].in" using a 
   text editor.

3. Place (copies of) the prepare\_[calcname].py and prepare\_[calcname].in in 
   the same directory. This can be anywhere, including the original calculation 
   folder.

4. In a terminal, cd to the directory containing the two prepare files, and 
   enter:
        
        python prepare_[calcname].py prepare_[calcname].in
        
5. When the script finishes, check that there are copies of the calculation in 
   your run_directory, and incomplete calculation records in your database.

6. Start one or more [runner]() scripts to perform the calculations.

Alternatively, calculations can be prepared either from another Python script 
using the iprPy.Calculation class, or in a slightly more streamlined manner 
using the iprPy command line options.

--------------------------------------------------------------------------------

## <a name="input"></a>Input parameter files

For both the calc_[calcname].py and prepare_[calcname].py scripts, all variable 
parameters are read in from input parameter files. These files are simple text 
files that provide values to parameter names in a simple key-value manner. Each 
script has its own set of recognized variable names, which are listed in the 
calculation folder's README.md documentation file. 

### a name="input-rules"></a>Formating rules

The input parameter files follow some very simple rules.

1. Each line is read separately, and divided into whitespace-delimited terms.

2. Blank lines are allowed.

3. Comments are allowed by starting terms with #. The # term and any subsequent 
   terms on the line are ignored. 

4. The first term in each line is a variable name.

5. All remaining (non-comment) terms are collected together as a complete value
   that is assigned to that variable name.

6. Any variable names without values are ignored.

7. For calculation input parameter files, each variable name can appear at most
   one time. This is because each variable is allowed only one value.
   
8. For prepare input parameter files, some variables are allowed to have 
   multiple values. This can be accomplished by listing a parameter name with a
   value on separate lines. Which parameters are limited to singular values and 
   which can be assigned multiple values is indicated in the calculation's 
   README.md file.

### <a name="input-example"></a>Formatting example

Script:
    
    #This is a comment and will be ignored
    
    firstvariable    singleterm
    
    secondvariable   multiple terms   using    spaces
    thirdvariable    term #with comments
    thirdvariable    again!
    
    fourthvariable
    
Gets interpreted as a Python dictionary:
    
    {'firstvariable': 'singleterm',
     'secondvariable': 'multiple terms using spaces',
     'thirdvariable': ['term', 'again!']}
     
### <a name="input-easy"></a>Easy creation

Here's a helpful tip for running single instances of a calculation. Instead of 
creating an input parameter file from scratch, copy the 
calc\_[calcname].template and then fill in values. The template files were 
designed for the prepare scripts, and list all of the parameter names recognized
by the calculation divided into meaningful categories. Each non-comment line 
looks something like

    parametername     <parametername>
    
Simply replace &lt;parametername&gt; with the value to assign parametername (or 
delete it to use the calculation's default value) for every line in the file. 