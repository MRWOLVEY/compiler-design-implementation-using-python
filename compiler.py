import re

class Lexical_Error(Exception):
    def __init__(self,exp):
        super().__init__(exp)
class preProcessor:
    def __init__(self):#open the file
        self.file=open("input1.txt","r")
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
                'loop_seq':(r"_",r""),
                'ptr_mv_right':(r">",r"[0-9]+"),
                'ptr_mv_left':(r"<",r"[0-9]+")}


class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.parse_trees=[]

    class Node:
        def __init__(self,value):
            self.value=value
            self.children=[]
        def add_child(self,node):
            self.children.append(node)
    def parse(self):
        for token in self.tokens:
            self.parse_trees.append(self.build_tree(token))
            
                
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
            pass
        return tree

