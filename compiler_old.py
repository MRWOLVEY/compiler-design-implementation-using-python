#reading the input file
program=open("input.txt","r")
queue=[]
for line in program:
    if "=" in line[:10]: #to remove the comments
        continue
    tt=line.split(";") # ; marks code end
    queue.extend(tt)
program.close()

#removing the empty snippets
def isCode(x):
    return x not in [" ","\n",""]

queue=filter(isCode,queue)

# program states
array=[0]*64
p=0
cP=0
acc=0

for s in queue:
    if s[0]==">":
        p+=int(s[1:])
    elif s[0]=="<":
        p-=int(s[1:])
    elif s[0]=="+":
        if s[1:]!="":
            array[p]+=int(s[1:])
        else:
            array[p]+=acc
    elif s[0]=="-":
        if s[1:]!="":
            array[p]-=int(s[1:])
        else:
            array[p]-=acc
    elif s[0]=="!": # assigning a value to the accumulator
        if s[2]=="+":
            acc+=int(s[2:])
        elif s[2]=="-":
            acc-=int(s[2:])
        elif s[2]=="@": # assign the value at the pointer as it is
            acc=array[p]
        else:
            acc+=array[p] # add the value at the pointer to the accumulator
    elif s[0]=="_": # loop logic
        cP+=p-cP #moving the control pointer to the current pointer address
        while array[cP] > 0:
            for segment in s[1:].split(":"):
                if segment[0]==">":
                    p+=int(segment[1:])
                elif segment[0]=="<":
                    p-=int(segment[1:])
                elif s[0]=="+":
                    array[p]+=int(segment[1:])
                elif segment[0]=="-":
                    array[p]-=int(segment[1:])
                elif segment[0]=="!": # assigning a value to the accumulator
                    if segment[2]=="+":
                        acc+=int(segment[2:])
                    elif segment[2]=="-":
                        acc-=int(segment[2:])
                    elif segment[2]=="@": # assign the value at the pointer as it is
                        acc=array[p]
                    else:
                        acc+=array[p] # add the value at the pointer to the accumulator
            array[cP]-=1


print("array:",array)
# for s in array:
#     if s>=32 and s<=126:
#         print(chr(s),end="")