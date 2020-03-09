import operator
import os
import time

from Properties import Properties
from Transformer import Transformer


class ETL:
    """
    Extract, Transform, Load process of Winamax Tournament file in order to convert them into a format that
    Poker Snowie can understand so hands can be reviewed.
    """

    _history_path = ""
    _file_dict = {}
    _conv_suffix = "_converted"
    _tourney_names = {"Kill The Fish", "MONSTER STACK", "Birthday Freeroll"}
    _file_by_tourney = {}  # dict with a 'tourney_name' as key and a file as value.
    _eur_sym = "€"

    def __init__(self):
        """
        Constructor
        """
        self._history_path = Properties.properties["path_to_winamax_hand_history"]

    def launch(self):
        """
        Runs the whole ETL process
        """
        self.extract()
        for tourney_name, file_list in self._file_by_tourney.items():
            for file_name in file_list:
                new_file_data = self.transform_file(tourney_name, file_name)
                self.load(new_file_data, file_name)

    def extract(self):
        """
        First step of the ETL process : extract tournament files
        """
        dir_list = os.listdir(self._history_path)
        # print(dir_list)
        # get_modif_time(dir_list)
        self._file_by_tourney = self.get_files_to_convert(dir_list)  # todo we could merge this method within this one.

    def get_files_to_convert(self, dir_list):
        """
        Returns a map of file to convert indexed by their tournament name
        """
        files_to_convert = {}
        for t_name in self._tourney_names:
            files_to_convert[t_name] = []
            for file in dir_list:
                if (t_name in file) and ("summary" not in file) and ("converted" not in file):
                    files_to_convert[t_name].append(file)
                    print("{} tournament {} will be converted.".format(t_name, file))
        return files_to_convert

    def transform_file(self, tourney_name, file_name):
        """
        Map a file to its transformation method by the tournament name
        """
        file_path = self._history_path + "/" + file_name
        tn_name_length = len(tourney_name.split())
        return Transformer.transform_tournament_generic(file_path, tn_name_length)

    def load(self, new_file, original_file_name):
        """
        Load a transformed file into a new file
        """
        str_new_file = ""
        for line in new_file:
            for line2 in line:
                str_new_file = str_new_file + line2 + " "
            str_new_file = str_new_file + "\n"

        conv_file_name = original_file_name.replace(".txt", "_converted.txt")
        conv_file_path = self._history_path + "/" + conv_file_name
        if os.path.isfile(conv_file_path):
            print("File already exists, please delete it and try again")  # todo Why not overwrite ?
        else:
            with open(conv_file_path, 'a') as new_f:
                new_f.write(str_new_file)
                new_f.close()
                print("{} file was successfully converted as {}.".format(original_file_name, conv_file_name))

    def get_modif_time(self, dir_list):
        """
        For debug purpose ?
        :param dir_list:
        """
        for file in dir_list:
            # print("Last modified: %s" % time.ctime(os.path.getmtime(history_path+"/"+file)))
            self._file_dict[file] = time.ctime(os.path.getmtime(self._history_path + "/" + file))
        sorted_dict = sorted(self._file_dict.items(), key=operator.itemgetter(1))


if __name__ == "__main__":
    print("## Launching script ##")
    # Init the configuration
    Properties.init()

    # Running Transformer
    etl = ETL()
    etl.launch()
    print("## Script ended ##")
