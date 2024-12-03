import re
class Compiler:
    def __init__(self):
        #defining the grammar
        self.Grammar={
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
        #addding the loop sequence to the grammar
        self.ptrOp=rf"({self.Grammar['ptr_mv_right']}|{self.Grammar['ptr_mv_left']})"
        self.expression=rf"({self.Grammar['add_num_val']}|{self.Grammar['add_acc']}|{self.Grammar['sub_num_val']}|{self.Grammar['sub_acc']}|{self.Grammar['inc_acc']}|{self.Grammar['dec_acc']}|{self.Grammar['ass_adds_acc']}|{self.Grammar['add_adds_acc']})"
        self.Grammar['loop_seq'] = rf"_({self.ptrOp}){{1}}(:{self.expression}|:{self.ptrOp})+"
    #defining custom erros
    class Lexical_Error(Exception):
        def __init__(self,exp):
            super().__init__(exp)
    
    #including and precessing the program
    class preProcessor:
        def __init__(self):#open the file
            self.file=open("input.cai","r")
            self.program=self.file.read()
            self.file.close()
        def process(self):
            a=re.sub(r'=.*','',self.program)
            b=re.findall(r"[^\n]",a)
            c=''.join(b).split(";")
            c.pop()#remove the last empty segment due to the last semicolon
            return c
    #lexical analysis: token list
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
                    raise self.Lexical_Error(f"invalid token: {exp}")
            return self.tokens
    #syntactic analysis: parse tree
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
    #code generation
    class CodeGenerator:
        def __init__(self):
            pass
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
    def compile(self):
        pp=self.preProcessor()
        proccessed_program=pp.process()
        lexer=self.Lexer(proccessed_program,self.Grammar)
        tokens=lexer.tokenize()
        parser=self.Parser(tokens,self.Grammar)
        parse_trees=parser.parse()
        code_generator=self.CodeGenerator()
        functions=code_generator.generate(parse_trees)
        return functions

#setting up the program
compiler=Compiler()
fns=compiler.compile()
print(fns)
#runtime errors
class RuntimeError(Exception):
    def __init__(self,exp):
        super().__init__(exp)
#program states
array=[0]*64
p=0
cP=0
acc=0
#running the compiled program
def run(functions):
    global array,p,cP,acc
    for fn in functions:
        if fn[0]=='ptr_mv_right':
            p+=fn[1]
            if p>63:
                raise RuntimeError("Index out of range")
        elif fn[0]=='ptr_mv_left':
            p-=fn[1]
            if p<0:
                raise RuntimeError("Index out of range")
        elif fn[0]=='add_num_val':
            array[p]+=fn[1]
        elif fn[0]=='add_acc':
            array[p]+=acc
        elif fn[0]=='sub_num_val':
            array[p]-=fn[1]
        elif fn[0]=='sub_acc':
            array[p]-=acc
        elif fn[0]=='inc_acc':
            acc+=fn[1]
        elif fn[0]=='dec_acc':
            acc-=fn[1]
        elif fn[0]=='ass_adds_acc':
            acc=array[p]
        elif fn[0]=='add_adds_acc':
            acc+=array[p]
        elif fn[0]=='loop_seq':
            cP+=p-cP
            segmentns=fn[1]
            run(segmentns[:1])
            loops=int(array[cP])
            for _ in range(loops):
                run(segmentns[1:])
run(fns)
print(array)
# for s in array:
#     if s>=32 and s<=126:
#         print(chr(s),end="")