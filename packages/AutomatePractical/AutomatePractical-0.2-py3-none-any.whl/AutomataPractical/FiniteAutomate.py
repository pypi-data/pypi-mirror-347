from collections import defaultdict
    
class NFA:
    """
    A class representing a Nondeterministic Finite Automaton (NFA), with support
    an equivalent Dterministic Finite Automaton (DFA).

    Attributes:
        Q (set): Set of states.
        E (set): Input alphabets.
        T (dict): Transition function in the format T[state][input] = set of next states.
        q0: Start state.
        F (set): Set of final states.
        lambda_transitions (defaultdict): Computed lambda closures for each state.
    """
    def __init__(self,Q,E,T,q0,F):# the formal definiation Q: States, E: alphabet, T: transtions, q0 :start state, F:final state
        """
        Initializes the NFA with the formal definiation (Q,E,T,q0,F).

        Args:
            Q (set): States.
            E (set): Alphabets.
            T (dict): Transitions, in the form T[state][inputl] = set of next states.
            q0: Start state.
            F (set): Final states.
        """
        self.trape_state='⌀'
        self.Q=Q
        self.E=E
        self.T=T#should be dictionary and the key is the state and the value is the dictionary key:input value:list of state when consume the input 
        self.q0=q0
        self.F=F
        self.lambda_transitions=defaultdict(set)
        self.lambda_transition_symbol="ε"

    def __str__(self):
        """
        Returns a string representation of the NFA.
        
        Returns:
            str: String representation of the NFA with states, alphabet, 
                start state, final states, and transitions.
        """
        result = []
        
        # Format states
        result.append("States:")
        for state in self.Q:
            state_repr = set(state) if isinstance(state, frozenset) else state
            result.append(f"  {state_repr}")
        
        # Format alphabet
        result.append("\nAlphabet:")
        alphabet_repr = set(self.E) if isinstance(self.E, frozenset) else self.E
        result.append(f"  {alphabet_repr}")
        
        # Format start state
        result.append("\nStart State:")
        start_state_repr = set(self.q0) if isinstance(self.q0, frozenset) else self.q0
        result.append(f"  {start_state_repr}")
        
        # Format final states
        result.append("\nFinal States:")
        for state in self.F:
            state_repr = set(state) if isinstance(state, frozenset) else state
            result.append(f"  {state_repr}")
        
        # Format transitions
        result.append("\nTransitions:")
        for from_state, transitions in self.T.items():
            from_state_repr = set(from_state) if isinstance(from_state, frozenset) else from_state
            for symbol, to_states in transitions.items():
                to_states_repr = set(to_states) if isinstance(to_states, frozenset) else to_states
                result.append(f"  δ({from_state_repr}, '{symbol}') => {to_states_repr}")
        
        # Join all parts and return as a single string
        return "\n".join(result)
                
    def _depth_first_search(self,from_,processing_state):
        """
        Perform DFS(Depth-First-Search) to compute the lambda closure of specific state.

        Args:
            from_ (str): The current state of being visited.
            processing_state (str): The original state that we compure the lambda closure for it.
        """
        if from_ == processing_state:#just when we start we need to add the current state
            self.lambda_transitions[processing_state].add(processing_state)

        #this only executed when there is an empty transision 
        for to in self.T[from_][self.lambda_transition_symbol]:
            if self.lambda_transitions[processing_state].__contains__(to) is False:                
                #before we go to the {To} state we can check if it exist in the lambdaTransisitions if yes no need to compute just union
                target=self.lambda_transitions[to]
                if len(target) > 0:# To is previously  calculated we no need calculte it again just update the transing of processingState
                    self.lambda_transitions[processing_state].update(target)
                    continue

                self.lambda_transitions[processing_state].add(to)
                self._depth_first_search(to,processing_state)
    
    def _compute_all_lambda_closures(self):
        '''
        Compute the lambda closure of all states.
        '''
        #this is called when there is an empty transtion and not 
        for state in self.Q:
            self._depth_first_search(state, state)

    def DFA_equivalence(self):
        """
        Converts the NFA (that has lambda transitions or not) into equivalent DFA using subset construction method.

        Returns:
            NFA: new NFA represent the equivalent DFA.
        """
        self._compute_all_lambda_closures()
        #we use the frozenset because we want use it as key so it must be hashable because in conversion nfa to dfa the state itself can my more than on symbol
        initial_state=frozenset(self.lambda_transitions[self.q0])
        dfa_states = {initial_state}#our states in the dfa maynot be just a single symbol it can be more one
        unprocessed_dfa_states=[initial_state]
        dfa_transitions = {}
        dfa_final_states= set()
     

        while len(unprocessed_dfa_states) > 0: #for each unprocessed state
            current_dfa_states = unprocessed_dfa_states.pop(0)

            for nfa_final_state in self.F:#this loop just for check if the dfa state is final state or not
                if current_dfa_states.__contains__(nfa_final_state) is True:
                    dfa_final_states.add(current_dfa_states)
                    break
            
            dfa_transitions[current_dfa_states]= {}#the key itself might be a list so we use frozenset

            for input in self.E:#a,b
                if input == self.lambda_transition_symbol:
                    continue
                next_dfa_states=set()
                for state in current_dfa_states: 
                    nfa_to_states=self.T[state][input]#{NFA(q1,a)={q1,q2} in next iter NFA(q1,b)}
                    for nfa_state in nfa_to_states:#q1 , q2
                        next_dfa_states.update(self.lambda_transitions[nfa_state])
                
                if len(next_dfa_states) == 0:#not exist transistion for this input
                        next_dfa_states.add(self.trape_state)#trap state

                next_states_frozen = frozenset(next_dfa_states)#just for hashing
                dfa_transitions[current_dfa_states][input]=next_states_frozen

                if dfa_states.__contains__(next_states_frozen) == False:#this state is new and not processed before add it!
                    dfa_states.add(next_states_frozen)
                    unprocessed_dfa_states.append(next_states_frozen)

        #just add self loop for trap state if exist
        trap_state=frozenset([self.trape_state])
        if dfa_states.__contains__(trap_state):
            for input in self.E:
                if input == self.lambda_transition_symbol:
                    continue
                dfa_transitions[trap_state][input]=trap_state
                

        return NFA(dfa_states, self.E - {self.lambda_transition_symbol} , dfa_transitions, initial_state, dfa_final_states)










