from collections import defaultdict

class Transition:
    """
    Represents transition in the Turing machine.

    Attributes:
        write_symbol (str): The symbol to write on the tape.
        direction (str): The direction to move the head ('L' : left, 'R' : right).
        next_state (str): The next state after this transition.
    """
    def __init__(self,write_symbol,direction,next_state):
        self.write_symbol=write_symbol
        self.direction=direction
        self.next_state=next_state

class TuringMachine:
    """
    Simulates a simple Turing machine that performs unary addition.
    """
    def __init__(self,input):
        """
        Initializes the tape with given input.

        Args:
            input (str): The initial tape content.
        """
        self.tape=list(input)

    def _construct_addition_turning_machine(self):
        """
        Constructs the Turing machine that performs unary addition.
        """
        start_state='q0'
        accept_state = 'q3'
        blank_symbol = 'B'
        self.start_state=start_state
        self.accept_state=accept_state
        self.blank_symbol=blank_symbol

        #we construct the turning machine

        self.transistions=defaultdict(dict)
        #we need simulate a + b
        #finish the first input(a)
        self.transistions[start_state]['1']=Transition('1','R',start_state)
        #if we found the + remove it and replace it with 1 and move right
        self.transistions[start_state]['+']=Transition('1','R','q1')
        #finish the second input(b)
        self.transistions['q1']['1']=Transition('1','R','q1')
        #if we found the blank then we reached the end of the tape then back left
        self.transistions['q1'][blank_symbol]=Transition(blank_symbol,'L','q2')
        #override the current cell with the blank symbol because we replaced the + with 1 so there is an extra 1 so we need remove it
        self.transistions['q2']['1']=Transition(blank_symbol,'L',accept_state)

    def addition(self):
        """
        Run the Turing machine to compute the unary addition.

        Returns:
            str: result of the addition in unary representation.
        """
        self._construct_addition_turning_machine()
        processing_state=self.start_state
        head=0
        while processing_state != self.accept_state:

            #just extend the tape when head passed the  boundries
            if head < 0:
                self.tape.insert(0, self.blank_symbol)
                head = 0
            if head >= len(self.tape):
                self.tape.append(self.blank_symbol)

            read=self.tape[head]#read the input that the tape pointing to

            if self.transistions[processing_state].__contains__(read) is False:#
                #we reject when the readed symbol not in the transistions[processing_state]
                return ""

            transition=self.transistions[processing_state][read]
            self.tape[head]=transition.write_symbol#write the symbol to the cell that is the head pointing to
            if transition.direction == 'R':
                head+=1
            else:
                head-=1
            processing_state=transition.next_state
        return ''.join(self.tape).strip(self.blank_symbol)
