import numpy as np
import json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.utils import asynckivy




def update_dict(tuple):
    file_path = "tic_tac_toe_dict.json"
    with open(file_path, 'r') as json_file:
        dict = json.load(json_file)
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

#מחשב - איקס
class Comp:
    def __init__(self, board):
        self.board = board

    def find_board(self, str_next_board, str_board):
        counter=0
        for i in range(9):
            if str_board[i]=='1' and str_next_board[i]!='1':
                return False
            if str_board[i]=='2' and str_next_board[i]!='2':
                return False
            if str_board[i] == '0' and str_next_board[i]=='1':
                return False
            if str_board[i] == '0' and str_next_board[i] == '2':
                counter+=1
        if counter != 1:
            return False
        return True

    def create_possible_boards_lst(self, str_board):
        file_path = "tic_tac_toe_dict.json"
        with open(file_path, 'r') as json_file:
            dict = json.load(json_file)
        list = []
        for key in dict:
            if self.find_board(key, str_board) == True:
                tuple = (key, dict[key][0])
                list.append(tuple)
        return list

    def find_best_board(self, lst):
        best_score = -1
        best_board = ""
        for i in lst:
            if i[1] > best_score:
                best_score = i[1]
                best_board = i[0]
        return best_board

    def play(self, str_board):
        lst = self.create_possible_boards_lst(str_board)
        best_board = self.find_best_board(lst)
        i = 0
        j = 0
        for k in range(9):
            if str_board[k] == '0' and best_board[k] == '2':
                break
            if j<2:
                j+=1
            else:
                j = 0
                i+=1
        self.board[i][j] = 2
        return (i,j)


#אדם - עיגול
class Grafic_Board(App):

    def build(self):
        self.board = np.zeros((3,3))
        self.board = self.board.astype(int)
        self.lst = []
        self.buttons = []
        self.c1 = Comp(self.board)
        self.layout = GridLayout(cols=3)
        str = np.array2string(self.board)
        str = self.change_str(str)
        self.lst.append(str)
        for i in range(3):
            for j in range(3):
                button = Button(background_normal='GUI_images/tic tac toe background.jpg')
                button.bind(on_press=self.human_play)
                button.pos_hint = {'center_x': (i), 'center_y': (j)}
                self.layout.add_widget(button)
                self.buttons.append(button)
        self.buttons = [self.buttons[i:i + 3] for i in range(0, len(self.buttons), 3)]
        return self.layout

    def human_play(self, instance):
        async def human_play():
            bool = False
            self.row = instance.pos_hint['center_x']
            self.cul = instance.pos_hint['center_y']
            self.buttons[self.row][self.cul].background_normal = 'GUI_images/tic tac toe round.jpg'
            self.board[self.row][self.cul] = 1
            str = np.array2string(self.board)
            str = self.change_str(str)
            self.lst.append(str)
            if self.check_circle_win() == True:
                await asynckivy.sleep(1)
                self.win()
                bool = True
            if self.check_full_board() == True and bool == False:
                await asynckivy.sleep(1)
                self.draw()
                bool = True
            if bool == False:
                await asynckivy.sleep(1)
                self.computer_play(str)
        asynckivy.start(human_play())

    def computer_play(self, str):
        async def computer_play(str):
            i , j = self.c1.play(str)
            self.board[i][j] = 2
            bool = False
            self.buttons[i][j].background_normal = 'GUI_images/tic tac toe x.jpg'
            str = np.array2string(self.board)
            str = self.change_str(str)
            self.lst.append(str)
            if self.check_x_win() == True:
                await asynckivy.sleep(1)
                self.lose()
                bool = True
            if self.check_full_board() == True and bool == False:
                await asynckivy.sleep(1)
                self.draw()
        asynckivy.start(computer_play(str))

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

    def check_full_board(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        return True

    def win(self):
        async def win():
            self.layout.clear_widgets()
            win_label = Label(text = "YOU WON!", font_size=100)
            self.layout.add_widget(win_label)
            update_dict((self.lst, 'lose'))
            await asynckivy.sleep(3)
            Window.close()
        asynckivy.start(win())

    def lose(self):
        async def lose():
            self.layout.clear_widgets()
            lost_label = Label(text = "YOU LOST!", font_size=100)
            self.layout.add_widget(lost_label)
            update_dict((self.lst, 'win'))
            await asynckivy.sleep(3)
            Window.close()
        asynckivy.start(lose())


    def draw(self):
        async def draw():
            self.layout.clear_widgets()
            draw_label = Label(text = "IT'S A DRAW!", font_size=100)
            self.layout.add_widget(draw_label)
            update_dict((self.lst, 'draw'))
            await asynckivy.sleep(3)
            Window.close()
        asynckivy.start(draw())







if __name__ == "__main__":

    Grafic_Board().run()

