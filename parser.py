
from lexer import Token,Lexer


class Parser:
 
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = 0


    def next(self):
     
        lexer.next()


    def match(self, token):
       
        if hasattr(token, '__iter__'):
            return self.lexer.cur_tok.token in token

        
        return self.lexer.cur_tok.token == token



    def have(self, token):
    
        if self.match(token):
            self.next()
            return True
        return False
    


    def must_be(self, token, error_msg="Unexpected Token"):
     
        if self.match(token):
            self.next()
            return

        
        self.errors += 1
        error_tok = self.lexer.cur_tok
        self.next()
        print("Error: %s %s:\"%s\" at Line %d Column %d"%(error_msg, 
            error_tok.token, error_tok.lex, error_tok.line, error_tok.col))


    def parse(self):
       
        self.next()

        
        self.parse_program()

        
        return self.errors == 0


    def parse_program(self):
    #  < program >     ::= < var-declist > < fun-declist > < block >
    #                 | < fun-declist > < block >
    #                 | < block >
        self.parse_function_def()

        while not self.have(Token.EOF):
            self.parse_function_def()


    def parse_function_def(self):
        # < fun-declist > ::= < fun >
                    # | < fun-declist > < fun >
        if(self.match(Token.PROC)):
            self.parse_signature()
        self.parse_block()


    def parse_signature(self):

# < param-list >  ::= < param-decl >
                    # | < param-decl > "," < param-list >
        self.parse_type()
        
        self.must_be(Token.ID)
        self.must_be(Token.leftParenthesis)

        
        if self.have(Token.rightParenthesis):
            
            return
        self.parse_params()
        self.must_be(Token.rightParenthesis, "Mismatched Parenthesis")
            

    def parse_params(self):
    
        self.parse_decl()
        
        
        while self.have(Token.COMMA):
            self.parse_decl()


    def parse_block(self):
# < block >       ::= "BEGIN" < var-declist > < stmnt-list > "END"
                    # | "BEGIN" < stmnt-list > "END"
        if(self.match(Token.BEGIN)):
        
            self.must_be(Token.BEGIN)
        
            if self.have(Token.END):
        
                return
            self.parse_statement_list()
            self.must_be(Token.END, "Mismatched : END")
        else:
            self.parse_statement_list()         
               
            


    def parse_statement_list(self):

        self.parse_statement()

        first = ( Token.NUMBER, Token.ID, Token.intNumb, 
                 Token.floatNumb, Token.leftParenthesis, Token.WHILE, Token.IF)
        while self.match(first):
            self.parse_statement()


    def parse_statement(self):
     
        semi = False 
        if self.match(( Token.NUMBER,)):
            semi = True
            self.parse_decl()
        elif self.match(Token.WHILE):
            self.parse_while()
        elif self.match(Token.IF):
            self.parse_if()
        elif self.have(Token.ID):
            semi = True
            
            
            if self.have(Token.ASSIGN):
                
                self.parse_expr()
            elif self.have(Token.leftParenthesis):
                self.parse_call2()
            else:
                

                self.parse_expr2()
                
        else:
            semi = True
            self.parse_expr()

        
        
        


    def parse_call2(self):
 
        if self.have(Token.rightParenthesis):
            
            return
        self.parse_args()
        self.must_be(Token.rightParenthesis, "Mismatched Parenthesis")


    def parse_decl(self):
        
        self.parse_type()
        self.must_be(Token.ID)


    def parse_type(self):
        
        if self.have(Token.PROC):
            return
        self.must_be(Token.PROC, "Expected Type")
            

    def parse_args(self):
       
        self.parse_expr()
        while self.have(Token.COMMA):
            self.parse_expr()


    def parse_while(self):
      
        self.must_be(Token.WHILE)
        self.must_be(Token.leftParenthesis)
        self.parse_expr()
        self.must_be(Token.rightParenthesis, "Mismatched Parenthesis")
        self.parse_body()


    def parse_if(self):
        
        self.must_be(Token.IF)
        self.must_be(Token.leftParenthesis)
        self.parse_expr()
        self.must_be(Token.rightParenthesis)
        self.parse_body()


    def parse_body(self):
        
        if self.match(Token.leftBrace):
            self.parse_block()
        else:
            self.parse_statement()


    def parse_expr(self):
     
        self.parse_sum()
        self.parse_expr2()


    def parse_expr2(self):
       
        first = (Token.lessThan, Token.lessThanEqual, Token.greaterThan, Token.greaterThanEqual, Token.EQUAL)
        while self.match(first):
            if self.have(Token.lessThan):
                self.parse_sum()
            elif self.have(Token.lessThanEqual):
                self.parse_sum()
            elif self.have(Token.greaterThan):
                self.parse_sum()
            elif self.have(Token.greaterThanEqual):
                self.parse_sum()
            elif self.have(Token.EQUAL):
                self.parse_sum()


    def parse_sum(self):
        
        self.parse_mul()

        
        first = (Token.PLUS, Token.MINUS)
        while self.match(first):
            if self.have(Token.PLUS):
                self.parse_mul()
            elif self.have(Token.MINUS):
                self.parse_mul()


    def parse_mul(self):
       
        self.parse_value()

        
        first = (Token.TIMES, Token.DIVIDE)
        while self.match(first):
            if self.have(Token.TIMES):
                self.parse_value()
            elif self.have(Token.DIVIDE):
                self.parse_value()


    def parse_value(self):
  
        
        if self.have(Token.intNumb):
            
            return
        elif self.have(Token.floatNumb):
            
            return

        if self.have(Token.ID):
            
            if self.have(Token.leftParenthesis):
                self.parse_call2()
            return

        if self.have(Token.leftParenthesis):
            self.parse_expr()
            self.must_be(Token.rightParenthesis, "Mismatched Parenthesis")



if __name__ == '__main__':

    file = open("code.fang")    

    
    lexer = Lexer(file)
    parser = Parser(lexer)

    
    try:
        parser.parse()
        print("Code is parsed successfully")
    except:

        print("Parsing failed with %d errors."%(parser.errors))
