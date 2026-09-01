# Chapter 7: Third-Party Packages and Pip

# --- Pip and PyPI ---
# Theory: PyPI (Python Package Index) is the public repository where
# third-party Python packages are published. pip is the command-line tool
# that downloads and installs those packages from PyPI onto your machine.
# Example: install the popular "requests" package
# $ pip install requests

# --- Virtual Environments ---
# Theory: a virtual environment is an isolated Python setup for a single
# project. It keeps that project's installed packages separate from other
# projects and from your system-wide Python, avoiding version conflicts.
# Example: create a virtual environment named "venv"
# $ python -m venv venv
#
# Example: activate it
# macOS/Linux: $ source venv/bin/activate
# Windows:     > venv\Scripts\activate
#
# Example: deactivate it when done
# $ deactivate

# --- Installing Packages in a Virtual Environment ---
# Theory: once a virtual environment is activated, any "pip install"
# command installs packages into that environment only, not system-wide.
# Example: with venv activated, install a package
# $ pip install requests
#
# Example: install a specific version
# $ pip install requests==2.31.0
#
# Example: uninstall a package
# $ pip uninstall requests

# --- Pip Freeze and requirements.txt ---
# Theory: "pip freeze" lists all installed packages and their exact
# versions. Saving that output to requirements.txt lets anyone recreate
# the same environment with "pip install -r requirements.txt" — useful for
# sharing projects or deploying them.
# Example: generate the requirements file
# $ pip freeze > requirements.txt
#
# Example: install everything listed in it
# $ pip install -r requirements.txt
