"""
"""
from random import choice
import numpy as np
import sys
import csv
import json


def lazyprop(fn):
    """
    Use as a decorator to get lazily evaluated properties.
    """
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


def get_infile(infilename, inmode='rb'):
    """
    Gets infile, which is an opened version of infilename.

    Parameters
    ----------
    infilename : String
        Name of file to read.  If None, we will read from stdin

    Returns
    -------
    infile
    """
    if infilename:
        infile = open(infilename, inmode)
    else:
        infile = sys.stdin

    return infile


def get_outfile(outfilename, outmode='wb'):
    """
    Gets outfile, which is an opened version of outfilename.

    Parameters
    ----------
    outfilename : String
        Name of file to write.  If None, we will write to stdout
    outmode : String
        Mode to open file in

    Returns
    -------
    outfile
    """
    if outfilename:
        outfile = open(outfilename, outmode)
    else:
        outfile = sys.stdout

    return outfile


def get_inout_files(infilename, outfilename, inmode='rb', outmode='wb'):
    """
    Gets infile, and outfile, which are opened versions of infilename,
    outfilename.

    Parameters
    ----------
    infilename : String
        Name of file to read.  If None, we will read from stdin
    outfilename : String
        Name of file to write.  If None, we will write to stdout
    outmode : String
        Mode to open file in

    Returns
    -------
    The tuple (infile, outfile)
    """
    infile = get_infile(infilename, inmode=inmode)
    outfile = get_outfile(outfilename, outmode=outmode)

    return infile, outfile


def close_files(infile, outfile):
    """
    Closes the files if and only if they are not equal to sys.stdin, sys.stdout
    """
    if infile != sys.stdin:
        infile.close()
    if outfile != sys.stdout:
        outfile.close()


def get_list_from_filerows(infile):
    """
    Returns a list generated from rows of a file.
    
    Parameters
    ----------
    infile : File object
        Lines starting with # are comments
        Blank lines and leading/trailing whitespace are ignored
        Other lines will be converted to a string and appended to a
        list.
    """
    kpv_list = []
    for line in infile:
        # Strip whitespace
        line = line.strip()
        # Skip empty lines
        if len(line) > 0:
            # If the line isn't a comment
            # Append the content to the list
            if line[0] != '#':
                kpv_list.append(line.rstrip('\n'))

    return kpv_list


class BadDataError(Exception):
    """
    Dummpy class that is exactly like the Exception class.  Used to make sure
    people are raising the intended exception, rather than some other wierd
    one.
    """
    pass


def pickleme(obj, filename, protocol=2):
    """
    Save obj to disk using cPickle.

    Parameters
    ----------
    obj : Serializable Python object
    filename : String
        Name of file to store obj to
    protocol : 0, 1, or 2
        2 is fastest
    """
    with open(filename, 'w') as f:
        cPickle.dump(obj, f, protocol=protocol)


def unpickleme(filename):
    """
    Returns unpickled version of object.

    Parameters
    ----------
    filename : String
        We will attempt to unpickle this file.
    """
    with open(filename, 'r') as f:
        return cPickle.load(f)


def printdict(d):
    for key, value in d.iteritems():
        print "%s: %s" % (key, value)


def print_dicts(dicts, prepend_str=''):
    for key, value in dicts.iteritems():
        if isinstance(value, dict):
            print prepend_str + key
            next_prepend_str = prepend_str + '  '
            print_dicts(value, next_prepend_str)
        else:
            print "%s%s = %.5f"%(prepend_str, key, value)


def get_structured_array(listoflists, schema, dropmissing=False):
    """ 
    Uses schema to convert listoflists to a structured array.

    Parameters
    ----------
    listoflists : List of lists
    schema : List of tuples
        E.g. [(var1, type1),...,(varK, typeK)]
    dropmissing : Boolean
        If True, drop rows that contain missing values
    """
    ## First convert listoflists to a list of tuples...
    # TODO : This CAN'T actually be necessary..find another way
    if dropmissing:
        tuple_list = [tuple(row) for row in loan_list if '' not in row]
    else:
        tuple_list = [tuple(row) for row in loan_list]

    return np.array(tuple_list, schema)
