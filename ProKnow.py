from copy import deepcopy
from random import random,choice
class SI(object):


    def  __init__(self):

        self.epsilon = 0.0001

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
            prod *= x[i]*item[i]-Theta[i]

        return (prod)
        

    def approx(self,x,delta = False):
        
        epsilon = self.epsilon
        result = 0.0
        Theta = deepcopy(self.Theta)
        Theta = [(i + delta*epsilon) for i in Theta if delta]
        
        for item in self.Theta:
            item_prod = self.probs(item)
            item_prod *= self.dot_product(x,item,Theta)
            result += item_prod

        return (result)

    def change(self,x,order=1):

        return (self.approx(x,delta = order) - (self.approx(x)))

    def optimize(self):
        pass
            

data =  [[(0,0),0],[(0,1),1],[(1,0),1],[(1,1),0]]

data = data*10
gen_data = []

N = len(data)
for i in range(N):
    item = deepcopy(data[i])
    if random() > 0.9:
        item[1] = 1 - item[1]
        gen_data.append(item)
    else:
        gen_data.append(item)
    
o = SI()
o.calc_prob(gen_data)
print (o.probs)
