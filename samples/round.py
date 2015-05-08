import storage
import random

for i in range(0, 10000):

	if ( random.random() > 0.95 ):
		# print "\n"
		# print storage.read()
		# print storage.read()
		# print storage.read()
		storage.initialize()

	storage.write(">>> a b c d e f g h i j k l m n o p q r s t u v w x y z (%s)" % i)

#print "\n"
#print storage.read()

storage.end()
