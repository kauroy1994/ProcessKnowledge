import spacy
import numpy
import numpy as np
nlp = spacy.load('en_core_web_md')
#doc = nlp(word) #inference, no retraining
        
class FineTune(object):

    def __init__(self,alpha,data):

        self.alpha = alpha
        self.data = data
        self.L = self.init_matrix()

    def init_matrix(self):

        return (np.array([[0.0 for i in range(300)] for j in range(300)]))

    def objective(self,L=None):

        result = -self.alpha
        for item in self.data:
            x0,x1 = np.array(nlp(item[0]).vector), np.array(nlp(item[1]).vector)
            if item[-1] == 1:
                result += (L@x0/float(np.linalg.norm(L@x0)+0.0001)) @ (L@x1/float(np.linalg.norm(L@x1)+0.0001))
            else:
                result -= (L@x0/float(np.linalg.norm(L@x0)+0.0001)) @ (L@x1/float(np.linalg.norm(L@x1)+0.0001))

        return result

o = FineTune(0.5,[['hello','hello',1]])
r = o.objective(L=o.L)
        
