import random
import numpy as np
import json

class Games:
    def __init__(self):
        file_path = "tic_tac_toe_dict.json"
        with open(file_path, 'r') as json_file:
            dict = json.load(json_file)
        for k in range(100000):
            g1 = game()
            tuple = g1.play()
            list = tuple[0]
            if tuple[1] == 'lose':
                for i in list:
                    if i not in dict:
                        dict[i] = (0,1)
                    else:
                        average = (dict[i][0]*dict[i][1])/(dict[i][1]+1)
                        dict[i] = (average, dict[i][1]+1)
            if tuple[1] == 'win':
                num = 1
                for i in reversed(list):
                    if i not in dict:
                        dict[i] = (num,1)
                    else:
                        average = ((dict[i][0]*dict[i][1]) + num)/(dict[i][1]+1)
                        dict[i] = (average, dict[i][1]+1)
                    num = num*0.9
            if tuple[1] == 'draw':
                num = 0.5
                for i in reversed(list):
                    if i not in dict:
                        dict[i] = (num,1)
                    else:
                        average = ((dict[i][0]*dict[i][1]) + num)/(dict[i][1]+1)
                        dict[i] = (average, dict[i][1]+1)
                    num = num*0.9

        with open(file_path, 'w') as json_file:
            json.dump(dict, json_file)


class game:
    def __init__(self):
        self.board = np.zeros((3,3))
        self.board = self.board.astype(int)
        self.lst = []
    def play(self):
        r1 = random_player1(self.board)
        r2 = random_player2(self.board)
        str = np.array2string(self.board)
        str = self.change_str(str)
        self.lst.append(str)
        print(self.board)
        bool = ''
        for i in range(9):
            if i%2==0:
                r1.play()
                print(self.board)
                str = np.array2string(self.board)
                str = self.change_str(str)
                self.lst.append(str)
                if self.check_circle_win():
                    bool = 'lose'
                    break
            else:
                r2.play()
                print(self.board)
                str = np.array2string(self.board)
                str = self.change_str(str)
                self.lst.append(str)
                if self.check_x_win():
                    bool = 'win'
                    break
        if bool == '':
            bool = 'draw'
        return (self.lst, bool)


    def change_str(self, str):
        str = str.replace("[", "")
        str = str.replace("]", "")
        str = str.replace(" ", "")
        str = str.replace("\n", "")
        return str

    def check_circle_win(self):
        counter = 0
        for i in range (3):
            for j in range(3):
                if self.board[i][j]==1:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range (3):
            for j in range(3):
                if self.board[j][i]==1:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range(3):
            if self.board[i][i] == 1:
                counter +=1
        if counter == 3:
            return True
        counter = 0
        for i in range(3):
            if self.board[i][2-i] == 1:
                counter +=1
        if counter == 3:
            return True
        return False

    def check_x_win(self):
        counter = 0
        for i in range (3):
            for j in range(3):
                if self.board[i][j]==2:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range (3):
            for j in range(3):
                if self.board[j][i]==2:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range(3):
            if self.board[i][i] == 2:
                counter +=1
        if counter == 3:
            return True
        counter = 0
        for i in range(3):
            if self.board[i][2-i] == 2:
                counter +=1
        if counter == 3:
            return True
        return False


class random_player2:
    def __init__(self, board):
        self.board = board

    def play(self):
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        while self.board[x][y] != 0:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        self.board[x][y] = 2


class random_player1:
    def __init__(self, board):
        self.board = board

    def play(self):
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        while self.board[x][y] != 0:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
        self.board[x][y] = 1





def update_dict():
    file_path = "tic_tac_toe_dict.json"
    with open(file_path, 'r') as json_file:
        dict = json.load(json_file)
    for l in dict:
        numeric_elements = [int(l[i:i+1]) for i in range(0, len(l), 1)]
        array = np.array(numeric_elements).reshape(3, 3)
        counter = 0
        if num_win(array)>0 and dict[l][0]!=1:
            dict[l][0] = dict[l][0]/2
        for k in range(3):
            for j in range(3):
                if array[k][j] == 0:
                    array[k][j] = 1
                    if num_win(array) >=2:
                        counter+=1
                    array[k][j] = 0
        if counter>0 and dict[l][0]!=1:
            dict[l][0] = dict[l][0]/1.5
    with open(file_path, 'w') as json_file:
            json.dump(dict, json_file)


def num_win(array):
    counter = 0
    for k in range(3):
        for j in range(3):
            if array[k][j] == 0:
                array[k][j] = 1
                if check_circle_win(array) == True:
                    counter+=1
                array[k][j] = 0
    return counter


def check_circle_win(board):
        counter = 0
        for i in range (3):
            for j in range(3):
                if board[i][j]==1:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range (3):
            for j in range(3):
                if board[j][i]==1:
                    counter+=1
            if counter == 3:
                return True
            counter = 0
        for i in range(3):
            if board[i][i] == 1:
                counter +=1
        if counter == 3:
            return True
        counter = 0
        for i in range(3):
            if board[i][2-i] == 1:
                counter +=1
        if counter == 3:
            return True
        return False




if __name__ == '__main__':

    #g = Games()
    #update_dict()
    '''dict = {}
    file_path = "tic_tac_toe_dict.json"
    with open(file_path, 'w') as json_file:
            json.dump(dict, json_file)'''




