class InstructionDecoder:
    def __init__(self):
        self.variables = {'Y': 1}
        self.c = self.variables.copy()

        for i in range(1, 20): 
            self.c[f'X{i}'] = 2 * i
            self.c[f'Z{i}'] = 2 * i + 1


        self.labels = {}
        self.a = self.labels.copy()
        label_index = 1

        for i in range(1, 10):
            for j in ['A', 'B', 'C', 'D', 'E']:
                self.a[f'{j}{i}'] = label_index
                label_index += 1

    def decode_instruction(self, encoded_dict):
        reverse_a = {v: k for k, v in self.a.items()}
        reverse_c = {v: k for k, v in self.c.items()}

        label = reverse_a.get(encoded_dict['a'], ' ')
        variable = reverse_c.get(encoded_dict['c']+1, 'unknown')  
        operation = ''
        if encoded_dict['b'] == 0:
            operation = f'{variable} <- {variable}'
        elif encoded_dict['b'] == 1:
            operation = f'{variable} <- {variable}+1'
        elif encoded_dict['b'] == 2:
            operation = f'{variable} <- {variable}-1'
        
        else:
            label_var = reverse_a.get(encoded_dict['b'] - 2) 
            operation = f'if {variable} != 0 go to {label_var}'

        return f'[{label}] {operation}'

    def decode_instruction_reverse(self, decode_instruction_str):
        decode_dict = {'a': 0, 'b': 0, 'c': 0}

        if 'if' in decode_instruction_str:
            for label, idx in self.a.items():
                if label in decode_instruction_str[16:]:
                    decode_dict['b'] = idx+2
                    break
            # variable
            for var, idx in self.c.items():
                if var in decode_instruction_str:
                    decode_dict['c'] = idx -1
                    break
            # label
            for label, idx in self.a.items():
                if label in decode_instruction_str[0:3]:
                    decode_dict['a'] = idx
                    break
        else:
            if '+1' in decode_instruction_str:
                decode_dict['b'] = 1
            elif '-1' in decode_instruction_str:
                decode_dict['b'] = 2
            else:
                decode_dict['b'] = 0

            # variable
            for var, idx in self.c.items():
                if var in decode_instruction_str:
                    decode_dict['c'] = idx -1
                    break
            # label
            for label, idx in self.a.items():
                if label in decode_instruction_str:
                    decode_dict['a'] = idx
                    break

        return decode_dict