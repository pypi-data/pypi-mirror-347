from collections import defaultdict
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from AutomataPractical import NFA

class NFA_WithLambdaClosureTests(unittest.TestCase):

    def setUp(self):#this function is called automatically before each test function
        T=defaultdict(lambda: defaultdict(set))
        T['0']['a'].add('1')
        T['0']['a'].add('2')
        T['0']['ε'].add('3')
        T['1']['b'].add('3')
        T['2']['ε'].add('3')
        T['3']['ε'].add('1')
        self.nfa=NFA(Q={'0','1','2','3'},E={'a','b'},T=T,q0='0',F='3')
        self.trape_state=self.nfa.trape_state

    def test_compute_all_lambda_closures(self):
        expected_lambda_closures={
            '0':{'0','3','1'},
            '1':{'1'},
            '2':{'2','3','1'},
            '3':{'3','1'}
        }
        self.nfa._compute_all_lambda_closures()
        actual_lambda_closures=self.nfa.lambda_transitions
        self.assertDictEqual(expected_lambda_closures,actual_lambda_closures)

    def test_dfa_states(self):
        expected_dfa_states={
            frozenset({'0','1','3'}),
            frozenset({'1','2','3'}),
            frozenset({'1','3'}),
            frozenset({self.trape_state})
        }
        
        actual_dfa_states = self.nfa.DFA_equivalence().Q

        self.assertSetEqual(expected_dfa_states,actual_dfa_states)

    def test_dfa_final_sates(self):
        expected_dfa_final_states = { 
            frozenset({'0','1','3'}),
            frozenset({'1','3'}),
            frozenset({'1','2','3'})
            }
        
        actual_dfa_fina_states=self.nfa.DFA_equivalence().F

        self.assertSetEqual(actual_dfa_fina_states,expected_dfa_final_states)
    
    def test_dfa_start_state(self):
        expected_dfa_start_state = frozenset({'0','1','3'})

        actual_dfa_start_state=self.nfa.DFA_equivalence().q0

        self.assertSetEqual(expected_dfa_start_state,actual_dfa_start_state)
    
    def test_dfa_equivalence(self):
        expected_dfa = {
            frozenset({'0', '1', '3'}): {
                'a': frozenset({'1', '2', '3'}),
                'b': frozenset({'1', '3'}),
            },
            frozenset({'1', '2', '3'}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({'1', '3'})
            },
            frozenset({'1', '3'}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({'1', '3'})
            },
            frozenset({self.trape_state}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({self.trape_state})
            }
        }  
        actual_dfa=self.nfa.DFA_equivalence().T

        self.assertDictEqual(expected_dfa,actual_dfa)
       


    
 




class NFA_WithoutLambdaClosureTests(unittest.TestCase):

    def setUp(self):#this function is called automatically before each test function
        T=defaultdict(lambda: defaultdict(set))

        T['1']['a'].add('1')
        T['1']['a'].add('2')
        T['1']['a'].add('3')
        T['1']['a'].add('4')
        T['1']['a'].add('5')
        T['1']['b'].add('4')
        T['1']['b'].add('5')


        T['2']['a'].add('3')
        T['2']['b'].add('5')

        T['3']['b'].add('2')

        T['4']['a'].add('5')
        T['4']['b'].add('4')
       


        self.nfa=NFA(Q={'1','2','3','4','5'},E={'a','b'},T=T,q0='1',F='5')
        self.trape_state=self.nfa.trape_state

    def test_compute_all_lambda_closures(self):
        expected_lambda_closures={
            '1':{'1'},
            '2':{'2'},
            '3':{'3'},
            '4':{'4'},
            '5':{'5'},
        }
        self.nfa._compute_all_lambda_closures()
        actual_lambda_closures=self.nfa.lambda_transitions
        self.assertDictEqual(expected_lambda_closures,actual_lambda_closures)

    def test_dfa_states(self):
        expected_dfa_states={
            frozenset({'1', '2', '3', '4', '5'}),
            frozenset({'4', '5'}),
            frozenset({'3', '5'}),
            frozenset({'2', '4', '5'}),
            frozenset({self.nfa.trape_state}),
            frozenset({'1'}),
            frozenset({'2'}),
            frozenset({'3'}),
            frozenset({'4'}),
            frozenset({'5'}),

        }
        
        actual_dfa_states = self.nfa.DFA_equivalence().Q

        self.assertSetEqual(expected_dfa_states,actual_dfa_states)

    def test_dfa_final_sates(self):
        expected_dfa_final_states = { 
            frozenset({'1','2','3','4','5'}),
            frozenset({'2','4','5'}),
            frozenset({'3','5'}),
            frozenset({'4','5'}),
            frozenset({'5'}),

            }
        
        actual_dfa_fina_states=self.nfa.DFA_equivalence().F

        self.assertSetEqual(actual_dfa_fina_states,expected_dfa_final_states)

    def test_dfa_equivalence(self):
        expected_dfa = {
            frozenset({'1'}): {
                'a': frozenset({'1', '2', '3', '4', '5'}),
                'b': frozenset({'4', '5'}),
            },
            frozenset({'1', '2', '3', '4', '5'}): {
                'a': frozenset({'1', '2', '3', '4', '5'}),
                'b': frozenset({'2', '4', '5'})
            },
            frozenset({'4', '5'}): {
                'a': frozenset({'5'}),
                'b': frozenset({'4'})
            },
            frozenset({'5'}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({self.trape_state})
            },
            frozenset({'4'}): {
                'a': frozenset({'5'}),
                'b': frozenset({'4'})
            },
            frozenset({'2', '4', '5'}): {
                'a': frozenset({'3', '5'}),
                'b': frozenset({'4', '5'})
            },
            frozenset({'3', '5'}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({'2'})
            },
            frozenset({self.trape_state}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({self.trape_state})
            },
            frozenset({'2'}): {
                'a': frozenset({'3'}),
                'b': frozenset({'5'})
            },
            frozenset({'3'}): {
                'a': frozenset({self.trape_state}),
                'b': frozenset({'2'})
            },}       
        
        actual_dfa=self.nfa.DFA_equivalence().T
        self.assertDictEqual(expected_dfa,actual_dfa)
       
    def test_dfa_start_state(self):
        expected_dfa_start_state = frozenset({'1'})

        actual_dfa_start_state=self.nfa.DFA_equivalence().q0

        self.assertSetEqual(expected_dfa_start_state,actual_dfa_start_state)
    

      
    



if __name__ == '__main__':
    unittest.main()