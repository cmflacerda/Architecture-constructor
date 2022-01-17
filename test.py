import os
import json
import re
import numpy as np
import pandas as pd
import sys
from numpy.core.fromnumeric import mean

from function_names_extractor import FunctionsIdentifier

class TraceFunc:
    
    def __init__(self):
        
        self.ROOT = os.getcwd()
        self.indent_list = []
        self.dict_to_df = {}
        with open(f'{self.ROOT}/directores.json', 'r') as f:
            self.dir = json.load(f)


    def tracefunc(self, frame, event, arg, indent=[0]):
              
        
        with open(f'{self.ROOT}/output_tracefunc.txt', 'a+') as f:
            dir_searched = re.compile(r'([\W\w*]*(?=\/\w*\.py))').findall(frame.f_code.co_filename)
            if len(dir_searched) > 0:
                if event == "call":
                    indent[0] += 2
                    if dir_searched[0] in self.dir:
                        self.indent_list.append(indent[0])
                        f.write(str(indent[0]) + f" call function {frame.f_code.co_filename} {frame.f_code.co_name}\n") #"-" * indent[0]
                        #f.write(str(indent[0]) + f" {frame.f_code.co_name}\n") #"-" * indent[0]
                elif event == "return":
                    """ if dir_searched[0] in self.dir:
                        print("<" + str(indent[0]), "exit function", frame.f_code.co_filename, frame.f_code.co_name)
                        f.write("<" + str(indent[0]) + f"exit function {frame.f_code.co_filename} {frame.f_code.co_name}\n") """
                    indent[0] -= 2
        
        return self.tracefunc
    
    def formatting_dataframe(self):
        
        d = FunctionsIdentifier()
        
        max = np.max(self.indent_list)
        """ print(max)
        print(self.indent_list) """
        with open(f'{self.ROOT}/output_tracefunc.txt', 'r') as f:
            for i in range(2, max+2, 2):
                temp_list = []
                line = f.readline()
                """ print(line.split(' ')[0])
                print(line) """
                while line != '':
                    if line.split(' ')[0] == str(i):
                        temp_list.append(line)
                    line = f.readline()
                self.dict_to_df[f'level {i}'] = temp_list
                f.seek(0,0)
            f.close()
        
        
        df = pd.DataFrame.from_dict(self.dict_to_df, orient='index').T
        df = df.groupby([x for x in self.dict_to_df.keys()], axis=0, as_index=False, dropna=False).count()
        
        
        """ print(self.dict_to_df['level 2'])
        print(self.dict_to_df['level 4'])
        print(self.dict_to_df['level 6']) """
        """ print('\n')        
        print()
        print('\n') """
        
        try:
            
            d.printing_formatted_dataframe(df)
        
        except:
            
            print('\nDeseja deletar o arquivo output_tracefunc?\n\n1 - Sim\n2 - Nao')
            choice = input('Opcao desejada: ')
            while choice not in ['1','2']:
                choice = input('\nOpcao errada. Digite novamente a opcao desejada: ')
            
            if choice == '1':
                os.remove(f'{self.ROOT}/output_tracefunc.txt')
                sys.exit(0)

                            



