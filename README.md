# tournament-converter-poker-snowie
Script used to convert tournament hands to cash game hands so it can be analyzed by Poker Snowie

## Installation 
Runs with python3 without any more dependencies.

## Usage
 1 - Change configuration in the .properties with your file path.   
 `path_to_winamax_hand_history` must point to the Winamax hand history folder. Make sure to enter the path with '/' character for folder delimitation or '\\\\' but not '\\'.   
 2 - Run   
```
python3 Parser.py
```   

## TODO-LIST
 - Rename every 'file' occurrences that are in fact a file name as 'file_name'   
 - Extract should load files into memory already and not just get file names