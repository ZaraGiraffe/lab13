from linkedbst import LinkedBST
import random

tr = LinkedBST()

'''w1 = open('words.txt', 'r')
w2 = open('words2.txt', 'w')
words = []
for line in w1:
    words.append(line.strip())
words2 = random.sample(words, 10000)
words2.sort()
for i in words2:
    w2.write(i + '\n')'''

tr.demo_bst('words2.txt')
