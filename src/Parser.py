import os
import time
import operator

history_path = "C:/Users/NaG/Documents/Winamax Poker/accounts/NaG01/history"
file_dict = {}
conv_suffix= "_converted"
tourney_names = {"Kill The Fish"}
str_euro = "€"


def main():
    dir_list = os.listdir(history_path)
    #print(dir_list)
    #get_modif_time(dir_list)
    files_to_convert = get_files_to_convert(dir_list)
    convert_files(files_to_convert)


def get_files_to_convert(dir_list):
    files_to_convert = []
    for file in dir_list:
        for t_name in tourney_names:
            if((t_name in file) and ("summary" not in file) and ("converted" not in file)):
                files_to_convert.append(file)
                print(file)
    return files_to_convert


def convert_files(files_to_convert):
    for file in files_to_convert:
        f = open(history_path+"/"+file)
        new_file = []
        player_names = []
        summary = 0
        for line in f:
            split_l = line.split()
            new_line = []
            if(split_l):
                #First line of a new hand = need to change it to make it into a Cash game hand
                if(split_l[0]=="Winamax"):
                    new_line.append(split_l[0]) #Winamax
                    new_line.append(split_l[1]) #Poker
                    new_line.append("-") #-
                    new_line.append("CashGame") #replace tournament name with "CashGame"
                    new_line.append("-")
                    new_line.append("HandId:")
                    new_line.append(split_l[15])
                    new_line.append("-")
                    new_line.append("Holdem")
                    new_line.append("no")
                    new_line.append("limit")
                    index = split_l[20].find("/")
                    str_stakes = split_l[20][index+1:]
                    str_stakes = "(" + str_stakes
                    str_stakes = str_stakes.replace("/", "€/")
                    str_stakes_fin = str_stakes.replace(")", "€)")
                    new_line.append(str_stakes_fin)
                    new_line.append("-")
                    new_line.append(split_l[-3])
                    new_line.append(split_l[-2])
                    new_line.append(split_l[-1])
                    #print(new_line)
                    new_file.append(new_line)
                    #split_l = []
                    #new_line = []
                elif((split_l[0]=="Seat") and (summary==0)):
                    new_line.append(split_l[0])
                    new_line.append(split_l[1])
                    #Added support for player with multiple word names
                    str_length = len(split_l)
                    #print(str_length)
                    if(str_length>4):
                        player_name = ""
                        for i in range(2,str_length-1):
                            if(i<str_length-2):
                                player_name = player_name + split_l[i] + " "
                            else:
                                player_name = player_name + split_l[i]
                    else:
                        player_name = split_l[2]
                    #print(player_name)
                    new_line.append(player_name)
                    if(player_name not in player_names):
                        player_names.append(player_name)
                    str_stack = split_l[-1].replace(")", "€)")
                    new_line.append(str_stack)
                    new_file.append(new_line)
                #Lines describing players actions
                elif(split_l[0] in player_names):
                    new_line.append(split_l[0])
                    #Posts line
                    if(split_l[1]=="posts"):
                        new_line.append(split_l[1])
                        #Ante is posted
                        if(split_l[2]=="ante"):
                            new_line.append(split_l[2])
                            new_ante = split_l[3] + "€"
                            new_line.append(new_ante)
                            new_file.append(new_line)
                        #Small or big blind posted
                        elif((split_l[2]=="small") or (split_l[2]=="big")):
                            new_line.append(split_l[2])
                            new_line.append(split_l[3])
                            new_blind = split_l[4] + "€"
                            new_line.append(new_blind)
                            new_file.append(new_line)
                    #Player folds or checks
                    elif((split_l[1]=="folds") or (split_l[1]=="checks")):
                        new_line.append(split_l[1])
                        new_file.append(new_line)
                    #Player calls or bets
                    elif((split_l[1]=="calls") or (split_l[1]=="bets")):
                        new_line.append(split_l[1])
                        new_call = split_l[2] + "€"
                        new_line.append(new_call)
                        #"and is all-in" case
                        if(len(split_l)>3):
                            new_line.append(split_l[3])
                            new_line.append(split_l[4])
                            new_line.append(split_l[5])
                        new_file.append(new_line)
                    #Player raises
                    elif(split_l[1]=="raises"):
                        new_line.append(split_l[1])
                        new_start_raise = split_l[2] + "€"
                        new_line.append(new_start_raise)
                        new_line.append(split_l[3])
                        new_end_raise = split_l[4] + "€"
                        new_line.append(new_end_raise)
                        #"and is all-in" case
                        if(len(split_l)>5):
                            new_line.append(split_l[5])
                            new_line.append(split_l[6])
                            new_line.append(split_l[7])
                        new_file.append(new_line)
                    #Player collected money from pot
                    elif(split_l[1]=="collected"):
                        new_line.append(split_l[1])
                        new_winnings = split_l[2] + "€"
                        new_line.append(new_winnings)
                        new_line.append(split_l[3])
                        new_line.append(split_l[4])
                        #Take into account "side pot n"
                        if(len(split_l)>5): 
                            new_line.append(split_l[5])
                            if(len(split_l)>6): 
                                new_line.append(split_l[6])
                        new_file.append(new_line)
                    #Line starts with player name but doesn't need to be changed
                    else:
                        idx = 0
                        for word in split_l:
                            if (idx>0):
                                new_line.append(word)
                            idx = idx +1
                        new_file.append(new_line)
                #Different behaviour in summary
                elif((split_l[0]=="***") and (split_l[1]=="SUMMARY")):
                    summary = 1
                    new_line.append(split_l[0])
                    new_line.append(split_l[1])
                    new_line.append(split_l[2])
                    new_file.append(new_line)
                elif((split_l[0]=="Total") and (summary==1)):
                    prev_word = ""
                    for word in split_l:
                        if(prev_word=="pot"):
                            new_line.append(word+"€")
                            prev_word=""
                        else:
                            new_line.append(word)
                        if word=="pot":
                            prev_word = word
                    new_file.append(new_line)
                elif((split_l[0]=="Seat") and (summary==1)):
                    prev_word = ""
                    for word in split_l:
                        if(prev_word=="won"):
                            new_line.append(word+"€")
                            prev_word=""
                        else:
                            new_line.append(word)
                        if word=="won":
                            prev_word = word
                    new_file.append(new_line)
                #Any line that doesn't start with a player name and doesn't need to be changed
                #Is just copied
                else:
                    for word in split_l:
                        new_line.append(word)
                    new_file.append(new_line)
                #print(new_line)
            else:
                summary = 0
                new_file.append("")

        str_new_file = ""
        for line in new_file:
            for line2 in line:
                str_new_file = str_new_file + line2 + " "
            str_new_file = str_new_file + "\n"

        orig_file = history_path+"/"+file
        conv_file = orig_file.replace(".txt", "_converted.txt")
        if(os.path.isfile(conv_file)):
            print("File already exists, please delete it and try again")
        else:
            with open(conv_file, 'a') as new_f:
                for line in str_new_file:
                    new_f.write(line)
                new_f.close()


    
def get_modif_time(dir_list):
    for file in dir_list:
        #print("Last modified: %s" % time.ctime(os.path.getmtime(history_path+"/"+file)))
        file_dict[file] = time.ctime(os.path.getmtime(history_path+"/"+file))
    sorted_dict = sorted(file_dict.items(), key=operator.itemgetter(1))



main()
