
# Quick start

# Navigating GitHub

Click the copy button like this

![Image](https://cdn.discordapp.com/attachments/799265265820237834/863153436487843911/rVZsBs7xsU.gif)

If the command line says that you don't have permission, set your credentials

Get your no reply email here https://github.com/settings/emails

![image](https://cdn.discordapp.com/attachments/799265265820237834/863183120738811934/unknown.png)

```
git config --global user.name "fname lname"
git config --global user.email "no reply email here"
git config --global user.password "secret"
```

> Note: this is not a good method of setting credentials. But if you are just learning git, it doesn't matter that much

> Another note: If that doesn't work, clone using the command line and select `Web Browser` for authentication

Now go to your project folder

# Cloning

Type `cmd` in the file explorer address bar of our project (create empty file before doing this)

do `git clone <rightclick - this pastes the url> .`

It will generate the repo in our current repository

# Quick start this project

`python -m venv .venv`

# Activate virtual environment

if you are windows

run `".venv/bin/activate.bat"` in `cmd.exe`

After that, you should see `(.venv)` in front like this

```
C:\public\pydis-cj8>".venv/scripts/activate.bat"

(.venv) C:\public\pydis-cj8>
```

> EVERYTHING YOU WOULD RUN AS `python` and `pip` SHOULD BE RUN ONLY WHEN `(.venv)` IS THERE (when in doubt, just run on both)

# Installing dependencies

`(.venv) C:\public\pydis-cj8>pip install -r dev-requirements.txt`

to exit, just run `deactivate` like `(.venv) >deactivate` and it will exit

# Installing pre-commit

> If you are new to git, please skip this step. It's more of a waste of time than a precaution when you are new to git. It's ok to do this step a few days later when you are familiar with everything

```
(.venv) >pip install pre-commit
...some logs here, wait patiently
(.venv) >pre-commit install
(just in case it's not installed)
```

What this does is essentially runs a "prehook" when you run `git commit`. These are various checks before a developer actually commits something to a git repository.

# Installing Windows Terminal

Search for Microsoft Store in your taskbar

Launch it and install `Windows Terminal`

You can go to your project directory like this

![image](https://cdn.discordapp.com/attachments/799265265820237834/863181507392438272/unknown.png)

# Few notes

You have push access. Go ham with the code

Here are my vscode settings. If you use vsc, make a `.vscode/settings.json` file and paste this in
```json
{
	"python.linting.flake8Enabled": true,
	"python.linting.enabled": true,
	"editor.tabSize": 4,
	"editor.detectIndentation": false,
	"editor.insertSpaces": true
}
```

# Ask questions on Discord

You are most probably not alone! Asking is faster than googling
