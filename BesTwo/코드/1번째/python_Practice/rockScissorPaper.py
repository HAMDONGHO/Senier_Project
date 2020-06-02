import time, random

print('play rock/scissor/paper')
play = True

while play:
    player = input('select : ')
    while (player != 'rock' and player != 'scissor' and player != 'paper'):
        player = input('select : ')
    
    computer = random.choice(['rock', 'scissor', 'paper'])
    time.sleep(1)
    
    if(player==computer):
        print('same')
    else:
        print(player)
        print(computer)
    userInput=input('retry? : ')
    if userInput=='n' :
        play=False
    