

# Ruby Script - Setup

* Copy `config.json.template` to `config.json`
* Modify `config.json` prefix to unique 3 character string.

# Ruby Script - Adding a note

* Copy `note_template.json` to a new file.
* Modify the contents to the question
* Run `ruby add_note.rb -f <DECK_JSON_FILE> -n <NOTE_JSON_FILE>`

--

# Python Script - Setup
* Copy the `yycnl-ankiaddcards-default.py` file and rename it `yycnl-ankiaddcards.py`. On Linux, you can do this via the command `cp yycnl-ankiaddcards-default.py yycnl-ankiaddcards.py`.
* This new file should be untracked by virtue of its inclusion in .gitignore.
* Open the file, scroll all the way down to the main() function, and modify the prefix and deckJSON variables (at minimum).
* OPTIONAL: Go back up to the top and add a shebang (`#!`) followed by the Python interpreter you wish to use (if you have multiple). You can find this by running `which python3` at your terminal.
* Make sure you can execute this Python script. You can do this by running `sudo chmod +x yycnl-ankiaddcards.py`. This, in combination with the last step, will allow you to run the script directly (e.g. `./yycnl-ankiaddcards.py`).

# Python Script - Adding (a) note(s) (Non-Interactive Mode)
* Copy the `python_note_template.json` file to a new file.
* Modify the contents to add your term/definition for each card + the reverse card + references and tags.
* Copy the format for one of the JSON objects if you need to make more than two questions, though make sure you add a comment to the end of the prior one to adhere to proper JSON standards.
* Execute the script with the -f parameter (assuming you have set the importFromFile boolean to True in the script) and specify the location of your JSON template.
* Delete the backup file created if the original file looks intact and commit to your fork / PR to the main repository.

# Python Script - Adding (a) note(s) (Interactive Mode)
* Make sure the importFromFile boolean is set to False, or else you will get an error because -f is required if this is set to True. The default is False.
* Run the script. You'll be guided through the steps to input your terms/definitions, reverse term/definition, references, and tag lists for each card, providing the option to add as many as you need to.
* When you're finished - the changes will be written to the decKJSON specified. Delete the backup file if the original is intact and commit to your fork / PR to the main repository.
