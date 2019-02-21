# Standard Python libraries
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)
import os
import shutil

# https://github.com/usnistgov/DataModelDict
from DataModelDict import DataModelDict as DM

# iprPy imports
from . import iaslist
from .. import rootdir

def save_potential_record(content, files=None, lib_directory=None,
                          record_style='potential_users_LAMMPS',
                          replace=False):
    """
    Saves a new potential_*LAMMPS record to the library directory.  The
    record's title is automatically taken as the record's id.

    Parameters
    ----------
    content : str or DataModelDict.DataModelDict
        The record content to save to the library directory.  Can be xml/json
        content, path to an xml/json file, or a DataModelDict.
    files : str or list, optional
        The directory path(s) to the parameter file(s) that the potential uses.
    lib_directory : str, optional
        The directory path for the library.  If not given, then it will use
        the iprPy/library directory.
    record_style : str, optional
        The record_style to save the record as.  Default value is
        'potential_users_LAMMPS', which should be used for user-defined
        potentials.
    replace : bool, optional
        If False (Default), will raise an error if a record with the same title
        already exists in the library.  If True, any matching records will be
        overwritten.

    Raises
    ------
    ValueError
        If replace=False and a record with the same title (i.e. id) already
        exists in the library.
    """
    # Load as DataModelDict and extract id as title
    content = DM(content)
    title = content['potential-LAMMPS']['id']

    # Set default lib_directory
    if lib_directory is None:
        lib_directory = os.path.join(os.path.dirname(rootdir), 'library')
    lib_directory = os.path.abspath(lib_directory)

    # Define record paths
    stylepath = os.path.join(lib_directory, record_style)
    if not os.path.isdir(stylepath):
        os.mkdir(stylepath)
    fname = os.path.join(stylepath, title + '.json')
    potdir = os.path.join(stylepath, title)
    
    # Save record
    if replace is False and os.path.isfile(fname):
        raise ValueError('Record ' + title + ' already exists')
    with open(fname, 'w') as recordfile:
        content.json(fp=recordfile, indent=4)

    # Copy parameter files
    if files is not None:
        if not os.path.isdir(potdir):
            os.mkdir(potdir)
        for fname in iaslist(files):
            shutil.copy(fname, potdir)