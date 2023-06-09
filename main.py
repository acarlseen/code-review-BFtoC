'''


What does it all mean?!
> shifts to the right one cell
< shifts to the left one cell
+ increments the value of the current cell
- decrements the value of the current cell
[ begins a loop using value of current cell as the case, decrease to NULL
] ends a loop
. ends a "line" of code
, read a character from input and store to memory
'''

'''
Things to add:
Parenthesis counter/matching
***Process counter***
For loop func, include int k for loop condition. Pass value of register through for writing loop.

Potentially calling interpretBF recursively when encountering a left bracket '['
eliminates use of func loop()?
this might mean moving "current_register" to class variables
Pass a new instance of BFtoPy class with substring for matched right brackets ']' 

Basically something like:
if elem == '[':
    bracket_code = self.bf_code[self.bf_point, self.matchBracket
    
    
    
Found the problem! Loop is starting with the self.bf_point pointing at the end of the substring already
need a temporary variable to hold the place of the entering value
'''

registers = [0 for x in range(10)]
class BFtoPy:

    def __init__(self, bf_code: str, current_reg = 0):
        self.bf_code = bf_code
        self.bf_code_len = len(bf_code)
        self.bf_point = 0
        self.current_register = current_reg


    def transpilePY(self):
        py_code = open("transpilePY.py", 'w')
        temp = ''
        num_indent = 0
        indent = '\t'
        temp += 'registers = [0 for x in range(10)]\n'
        temp += 'current_register = 0\n'
        while self.bf_point in range(self.bf_code_len):
            multiple = self.howMany()
            elem = self.bf_code[self.bf_point]
            
            if elem == '>':
                temp += f'{num_indent * indent}current_register += {multiple}\n'
            
            elif elem == '<':
                temp += f'{num_indent * indent}current_register -= {multiple}\n'

            elif elem == '+':
                #print(f'Adding to register {self.current_register} value is {registers[self.current_register]}')
                temp += f'{num_indent * indent}registers[current_register] += {multiple} \n'

            elif elem == '-':
                temp += f'{num_indent * indent}registers[current_register] -= {multiple} \n'
                #print(f'Counting down register {self.current_register} now at {registers[self.current_register]}')

            elif elem == '[':
                temp += f'{num_indent * indent}for x in range(registers[current_register]): \n'
                num_indent += 1


            elif elem == ']':
                num_indent -= 1

            elif elem == '.':
                #print(registers[self.current_register])
                for _ in range(multiple):
                    temp += 'print(chr(registers[current_register])) \n'
            
            elif elem == ',':
                temp += 'registers[current_register] = input() \n'

            self.bf_point += multiple
        py_code.write(temp)

    def transpileC(self):
        py_code = open("transpileC.c", 'w')
        temp = ''
        num_indent = 1
        indent = '\t'
        temp += '#include <stdio.h>\n\n'
        temp += 'int registers[10] = {0};\n'
        temp += 'int current_register = 0;\n\n'
        temp += 'int main()\n{\n'
        temp += '\tchar output;\n'
        while self.bf_point in range(self.bf_code_len):
            multiple = self.howMany()
            elem = self.bf_code[self.bf_point]
            
            if elem == '>':
                temp += f'{num_indent * indent}current_register += {multiple};\n'
            
            elif elem == '<':
                temp += f'{num_indent * indent}current_register -= {multiple};\n'

            elif elem == '+':
                #print(f'Adding to register {self.current_register} value is {registers[self.current_register]}')
                temp += f'{num_indent * indent}registers[current_register] += {multiple}; \n'

            elif elem == '-':
                temp += f'{num_indent * indent}registers[current_register] -= {multiple}; \n'
                #print(f'Counting down register {self.current_register} now at {registers[self.current_register]}')

            elif elem == '[':
                temp += f'{num_indent * indent}while (registers[current_register] > 0) \n {num_indent * indent}{{\n'
                num_indent += 1


            elif elem == ']':
                num_indent -= 1
                temp += f'{num_indent * indent}}} \n'

            elif elem == '.':
                #print(registers[self.current_register])
                for _ in range(multiple):
                    #temp += f'{num_indent * indent}output = (char) registers[current_register];\n'
                    temp += f'{num_indent * indent}printf("%c", registers[current_register]); \n'
            
            elif elem == ',':
                temp += 'registers[current_register] = scanf(); \n'

            self.bf_point += multiple
        temp += '\treturn 0; \n'
        temp += '}'
        py_code.write(temp)
    

    def interpretBF(self):
        #print(f'interpretBF() executing')
        #print(f'{registers} at {id(registers)}')
        while self.bf_point in range(self.bf_code_len):
            multiple = self.howMany()
            elem = self.bf_code[self.bf_point]
            
            if elem == '>':
                self.current_register += multiple
            
            elif elem == '<':
                self.current_register -= multiple

            elif elem == '+':
                #print(f'Adding to register {self.current_register} value is {registers[self.current_register]}')
                registers[self.current_register] += multiple

            elif elem == '-':
                registers[self.current_register] -= multiple
                #print(f'Counting down register {self.current_register} now at {registers[self.current_register]}')

            elif elem == '[':
                loop_cond = registers[self.current_register]
                loop = self.matchBracket()
                #print(loop[1:-1])
                bracket = BFtoPy(loop[1:-1], self.current_register)
                while loop_cond > 0:
                    #print(f'loop_cond is {loop_cond}\n'
                    #      f'bracket.interpretBF() called')
                    bracket.interpretBF()
                    #print(f'Register 0 is at {registers[0]}')
                    bracket.bf_point = 0
                    loop_cond -= 1
                self.bf_point += len(loop) - 1
                #self.loop(bf_code[i:right_sq:], reg_manip)

            elif elem == ']':
                pass

            elif elem == '.':
                #print(registers[self.current_register])
                for _ in range(multiple):
                    print(chr(registers[self.current_register]))
            
            elif elem == ',':
                x = input()

            self.bf_point += multiple


    '''returns an index value for matching parenthesis/bracket'''
    def matchBracket(self) -> str:
        #print(f'matchBracket executing')
        bracket_count = 1
        right_bracket = self.bf_point + 1
        while bracket_count > 0 and right_bracket < self.bf_code_len:
            if self.bf_code[right_bracket] == '[':
                bracket_count += 1
            elif self.bf_code[right_bracket] == ']':
                bracket_count -= 1
            right_bracket += 1
        print(str(self.bf_code[self.bf_point: right_bracket]))
        return str(self.bf_code[self.bf_point: right_bracket])

    def howMany(self):
        #print(f'howMany() executing')
        this_many = 1
        i = self.bf_point
        while i < self.bf_code_len - 1 and self.bf_code[i] == self.bf_code[i+1]:
            this_many += 1
            i += 1
        #print(this_many)
        return this_many





text = open('./hell.bf', 'r')
data = text.read()
data = data.strip(' ')
#print(ord('e'))
print(data)

answer = BFtoPy(data)
answer.transpileC()


#print(answer.registers)
#print(len(answer.registers))