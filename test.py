# l=[0,1,2,3,4]
# follow=[]
# for i in range(len(l)):
#     if i == len(l)-1:
#         follow.append('$')
#     else:
#         follow.append(l[i+1])
# print(follow)

# class CodeGenerator:
#     def __init__(self):
#         self.function_map = {
#             "ptr_mv_rt": self.generate_ptr_mv_rt,
#             "ptr_mv_left": self.generate_ptr_mv_left,
#             "add_num_val": self.generate_add_num_val,
#             "add_acc": self.generate_add_acc,
#             "sub_num_val": self.generate_sub_num_val,
#             "sub_acc": self.generate_sub_acc,
#             "inc_acc": self.generate_inc_acc,
#             "dec_acc": self.generate_dec_acc,
#             "ass_adds_acc": self.generate_ass_adds_acc,
#             "add_adds_acc": self.generate_add_adds_acc,
#             "loop_seq": self.generate_loop_seq
#         }

#     def generate_function(self, node):
#         generator = self.function_map.get(node.label)
#         if not generator:
#             raise ValueError(f"No function generator for label: {node.label}")
#         return generator(node)

#     def generate_ptr_mv_rt(self, node):
#         steps = int(node.children[1].value)
#         def ptr_mv_rt_fn(arr,ptr):
#             ptr+=steps
#             if ptr>=len(arr):
#                 raise IndexError("Index out of range")
#         return ptr_mv_rt_fn

#     def generate_ptr_mv_left(self, node):
#         steps = int(node.children[1].value)
#         def ptr_mv_left_fn(arr,ptr):
#             ptr-=steps
#             if ptr<0:
#                 raise IndexError("Index out of range")
#         return ptr_mv_left_fn

#     def generate_add_num_val(self, node):
#         value = int(node.children[1].value)
#         def add_num_val_fn(arr,ptr):
#             arr[ptr]+=value
#         return add_num_val_fn

#     def generate_add_acc(self, node):
#         def add_acc_fn(arr,ptr,acc):
#             ptr+=acc

#     def generate_loop_seq(self, node):
#         # Generate a sequence of functions for a loop
#         child_functions = [self.generate_function(child) for child in node.children]
#         def loop_seq_fn():
#             for fn in child_functions:
#                 fn()
#         return loop_seq_fn

# import re
# # patt=r"(:[0-9]+)"
# patt=r"(?<=_).+"
# # patt=r"^:[0-9]+"
# string="_>1:!:>1:+"
# # string=">123"
# res=re.findall(patt,string)
# print(res[0].split(":"))



print(())