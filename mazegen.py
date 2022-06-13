import random
import queue

# option thingy
go_nextx = [0,-1,0,1,0]
go_nexty = [0,0,1,0,-1]
xthing = [0,4,8,1,2]

# Generate maze
maze=[]
maze_x=27
maze_y=27
def dungeonmaze():
    global rooms
    global maze
    global room_location
    global mazeroom
    global states
    maze = []
    for i in range(maze_y):
        mazeline = []
        for j in range(maze_x):
            mazeline.append(0)
        maze.append(mazeline)
    #print (maze)
    #3+7+3+7+3+7+3
    mazeroom = [[0,0,0],
                [0,0,0],
                [0,0,0]]
    rooms = 0
    rooms = random.randint(2,9)
    room_location = random.sample(range(1,10),rooms)
    states = [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0],
              [0,0,0,0,0]]
    for room in room_location:
        room = room-1
        mazeroom[room//3][room%3] = 1
        states[(room//3)*2][(room%3)*2]=16
    newroom = []
    for i in range(len(room_location)-1):
        room = room_location[i]-1
        newroom=[((room//3)*2,(room%3)*2)]
        roomg = room_location[i+1]-1
        roomgoal = (((roomg//3)*2,(roomg%3)*2))
        direction=random.randint(1,4)
        choices = [1,2,3,4]
        #print('start_here')
        #print(room)
        while True:
            #print('hi')
            #print(direction)
            if direction == 1:
                if room//3==0:
                    direction = random.choice((2,3,4))
                else:
                    #print ((room//3)*2-1,(room%3)*2)
                    choices = [1,2,3,4]
                    choices.remove(3)
                    if ((room//3)*2-1,(room%3)*2) in newroom and states[(room//3)*2-1][(room%3)*2] & 4:
                        newroom.append(((room//3)*2-1,(room%3)*2))
                        break
                    newroom.append(((room//3)*2-1,(room%3)*2))
                    states[(room//3)*2-1][(room%3)*2]+=4
                    break
            elif direction == 2:
                if room%3 == 2:
                    direction = random.choice((1,3,4))
                else:
                    #print((room//3)*2,(room%3)*2+1)
                    choices = [1,2,3,4]
                    choices.remove(4)
                    if ((room//3)*2,(room%3)*2+1) in newroom and states[(room//3)*2][(room%3)*2+1] & 8:
                        newroom.append(((room//3)*2,(room%3)*2+1))
                        break
                    newroom.append(((room//3)*2,(room%3)*2+1))
                    states[(room//3)*2][(room%3)*2+1]+=8
                    break
            elif direction == 3:
                if room//3==2:
                    direction = random.choice((1,2,4))
                else:
                    #print ((room//3)*2+1,(room%3)*2)
                    choices = [1,2,3,4]
                    choices.remove(1)
                    if ((room//3)*2+1,(room%3)*2) in newroom and states[(room//3)*2+1][(room%3)*2] & 1:
                        newroom.append(((room//3)*2+1,(room%3)*2))
                        break
                    newroom.append(((room//3)*2+1,(room%3)*2))
                    states[(room//3)*2+1][(room%3)*2]+=1
                    break
            elif direction == 4:
                if room%3==0:
                    direction = random.choice((1,2,3))
                else:
                    #print ((room//3)*2,(room%3)*2-1)
                    choices = [1,2,3,4]
                    choices.remove(2)
                    if ((room//3)*2,(room%3)*2-1) in newroom and states[(room//3)*2][(room%3)*2-1] & 2:
                        newroom.append(((room//3)*2,(room%3)*2-1))
                        break
                    newroom.append(((room//3)*2,(room%3)*2-1))
                    states[(room//3)*2][(room%3)*2-1]+=2
                    break
        while roomgoal not in newroom:
            curroom = newroom[-1]
            #print(curroom)
            #print(roomgoal, curroom)
            while True:
                direction=random.choice(choices)
                #print(direction)
                #print(curroom, direction)
                if direction == 1:
                    if curroom[0]<=0:
                        choices.remove(1)
                    else:
                        if states[curroom[0]-1][curroom[1]] & 4 or states[curroom[0]][curroom[1]] & 1:
                            newroom.append((curroom[0]-1,curroom[1]))
                        elif states[curroom[0]][curroom[1]] == 16:
                            newroom.append((curroom[0]-1,curroom[1]))
                            # add code
                            if not states[curroom[0]-1][curroom[1]] & 4:
                                states[curroom[0]-1][curroom[1]]+=4
                            # /add code
                        elif states[curroom[0]-1][curroom[1]] == 16:
                            newroom.append((curroom[0]-1,curroom[1]))
                            # add code
                            if not states[curroom[0]][curroom[1]] & 1:
                                states[curroom[0]][curroom[1]]+=1
                            # /add code
                        else:
                            newroom.append((curroom[0]-1,curroom[1]))
                            states[curroom[0]][curroom[1]]+=1
                            states[curroom[0]-1][curroom[1]]+=4
                        choices = [1,2,3,4]
                        choices.remove(3)
                        break
                elif direction == 2:
                    if curroom[1]>=4:
                        choices.remove(2)
                    else:
                        if states[curroom[0]][curroom[1]+1] & 8 or states[curroom[0]][curroom[1]] & 2:
                            newroom.append((curroom[0],curroom[1]+1))
                        elif states[curroom[0]][curroom[1]] == 16:
                            newroom.append((curroom[0],curroom[1]+1))
                            # add code
                            if not states[curroom[0]][curroom[1]+1] & 8:
                                states[curroom[0]][curroom[1]+1]+=8
                            # /add code
                            states[curroom[0]][curroom[1]+1]+=8
                        elif states[curroom[0]][curroom[1]+1] == 16:
                            newroom.append((curroom[0],curroom[1]+1))
                            # add code
                            if not states[curroom[0]][curroom[1]] & 2:
                                states[curroom[0]][curroom[1]]+=2
                            # /add code
                            #states[curroom[0]][curroom[1]]+=2
                        else:
                            newroom.append((curroom[0],curroom[1]+1))
                            states[curroom[0]][curroom[1]]+=2
                            states[curroom[0]][curroom[1]+1]+=8
                        choices = [1,2,3,4]
                        choices.remove(4)
                        break
                elif direction == 3:
                    if curroom[0]>=4:
                        choices.remove(3)
                    else:
                        if states[curroom[0]+1][curroom[1]] & 1 or states[curroom[0]][curroom[1]] & 4:
                            newroom.append((curroom[0]+1,curroom[1]))
                        elif states[curroom[0]][curroom[1]] == 16:
                            newroom.append((curroom[0]+1,curroom[1]))
                            # add code
                            if not states[curroom[0]+1][curroom[1]] & 1:
                                states[curroom[0]+1][curroom[1]]+=1
                            # /add code
                            #states[curroom[0]+1][curroom[1]]+=1
                        elif states[curroom[0]+1][curroom[1]] == 16:
                            newroom.append((curroom[0]+1,curroom[1]))
                            # add code
                            if not states[curroom[0]][curroom[1]] & 4:
                                states[curroom[0]][curroom[1]]+=4
                            # /add code
                            #states[curroom[0]][curroom[1]]+=4
                        else:
                            newroom.append((curroom[0]+1,curroom[1]))
                            states[curroom[0]][curroom[1]]+=4
                            states[curroom[0]+1][curroom[1]]+=1
                        choices = [1,2,3,4]
                        choices.remove(1)
                        break
                elif direction == 4:
                    if curroom[1]<=0:
                        choices.remove(4)
                    else:
                        if states[curroom[0]][curroom[1]-1] & 2 or states[curroom[0]][curroom[1]] & 8:
                            newroom.append((curroom[0],curroom[1]-1))
                        elif states[curroom[0]][curroom[1]] == 16:
                            newroom.append((curroom[0],curroom[1]-1))
                            # add code
                            if not states[curroom[0]][curroom[1]-2] & 2:
                                states[curroom[0]][curroom[1]-1]+=2
                            # /add code
                            #states[curroom[0]][curroom[1]-1]+=2
                        elif states[curroom[0]][curroom[1]-1] == 16:
                            newroom.append((curroom[0],curroom[1]-1))
                            states[curroom[0]][curroom[1]]+=8
                        else:
                            newroom.append((curroom[0],curroom[1]-1))
                            states[curroom[0]][curroom[1]]+=8
                            states[curroom[0]][curroom[1]-1]+=2
                        choices = [1,2,3,4]
                        choices.remove(2)
                        break
    for i in range(0,25,5):
        for j in range(0,25,5):
            if states[i//5][j//5] >= 16:
                for k in range(5):
                    for l in range(5):
                        maze[i+k+1][j+l+1] = 1
            if states[i//5][j//5] & 8:
                for k in range(3):
                    maze[i+2+1][j+k+1] = 1
            if states[i//5][j//5] & 4:
                for k in range(3):
                    maze[i+2+k+1][j+2+1] = 1
            if states[i//5][j//5] & 2:
                for k in range(3):
                    maze[i+3][j+3+k] = 1
            if states[i//5][j//5] & 1:
                for k in range(3):
                    maze[i+k+1][j+3] = 1
def mazeprint():
    print()
    print(rooms)
    print()
    print (room_location)
    print()
    for i in range(3):
        for j in range(3):
            print(mazeroom[i][j],end=' ')
        print()
    print()
    for i in range(5):
        for j in range(5):
            print(states[i][j],end=' ')
        print()

    for i in range(0,25,5):
        for j in range(0,25,5):
            if states[i//5][j//5] >= 16:
                for k in range(5):
                    for l in range(5):
                        maze[i+k+1][j+l+1] = 1
            if states[i//5][j//5] & 8:
                for k in range(3):
                    maze[i+2+1][j+k+1] = 1
            if states[i//5][j//5] & 4:
                for k in range(3):
                    maze[i+2+k+1][j+2+1] = 1
            if states[i//5][j//5] & 2:
                for k in range(3):
                    maze[i+3][j+3+k] = 1
            if states[i//5][j//5] & 1:
                for k in range(3):
                    maze[i+k+1][j+3] = 1

    for i in range(maze_y):
        mazeline = []
        for j in range(maze_x):
            mazeline.append(maze[i][j])
        print(mazeline)


def bfs():
    visited = [[0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0],
               [0,0,0,0,0]]
    start = 0
    startloc = 0
    while start == 0:
        if states[startloc//5][startloc%5]>0:
            start = 1
            startloc-=1
        startloc+=1
    q = queue.Queue(0)
    q.put(startloc)
    while not q.empty():
        curloc = q.get()
        go_next = []
        #print()
        #print (curloc)
        if visited[curloc//5][curloc%5]==1:
            continue
        visited[curloc//5][curloc%5] = 1
        if states[curloc//5][curloc%5] >= 16:
            go_next = [1,2,3,4]
        else:
            if states[curloc//5][curloc%5] & 1: go_next.append(1)
            if states[curloc//5][curloc%5] & 2: go_next.append(2)
            if states[curloc//5][curloc%5] & 4: go_next.append(3)
            if states[curloc//5][curloc%5] & 8: go_next.append(4)
        #print (go_next)
        #print ()
        for option in go_next:
            #print (option, go_nextx[option], go_nexty[option])
            if curloc//5+go_nextx[option] < 5 and curloc//5+go_nextx[option] >= 0:
                if curloc%5+go_nexty[option] < 5 and curloc%5 + go_nexty[option] >= 0:
                    #print('here')
                    #print(curloc//5+go_nextx[option],curloc%5+go_nexty[option])
                    if states[curloc//5+go_nextx[option]][curloc%5+go_nexty[option]] & xthing[option] or states[curloc//5+go_nextx[option]][curloc%5+go_nexty[option]] > 15:
                        #print('there')
                        #print((curloc//5+go_nextx[option])*5+curloc%5+go_nexty[option])
                        #print()
                        q.put((curloc//5+go_nextx[option])*5+curloc%5+go_nexty[option])
    for i in range(25):
        if visited[i//5][i%5] == 0 and states[i//5][i%5] > 0:
            return False
    return True
            
def goodmaze():
    dungeonmaze()
    if not bfs():
        goodmaze()

def badmaze():
    dungeonmaze()
    if bfs():
        badmaze()
"""
dungeonmaze()
print(bfs())
mazeprint()
"""
"""
goodmaze()
mazeprint()
goodmaze()
mazeprint()
goodmaze()
mazeprint()
"""
