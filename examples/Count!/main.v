int start = 1
int countUpGoal = 10000
int countDownGoal = 1
int goalWasReached = 0
int goalCheck = 0

# Count up!

writeLine "Going Up!"
location loop
writeLine start
if start == countUpGoal
    goalWasReached += 1
start += 1

# If the goal has not been reached yet, loop 
if goalWasReached == goalCheck
    goto loop 

# Compensate for the extra +1 I do after writing 
start -= 1

# Count Down!
writeLine "Going Down!"
location loop_down 
writeLine start 
if start == countDownGoal 
    jump 3 
start -= 1
goto loop_down 
writeLine "GoodBye"
wait 3
writeLine "Jk. Let's go again!"
wait 1
start = 1 
goalWasReached = 0
jumpTo 6
exit
