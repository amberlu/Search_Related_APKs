The main.py file will find all related package names and it will at the same time
        1. Write all resultant apks in a text file stored in /outputs folder
        2. Write a log file with the date stored in /logs folder

###########################################
Instructions on how to run main.py. You can run 'python main.py --help' for reference.
Examples:

For developers:
Use either the numeric ID value (e.g., https://play.google.com/store/apps/dev?id=9133452689932095671)
python main.py --dev 9133452689932095671

Or the string ID value, in quotes if there are spaces (e.g. https://play.google.com/store/apps/developer?id=Amazon+Mobile+LLC)
python main.py --dev "Amazon Mobile LLC"

For category names:
python main.py --category 'Game Puzzle'

###########################################

The main.py calls functions from developer.py and category.py, which all can be executed alone. 
Read the two files for more details.


