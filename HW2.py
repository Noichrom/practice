import snp
import pyautogui
import time

loc_food = [None] * 7
loc_stick = [None] * 5
food_amount = [None] * 7
loc_plate = [None] * 3
no_menu = 0
board = 0
stick_put = 0
start_time = 0
food_time = [[4.8, 6.0, 6.0, 7.0, 7.0],
             [5.0, 6.0, 6.0, 7.0, 7.0],
             [5.8, 6.5, 6.5, 7.0, 7.0],
             [6.3, 7.3, 7.3, 9.1, 9.1],
             [7.0, 7.8, 7.8, 12.2, 12.2],
             [7.0, 8.5, 8.5, 11.4, 11.4],
             [8.6, 10.0, 10.0, 13.5, 13.5]]


def start():
    global loc_plate, start_time

    ###按下開始###
    loc_start = snp.locateCenterOnScreen('start.png')
    pyautogui.click(loc_start[0],loc_start[1])
    time.sleep(1)
    start_time = time.time()

    ###偵測所有物件位置###
    for i in range(7):
        loc_food[i] = snp.locateOnScreen('food' + str(i) + '.png')
        if i < 4:
            loc_food[i] = (loc_food[i][0] + loc_food[i][2]*3/4, loc_food[i][1] + loc_food[i][3]/2, loc_food[i][2], loc_food[i][3])
        else:
            loc_food[i] = (loc_food[i][0] + loc_food[i][2]/4, loc_food[i][1] + loc_food[i][3]/2, loc_food[i][2], loc_food[i][3])
    for j in range(5):
        loc_stick[j] = snp.locateOnScreen('stick' + str(j) + '.png')
        loc_stick[j] = (loc_stick[j][0] + loc_stick[j][2]/2, loc_stick[j][1] + loc_stick[j][3]*3/4, loc_stick[j][2], loc_stick[j][3])
    loc_board = snp.locateCenterOnScreen('board.png')
    loc_plate = [[loc_stick[3][0], loc_board[1]], loc_board, [loc_stick[4][0], loc_board[1]]]


def take_second(a):

    return a[1]


def count_number(loc):
    ###根據y座標大小排序###
    loc.sort(key=take_second)

    ###刪除重複的項目###
    last_loc = 0
    delete = []
    for i in range(len(loc)):
        e = loc[i][1] - last_loc
        if e < 5:
            delete.append(i)
        last_loc = loc[i][1]
    for j in range(len(delete)):
        del loc[delete[j]-j]

    ###計算所需食物數量###
    number = len(loc)
    return number


def read_menu(num):
    loc_left = []
    loc_center = []
    loc_right = []
    number = [[]] * 3

    ###偵測菜單位於左、中還是右###
    for c in snp.locateAllOnScreen('menu'+str(num)+'.png'):
        if c[0] < loc_stick[3][0]:        #左
            loc_left.append(c)
        elif c[0] > loc_stick[2][0]:      #右
            loc_right.append(c)
        else:                             #中
            loc_center.append(c)
    loc = [loc_left, loc_center, loc_right]

    ###左、中、右分別計算食物數量###
    for i in range(3):
        number[i] = count_number(loc[i])
    return number


def take_food(food_amount):
    global stick_put, no_menu
    stick_put = 0
    stick_food = [None] * 5

    ###將食物取到烤肉架###
    for i in range(7):
        if food_amount[i][board % 3] != 0:
            for j in range(food_amount[i][board % 3]):
                pyautogui.moveTo(loc_food[i][0], loc_food[i][1], 0.1)
                pyautogui.dragTo(loc_stick[stick_put % 5][0], loc_stick[stick_put % 5][1], 0.1)
                stick_food[stick_put % 5] = i
                stick_put += 1
        else:
            no_menu += 1
    return stick_food


def finish(stick_food):
    global board
    stick_time = []
    last_time = 0

    ###對應所需時間###
    for i in range(5):
        if stick_food[i] != None:
            stick_time.append([i,food_time[stick_food[i]][i]])
    stick_time.sort(key=take_second)

    ###將食物取到盤中###
    for j in range(len(stick_time)):
        if time.time() - start_time < 200:
            time.sleep(stick_time[j][1] - last_time)
        pyautogui.moveTo(loc_stick[stick_time[j][0]][0], loc_stick[stick_time[j][0]][1], 0.1)
        pyautogui.dragTo(loc_plate[board % 3][0], loc_plate[board % 3][1], 0.1)
        last_time = stick_time[j][1]
    board += 1


###main###
start()
while True:
    if time.time() - start_time > 300:
        break
    else:
        time.sleep(0.5)
        for i in range(7):
            food_amount[i] = read_menu(i)
        while True:
            if no_menu < 7:
                stick_food = take_food(food_amount)
                break
            else:
                board += 1
                no_menu = 0
        finish(stick_food)


