# How to contribute to the Knowledge Graph Toolkit

Third-party contributions are welcome to keep improving KGTK and support 
additional features. In order to include new contributions, please follow 
the guidelines below.

## Before you start
Please check the open issues related to your contribution, as your contribution
may be under discussion.

## Making changes

* Create a new branch with the new feature or bug you are addressing. Please try 
to keep features modular.
  * Clone the `dev` branch, as it is the most updated one in the repository.
* Make commits of logical and atomic units.
* Do pull requests **only** against the `dev` branch. Please avoid working directly
on the `main` branch.
  * Specify which issues does your pull request address. 
* Add/Update unit tests for the new changes.
* Update the documentation, if there are such changes, in the consequent file under the `docs` folder.
* Add a link to a new documentation file in the `mkdocs.yml` file, otherwise it will not show up in https://kgtk.readthedocs.io/en/latest/
* Please use the [KGTKReader](https://github.com/usc-isi-i2/kgtk/blob/master/kgtk/io/kgtkreader.py) class to read in a KGTK file.
* Please use the [KGTKWriter](https://github.com/usc-isi-i2/kgtk/blob/master/kgtk/io/kgtkwriter.py) class to write to a KGTK file.
