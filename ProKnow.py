from copy import deepcopy
from random import random,choice
from math import log

class SI(object):


    def  __init__(self):

        self.epsilon = 0.0001
        self.gamma = 5.0

        self.probs = {(0,0):0.0,
                      (0,1):0.0,
                      (1,0):0.0,
                      (1,1):0.0}

        self.Theta = [0.0,0.0]

        self.encoding = {(0,0): [['Q1',False],['Q2',False]],
                         (0,1): [['Q1',False],['Q2',True]],
                         (1,0): [['Q1',True],['Q2',False]],
                         (1,1): [['Q1',True],['Q2',True]]}

    def calc_prob(self,data):

        for item in self.probs:
            den = len([x for x in data if x[0] == item])
            num = len([x for x in data if ((x[0] == item) and (x[1] == 1))])
            self.probs[item] = num/float(den)

    def dot_product(self,x,item,Theta):

        prod = 1
        lfeatures = len(x)
        for i in range(lfeatures):
            prod *= (((x[i]+0.001)/float(x[i]+0.001))*((item[i]+0.001)/float(item[i]+0.001)))-Theta[i]

        return (prod)

    def objective(self,data):

        total = 0.0
        for data_point in data:
            y = data_point[1]
            x = data_point[0]
            
            p = 0.0
            
            for item in self.encoding:
                item_prod = self.probs[item]
                item_prod *= self.dot_product(x,item,self.Theta)
                p += item_prod

            if (y):
                total += -log(max(0,p)+0.0001) #log domain error corrections
            
            else:
                total += -log(max(0,1-p)+0.0001) #log domain error corrections

        return (total)

    def approx(self,x,theta_index,delta = False):
        
        epsilon = self.epsilon
        result = 0.0
        Theta = deepcopy(self.Theta)

        if delta == 1: #f(theta + epsilon)
            ntheta = len(Theta)
            for i in range(ntheta):
                if (i == theta_index):
                    Theta[i] += epsilon
            for item in self.encoding:
                item_prod = self.probs[item]
                item_prod *= self.dot_product(x,item,Theta)
                result += item_prod

        elif delta == 2: #f(theta + epsilon) + f(theta - epsilon)

            ntheta = len(Theta)
            for i in range(ntheta):
                if (i == theta_index):
                    Theta[i] += epsilon
            for item in self.encoding:
                item_prod = self.probs[item]
                item_prod *= self.dot_product(x,item,Theta)
                result += item_prod

            ntheta = len(Theta)
            for i in range(ntheta):
                if (i == theta_index):
                    Theta[i] -= 2*epsilon
            for item in self.encoding:
                item_prod = self.probs[item]
                item_prod *= self.dot_product(x,item,Theta)
                result += item_prod
        

        return (result)

    def objective_change(self,data_point,theta_index,order=1):

        delta_objective,objective = None,None
        y = data_point[1]
        x = data_point[0]

        if (y):
            delta_loss = -log(max(0,(self.approx(x,theta_index,delta = order)))+0.0001)
            loss = -log(max(0,(self.approx(x,theta_index)))+0.0001) #log domain error corrections
            
        else:
            delta_loss = -log(max(0,(1 - self.approx(x,theta_index,delta = order)))+0.0001)
            loss = -log(max(0,(1 - self.approx(x,theta_index)))+0.0001) #log domain error corrections

        return ((delta_loss - order*loss)+(1*int(order==2)))/float(self.epsilon**order)

    def optimize(self,data):

        c = 1
        while (True):
            if self.objective(data) <= 0.01:
                break
            ntheta = len(self.Theta)
            #print ("Objective before", self.objective(data))  
            #print ("before optim step",self.Theta)
            for j in range(ntheta):
                total_change = 0.0
                for data_point in data:
                    change = -self.objective_change(data_point,j,order=1)/float(self.objective_change(data_point,j,order=2))
                    total_change += change
                self.Theta[j] += self.gamma*total_change
            print ("Objective after ", c, self.objective(data))
            print ("after optim step",self.Theta)
            c += 1
    
#========================TESTER CODE===============================
data =  [[(0,0),0],[(0,1),1],[(1,0),1],[(1,1),0]]

data = data*100
gen_data = []

N = len(data)
for i in range(N):
    item = deepcopy(data[i])
    if random() > 1.0:
        item[1] = 1 - item[1]
        gen_data.append(item)
    else:
        gen_data.append(item)
    
o = SI()
o.calc_prob(gen_data)
o.optimize(gen_data)
#print (o.probs)
