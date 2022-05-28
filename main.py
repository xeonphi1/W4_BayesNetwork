import numpy as np

PA= [ 0.3 , 0.3 , 0.2 , 0.2 ]
PB= [ 0.4 , 0.4 , 0.1 , 0.1 ]
PC= [ 0.2 , 0.2 , 0.3 , 0.3 ]
PS = [ [ [ 0.2 , 0.6 , 0.2 ] , [ 0.1 , 0.3 , 0.6 ] , [ 0.05 , 0.2 , 0.75 ] ,
[ 0.01 , 0.1 , 0.89 ] ] ,[ [ 0.6 , 0.3 , 0.1 ] , [ 0.2 , 0.6 , 0.2 ] , [ 0.1 , 0.3 , 0.6 ] ,[ 0.05 , 0.2 , 0.75 ] ] ,[ [ 0.75 , 0.2 , 0.05 ] , [ 0.6 , 0.3 , 0.1 ] , [ 0.2 , 0.6 , 0.2 ] ,
[ 0.1 , 0.3 , 0.6 ] ] ,[ [ 0.89 , 0.1 , 0.01 ] , [ 0.75 , 0.2 , 0.05 ] , [ 0.6 , 0.3 , 0.1 ] ,[ 0.2 , 0.6 , 0.2 ] ] ]

class ProbDist:
    """A discrete probability distribution. You name the random variable
    in the constructor, then assign and query probability of values.
    >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    >>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    >>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """

    def __init__(self, var_name='?', freq=None):
        """If freq is given, it is a dictionary of values - frequency pairs,
        then ProbDist is normalized."""
        self.prob = {}
        self.var_name = var_name
        self.values = []
        if freq:
            for (v, p) in freq.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        """Given a value, return P(value)."""
        try:
            return self.prob[val]
        except KeyError:
            return 0

    def __setitem__(self, val, p):
        """Set P(val) = p."""
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0."""
        total = sum(self.prob.values())
        if not np.isclose(total, 1.0):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='{:.3g}'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('{}: ' + numfmt).format(v, p) for (v, p) in sorted(self.prob.items())])

    def __repr__(self):
        return "P({})".format(self.var_name)




def direct_cal():
    res=[ 0 , 0 , 0 ]
    for XA in range ( 4 ):
        for XB in range ( 4 ):
            for XC in range ( 4 ):
                for sBC in range ( 3 ):
                    res[sBC] += PA[XA] *PB[XB] *PC[XC] *PS[XA][XB][0] * PS[XA][XC] [1] * PS[XB][XC][sBC]
    return res
def rejectsampling( ):
    n=5000
    nBC=[0, 0, 0]
    for i in range (n):
        XA=np.random.choice( 4 , p=PA)
        XB=np.random.choice(4 , p=PB)
        XC=np.random.choice ( 4 , p=PC)
        SAB=np.random.choice ( 3 , p=PS[XA][XB] )
        SAC=np.random.choice ( 3 , p=PS[XA][XC] )
        SBC=np.random.choice ( 3 , p=PS[XB][XC] )
        if SAB==0 and SAC==1:
            nBC[SBC]+=1
    return nBC

def Gibs ( ):
    n=4999
    nBC=[ 0 , 0 , 0 ]
    XA,XB,XC,SAB,SAC,SBC=0 ,0 ,1 ,0 ,1 ,1
    for k in range (n):
        PA=normal( [PA[ i ] *PS [ i ] [XB] [ SAB] *PS [ i ] [C] [ SAC]\
                     for i in range ( 4 ) ] )
        XA=np . random. choice ( 4 , p= PA)
        PB=normal( [PB[ i ] *PS [XA] [i] [ SAB] *PS [ i ] [XC] [ SBC]\
                     for i in range ( 4 ) ] )
        XB=np . random. choice ( 4 , p= PB)
        PC=normal( [PC[ i ] *PS [XA] [ i ] [ SAC] *PS [XB] [ i ] [ SBC]\
                     for i in range ( 4 ) ] )
        XC=np. random. choice ( 4 , p= PC)
print(ProbDist.normalize((direct_cal())))
print(ProbDist.normalize((rejectsampling())))