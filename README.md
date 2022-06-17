CS1999: Buggy Race Editor
=========================

> This is the "buggy editor" component of the Foundation Year Computer Science
> project at RHUL.


## Installation & set up

Getting the editor running on your own machine differs depending on which
operating system you're using. The principles are the same, but the way to
execute them is slightly different.

Start by logging into the [race server](http://rhul.buggyrace.net) — if you
follow the instructions there, it will automatically _fork_ the repo into your
own GitHub account for you. Then clone that fork from your GitHub account onto
your own machine.

> If you don't have access to your own machine, it's possible to use
> [repli.it](https://replit.com) instead.


### Prerequisites

You must have Python3 installed:

* [Python 3](https://www.python.org) for programming

It's best if you have Git installed too:

* [Git](https://git-scm.com) for version control

> If you don't/can't install git, you _can_ download the source code manually
> but we recommend you don't do it that way.

If Python or git are not already installed on your machine, see the
downloads/installation instructions on their respective websites.


### Get the source code onto your own machine

This is the recommended way of doing it:

1. _Fork_ [our repo](https://github.com/RHUL-CS-Projects/CS1999-buggy-race-editor)
   into your own GitHub account. If you log into the
   [race server](http://rhul.buggyrace.net) we will do this automatically
   for you.

2. Next, _clone_ the forked repo from your GitHub account onto your own machine.


### Installation

Before you can run the buggy editor webserver you need to install some
Python modules.

Use the `cd` command to change to the directory that you got from either
cloning or unzipping the source code.

Use pip — which should have been installed as a side-effect of installing
Python — to load the required modules (including Flask, the webserver framework).
The file `requirements.txt` tells pip what modules are needed.

    pip install -r requirements.txt

Finally, set up the database:

    python3 init_db.py

This creates an SQLite database in a file called `database.db`.

There's no configuration file to edit (yet). You're ready to go!

> If `pip` or `python3` don't work for you: ask for help! The details differ
> depending on what operating system you're using and how you installed
> Python.


## Running the server

Once the source code is on your machine, the dependencies are installed, and
the database initialised, you can run the Buggy Editor.

If you're not already in the project's directory, `cd` into it.

> If you're using a virtual environment, remember to activate it now.

Run the application with:

    python3 app.py

The webserver is running on port 5000 (that's the default for Flask apps). If
you make a request for a web page, it will reply with one!

Go to [http://localhost:5000](http://localhost:5000) in your web browser.
You haven't specified which file you want, so you'll get the `/` route, which
(you can see this by looking in `app.py`) invokes the `index.html` template.

You can see the webserver's activity in the terminal, and the result of its
action in the browser.

You're done!

---