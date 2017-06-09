The main.py file will find all related package names and it will at the same time
        1. Write all resultant apks in a text file stored in /outputs folder
        2. Write a log file with the date stored in /logs folder

###########################################
Instructions on how to run main.py. You can run 'python main.py --help' for reference.
Examples:

For developers:
If it is number encoded: run: python relate.py --num_dev googleDevId
                        e.x python relate.py --num_dev 8050969478732289508
If it is character encoded, run python relate.py --str_dev googleDevId_string
                        e.x python relate.py --str_dev 'zc game'

For category names:
run: python relate.py --category category_name
    e.x python relate.py --category 'Game Puzzle'


###########################################

The main.py calls functions from developer.py and category.py, which all can be executed alone. 
Read the two files for more details.


