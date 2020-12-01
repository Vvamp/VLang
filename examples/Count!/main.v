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
    exit 
start -= 1
goto loop_down 

