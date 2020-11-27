# flake8: noqa
# type: ignore

# Configuration file for ipython.

## Whether to display a banner upon starting IPython.
#  Default: True
c.TerminalIPythonApp.display_banner = False

## Autoformatter to reformat Terminal code. Can be `'black'` or `None`
#  Default: None
c.TerminalInteractiveShell.autoformatter = "black"

## Set to confirm when you try to exit IPython with an EOF (Control-D in Unix,
#  Control-Z/Enter in Windows). By typing 'exit' or 'quit', you can force a
#  direct exit without any confirmation.
#  Default: True
c.TerminalInteractiveShell.confirm_exit = False

## If True, any %store-d variables will be automatically restored when IPython
#  starts.
#  Default: False
c.StoreMagics.autorestore = True
