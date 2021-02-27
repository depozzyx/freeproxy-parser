class Menu:
    def __init__(self, question, yes_text = None, no_text = None, listens_cusom_user_input = False, input_check_function = None):
        self.question = question
        self.yes_text = yes_text
        self.no_text = no_text
        self.listens_cusom_user_input = False
        self.res = None

        self.generate_header()
        
        input_correct = False
        while not input_correct:
            inp = self.get_input()
            if inp.lower() in ['q', 'quit']:
                quit()
            
            if input_check_function != None:
                try:
                    checked = input_check_function(inp)
                    if checked:
                        if listens_cusom_user_input:
                            self.res = inp
                        else:
                            self.res = 1
                        input_correct = True
                    else:
                        self.throw_input_err()
                except Exception as e:
                    print(' !',e)
                    self.throw_input_err()

            else:
                
                if inp.lower() in ['y', 'yes']:
                    if yes_text != None:
                        self.res = 1
                        input_correct = True
                    else:
                        self.throw_input_err()
                elif inp.lower() in ['n', 'no']:
                    if no_text != None:
                        self.res = 0
                        input_correct = True
                    else:
                        self.throw_input_err()
                else:
                    if listens_cusom_user_input != False:
                        self.res = inp
                        input_correct = True
                    else:
                        self.throw_input_err()

    def throw_input_err(self):
        print(' ! Ваш ввод кривой')     

    def generate_header(self):
        print('\n'+self.question)
        if self.yes_text:
            print(f' Y : {self.yes_text}')
        if self.no_text:
            print(f' N : {self.no_text}') 
        print(' Q : Выход')

    def get_input(self):
        print(' > ', end = '')
        return input()

