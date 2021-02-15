import numpy as np
import math


class Circuit:
    #initialize qubits and state vector
    def __init__(self,n_qubits):
        '''This functions takes the number of qubits in the circuit and initializes all the qubits in state |0> by default and the state vector corresponding to the qubits.'''
        self.n = n_qubits
        
        self.qubits = [[1,0]]*n_qubits  
        self.state_vector = np.zeros((1,pow(2,n_qubits)))
        
        self.state_vector = self.state_vector.T
        
        self.state_vector[0][0] = 1 
        
    
    def initialize(self,list_qubits, vectors):
        '''You can use this function to initialize qubits manually. It takes in a list of qubits and their corresponding unit vectors as arguments and initializes the state vector accordingly. '''
        for i in range(len(list_qubits)):
            self.qubits[list_qubits[i]] = vectors[i]
        
        state_vector = [1]*(2**self.n)
        for i in range(2**self.n):
            binary_str = str(bin(i))
            binary_str = binary_str[2:]
            padding = self.n-len(binary_str) 
            if padding != 0:
                binary_str ='0'*padding+binary_str
            
            for j in range(len(binary_str)):
                state_vector[i] *= self.qubits[j][int(binary_str[j])]
        
        self.state_vector = np.array(([state_vector]))
        self.state_vector = self.state_vector.T
        
    def apply_single_gate(self,nth_qubit,gate):
        '''This function  takes in arguments the qubit on which you want to perform operation and the gate/type of operation you want to perform on the given qubit, and performs the matrix operation to update the state_vector.'''
        if(nth_qubit == 0):
            gate_matrix = gate
        else:
            gate_matrix = np.identity(2)
        
        for i in range(1,self.n):
            if i != nth_qubit:
                gate_matrix = np.kron(gate_matrix,np.identity(2))
            else: 
                gate_matrix = np.kron(gate_matrix,gate)
          
        self.state_vector = np.dot(gate_matrix, self.state_vector)
        
        return self.state_vector
    
    def apply_multiple_gate(self,control_list,target_list,gate):
        '''This function  takes in arguments the listof control qubits and list of target qubits on which you want to perform operation and the gate/type of operation you want to perform on the given qubit, and performs the matrix operation to update the state_vector.''' 
        self.I = np.array(([[1,0],[0,1]]))
        self.p_zero = np.array(([[1,0],[0,0]]))
        self.p_one = np.array(([[0,0],[0,1]]))
        if (0 in control_list):
            gate_matrix0 = self.p_zero
        
            gate_matrix1 = self.p_one
        elif (0 in target_list):
            gate_matrix0 = self.I
            gate_matrix1 = gate
        else: 
            gate_matrix0 = self.I
            gate_matrix1 = self.I
            
        for i in range(1,self.n):
            if i in control_list:
                gate_matrix0 = np.kron(gate_matrix0,self.p_zero)
                gate_matrix1 = np.kron(gate_matrix1,self.p_one)
            elif i in target_list:
                gate_matrix0 = np.kron(gate_matrix0,self.I)
                gate_matrix1 = np.kron(gate_matrix1,gate)
                
            else:
                gate_matrix0 = np.kron(gate_matrix0,self.I)
                gate_matrix1 = np.kron(gate_matrix1,self.I) 
                
        
        gate_matrix = gate_matrix0 + gate_matrix1
        
        self.state_vector = np.dot(gate_matrix, self.state_vector)
        
        return self.state_vector   
            
    def x(self,nth_qubit):
        '''This function performs x gate operation on given qubit by passing the given and the x gate matrix for single qubit to the apply_single_gate() function. '''
        x_gate = np.array(([[0,1],[1,0]]))
        self.apply_single_gate(nth_qubit,x_gate)
    
    def h(self, nth_qubit):
        '''This function performs h gate operation on given qubit by passing the given and the h gate matrix for single qubit to the apply_single_gate() function. '''
        h_gate = np.dot(1/math.sqrt(2),[[1,1],[1,-1]])
        self.apply_single_gate(nth_qubit,h_gate)
    
    def y(self, nth_qubit):
        '''This function performs y gate operation on given qubit by passing the given and the y gate matrix for single qubit to the apply_single_gate() function. '''
        y_gate = np.array(([[0,-1j],[1j,0]]))
        self.apply_single_gate(nth_qubit,y_gate)
    
    def z(self, nth_qubit):
        '''This function performs z gate operation on given qubit by passing the given and the z gate matrix for single qubit to the apply_single_gate() function. '''
        z_gate = np.array(([[1,0],[0,-1]]))
    
    def cz(self, control_list, target_list):
        '''This function takes in arguments as list of control qubits and list of target qubits to perform controlled z operation on the qubits by passing the given arguments and z gate for single qubit to the apply_multiuple_gate() function.'''
        if (type(control_list) is not list):
            control_list = [control_list]
        if type(target_list) is not list:
            target_list = [target_list]
            
        z_gate = np.array(([[1,0],[0,-1]]))
        self.apply_multiple_gate(control_list, target_list,z_gate)
        
    def cx(self, control_list, target_list):
        '''This function takes in arguments as list of control qubits and list of target qubits to perform controlled x operation on the qubits by passing the given arguments and x gate for single qubit to the apply_multiuple_gate() function.'''
        if (type(control_list) is not list):
            control_list = [control_list]
        if type(target_list) is not list:
            target_list = [target_list]
            
        x_gate = np.array(([[0,1],[1,0]]))
        self.apply_multiple_gate(control_list, target_list,x_gate)
    
    def measure(self, shots):
        '''This function takes argument as the number of shots and performs a weighted random choice shots number of time on the state using probalbility vector to simulate quantum measurement (not in true sense).''' 
        count = {}
        positions = []
        probability_vector = []
        
        state_vector = self.state_vector.T.tolist()[0]
        
        for i in range(len(state_vector)):
            binary_str = str(bin(i))
            binary_str = binary_str[2:]
            padding = self.n-len(binary_str) 
            if padding != 0:
                binary_str ='0'*padding+binary_str
            
            count[binary_str] = 0
            positions.append(binary_str)
            probability_vector.append(abs((state_vector[i]**2).real))
            
          
        
        collapse = np.random.choice(positions,shots,p=probability_vector)
        for i in collapse:    
            count[i] += 1
            
        return count