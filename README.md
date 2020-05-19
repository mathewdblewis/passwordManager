CLI Password Manager
====================

Here is a password manager CLI written in python3 for mac and linux.
This command line tool offers a light weight, minimalistic
and easy to use interface for password management.
All data is encrypted using the library cryptograph.fernet and is stored
in the users home directory in the hidden file `.passwordmanager.enc`.


Installation
--------------------
To install passwords, paste the following in your console:

    curl -s https://raw.githubusercontent.com/mathewdblewis/passwordManager/master/install.py > install.py
    python3 install.py
    rm install.py
    
This installation script will prompt you for a location in your path to store
the passwords program. 

