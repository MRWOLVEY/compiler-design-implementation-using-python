#reading the input file
program=open("input.txt","r")
queue=[]
for line in program:
    if "//" in line[:10]: #to remove the comments
        continue
    tt=line.split(";") # ; marks code end
    queue.extend(tt)
program.close()

#removing the empty snippets
def isCode(x):
    return x not in [" ","\n",""]

queue=filter(isCode,queue)
print(queue)


# program states
array=[0]*20
p=0
acc=0

for s in queue:
    if s[0]==">":
        p+=int(s[1:])
    elif s[0]=="<":
        p-=int(s[1:])
    elif s[0]=="+":
        array[p]+=int(s[1:])
    elif s[0]=="-":
        array[p]-=int(s[1:])
    
print(array)
for s in array:
    if s>=32 and s<=126:
        print(chr(s),end="")