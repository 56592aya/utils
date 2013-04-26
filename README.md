Generic
=======
Contains code for generic repos.  

To use
------
You must add the directory above `utils` to your PYTHONPATH

Directories
-----------

### data

* Don't version data.
* To avoid excess sharing of processed data (which changes often), it is preferable to share raw data and the scripts and notebooks that transform *raw* into *processed*.  
* Contents of any *raw* folder should never be modified or deleted.  This way, your script will create the same output as everyone else's script.
* Shell scripts and notebooks will assume the existence of the **local** folders `data/raw` and `data/processed`.  They already exist in the repo.

### Notebooks
For ipython notebooks.  Put your name in the notebook name to avoid redundancy.

### src
Source code.

### schema
Schema for the data sets

### tests
Unit and integration tests.

### scripts
Shell scripts.
