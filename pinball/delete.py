



class tree:
    def __init__(self, val):
        self.left = False
        self.right = False
        self.val = val


root = tree(0)
root.left = tree(1)
root.right = tree(2)
root.left.left = tree(3)
root.left.right = tree(4)
root.left.left.right = tree(5)


def printTree(r, his):
    print(his, r.val)
    if r.left != False:
        #hisl = his
        #hisl.append("left")
        printTree(r.left, his)
    if r.right !=  False:
        #hisr = his
        #hisr.append("right")
        printTree(r.right, his)
    

printTree(root, [])