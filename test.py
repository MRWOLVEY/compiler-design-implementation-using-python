# l=[0,1,2,3,4]
# follow=[]
# for i in range(len(l)):
#     if i == len(l)-1:
#         follow.append('$')
#     else:
#         follow.append(l[i+1])
# print(follow)

import re
# patt=r"(:[0-9]+)"
patt=r"(?<=_).+"
# patt=r"^:[0-9]+"
string="_>1:!:>1:+"
# string=">123"
res=re.findall(patt,string)
print(res[0].split(":"))