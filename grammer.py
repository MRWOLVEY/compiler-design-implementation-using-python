import re

Grammar={
    'ptr_mv_right': r">[0-9]+",
    'ptr_mv_left': r"<[0-9]+",
    'add_num_val': r"\+[0-9]+",
    'add_acc': r"\+",
    'sub_num_val': r"-[0-9]+",
    'sub_acc': r"-",
    'inc_acc': r"!\+[0-9]+",
    'dec_acc': r"!\-[0-9]+",
    'ass_adds_acc': r"!@",
    'add_adds_acc': r"!"
}

a=r">[0-9]+|\+[0-9]+"
# Grammar['loop_seq']=f"_({Grammar['ptr_mv_right']|Grammar['ptr_mv_left']}){{1}}(\:({Grammar['add_num_val']|Grammar['add_acc']|Grammar['sub_num_val']|Grammar['sub_acc']|Grammar['inc_acc']|Grammar['dec_acc']|Grammar['ass_adds_acc']|Grammar['add_adds_acc']}){{1}})+"
# Grammar['loop_seq'] = rf"_({Grammar['ptr_mv_right']}|{Grammar['ptr_mv_left']}){{1}}:(({Grammar['add_num_val']}|{Grammar['add_acc']}|{Grammar['sub_num_val']}|{Grammar['sub_acc']}|{Grammar['inc_acc']}|{Grammar['dec_acc']}|{Grammar['ass_adds_acc']}|{Grammar['add_adds_acc']}){{1}})+"
# Grammar['loop_seq'] = rf"_({Grammar['ptr_mv_right']}|{Grammar['ptr_mv_left']}){{1}}:(({Grammar['add_num_val']}|{Grammar['add_acc']}|{Grammar['sub_num_val']}|{Grammar['sub_acc']}|{Grammar['inc_acc']}|{Grammar['dec_acc']}|{Grammar['ass_adds_acc']}|{Grammar['add_adds_acc']}){{1}}(:({Grammar['add_num_val']}|{Grammar['add_acc']}|{Grammar['sub_num_val']}|{Grammar['sub_acc']}|{Grammar['inc_acc']}|{Grammar['dec_acc']}|{Grammar['ass_adds_acc']}|{Grammar['add_adds_acc']}){{1}})*)"

ptrOp=rf"({Grammar['ptr_mv_right']}|{Grammar['ptr_mv_left']})"
expression=rf"({Grammar['add_num_val']}|{Grammar['add_acc']}|{Grammar['sub_num_val']}|{Grammar['sub_acc']}|{Grammar['inc_acc']}|{Grammar['dec_acc']}|{Grammar['ass_adds_acc']}|{Grammar['add_adds_acc']})"
Grammar['loop_seq'] = rf"_({ptrOp}){{1}}(:{expression}|:{ptrOp})+"


test1="_>1:!:>1:+"
test2="_>1:<1:>1"

print(re.findall(Grammar['loop_seq'],test1))