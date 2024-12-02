import re

class Lexical_Error(Exception):
    def __init__(self,exp):
        super().__init__(exp)

class preProcessor:
    def __init__(self):#open the file
        self.file=open("input.cai","r")
        self.program=self.file.read()
        self.file.close()
    def removeComments(self,program):#remove comments
        self.no_comments=re.sub(r'=.*','',program)
        return self.no_comments
    def removeEmptyLinesAndSpaces(self,exp):#remove spaces
        self.search=re.findall(r"[^\n]",exp)
        exp=''.join(self.search).split(";")
        exp.pop()#remove the last empty segment due to the last semicolon
        return exp


class Rule:
    def __init__(self,label,rule):
        self.label=label
        if type(rule)==Rule:
            self.rule=rule.rule
        self.rule=rule

Rules1=[Rule('ptr_mv_right',r">[0-9]+"),Rule('ptr_mv_left',r"<[0-9]+"),
       Rule('add_num_val',r"\+[0-9]+"),Rule('add_acc',r"\+"),Rule('sub_num_val',r"-[0-9]+"),
       Rule('sub_acc',r"-"),Rule('inc_acc',r"!\+[0-9]+"),Rule('dec_acc',r"!\-[0-9]+"),
       Rule('ass_adds_acc',r"!@"),Rule('add_adds_acc',r"!")]

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
ptrOp=rf"({Grammar['ptr_mv_right']}|{Grammar['ptr_mv_left']})"
expression=rf"({Grammar['add_num_val']}|{Grammar['add_acc']}|{Grammar['sub_num_val']}|{Grammar['sub_acc']}|{Grammar['inc_acc']}|{Grammar['dec_acc']}|{Grammar['ass_adds_acc']}|{Grammar['add_adds_acc']})"
Grammar['loop_seq'] = rf"_({ptrOp}){{1}}(:{expression}|:{ptrOp})+"

class Lexer:
    def __init__(self,program,grammar):
        self.exps=program
        self.grammar=grammar
        self.tokens=[]
    def tokenize(self):
        for exp in self.exps:
            valid=False
            for label,pattern in self.grammar.items():
                if re.fullmatch(pattern,exp):
                    valid=True
                    self.tokens.append((label,exp)) #should it be an object?
            if not valid:
                raise Lexical_Error(f"invalid token: {exp}")
        return self.tokens
    

firstAndFollow={'add_num_val':(r"\+",r"[0-9]+"),
                'add_acc':(r"\+",None),
                'sub_num_val':(r"-",r"[0-9]+"),
                'sub_acc':(r"-",None),
                'inc_acc':(r"!",r"\+"),
                'dec_acc':(r"!",r"-"),
                'ass_adds_acc':(r"!",r"@"),
                'add_adds_acc':(r"!",None),
                'ptr_mv_right':(r">",r"[0-9]+"),
                'ptr_mv_left':(r"<",r"[0-9]+")}


class Parser:
    def __init__(self,tokens,grammar):
        self.tokens=tokens
        self.parse_trees=[]
        self.grammar=grammar

    class Node:
        def __init__(self,value):
            self.value=value
            self.children=[]
        def add_child(self,node):
            self.children.append(node)
    def parse(self):
        for token in self.tokens:
            self.parse_trees.append(self.build_tree(token))
        return self.parse_trees
            
                
    def build_tree(self,token):
        tree=None
        if token[0]=='ptr_mv_right':
            tree=self.Node(token[0])
            tree.add_child(self.Node('>'))
            tree.add_child(self.Node(re.findall(r"(?<=>).+",token[1])[0]))
        elif token[0]=='ptr_mv_left':
            tree=self.Node(token[0])
            tree.add_child(self.Node('<'))
            tree.add_child(self.Node(re.findall(r"(?<=<).+",token[1])[0]))
        elif token[0]=='add_num_val':
            tree=self.Node(token[0])
            tree.add_child(self.Node('+'))
            tree.add_child(self.Node(re.findall(r"(?<=\+).+",token[1])[0]))
        elif token[0]=='add_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('+'))
        elif token[0]=='sub_num_val':
            tree=self.Node(token[0])
            tree.add_child(self.Node('-'))
            tree.add_child(self.Node(re.findall(r"(?<=-).+",token[1])[0]))
        elif token[0]=='sub_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('-'))
        elif token[0]=='inc_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('!'))
            tree.add_child(self.Node('+'))
            tree.add_child(self.Node(re.findall(r"(?<=\+).+",token[1])[0]))
        elif token[0]=='dec_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('!'))
            tree.add_child(self.Node('-'))
            tree.add_child(self.Node(re.findall(r"(?<=-).+",token[1])[0]))
        elif token[0]=='ass_adds_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('!'))
            tree.add_child(self.Node('@'))
        elif token[0]=='add_adds_acc':
            tree=self.Node(token[0])
            tree.add_child(self.Node('!'))
        elif token[0]=='loop_seq':
            tree=self.Node(token[0])
            tree.add_child(self.Node('_'))
            segmentns=re.findall(r"(?<=_).+",token[1])[0].split(':')
            tokens=[]
            for exp in segmentns:
                for label,pattern in self.grammar.items():
                    if re.fullmatch(pattern,exp):
                        tokens.append((label,exp))
            for token in tokens:
                tree.add_child(self.build_tree(token))
        return tree

class CodeGenerator:
    def __init__(self,parse_trees):
        self.parse_trees=parse_trees
        self.funcitons=[]
    def generate(self,parse_trees):
        functions=[]
        for tree in parse_trees:
            if tree.value=='ptr_mv_right':
                steps=int(tree.children[1].value)
                functions.append([tree.value,(steps)])
            elif tree.value=='ptr_mv_left':
                steps=int(tree.children[1].value)
                functions.append([tree.value,(steps)])
            elif tree.value=='add_num_val':
                value=int(tree.children[1].value)
                functions.append([tree.value,(value)])
            elif tree.value=='add_acc':
                functions.append([tree.value])
            elif tree.value=='sub_num_val':
                value=int(tree.children[1].value)
                functions.append([tree.value,(value)])
            elif tree.value=='sub_acc':
                functions.append([tree.value])
            elif tree.value=='inc_acc':
                value=int(tree.children[2].value)
                functions.append([tree.value,(value)])
            elif tree.value=='dec_acc':
                value=int(tree.children[2].value)
                functions.append([tree.value,(value)])
            elif tree.value=='ass_adds_acc':
                functions.append([tree.value])
            elif tree.value=='add_adds_acc':
                functions.append([tree.value])
            elif tree.value=='loop_seq':
                fns=self.generate(tree.children[1:])
                functions.append([tree.value,fns])
        return functions



pp=preProcessor()
tt=pp.removeComments(pp.program)
nn=pp.removeEmptyLinesAndSpaces(tt)
print("lexical units:",nn)
tokens=Lexer(nn,Grammar).tokenize()
print("tokens:",tokens)
p=Parser(tokens,Grammar)
parse_trees=p.parse()
fns=CodeGenerator(parse_trees).generate(parse_trees)
print("functions:",fns)

# print("parse trees:",p.parse_trees[0].children)
# for tree in p.parse_trees:
#     print(tree.value,)
#     for child in tree.children:
#         print(child.value,end=",")
#         if child.children:
#             print()
#             for child2 in child.children:
#                 print(child2.value,end=",")
#             print()
#     print()



    