import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf

'''
print(tf.__version__)
print("HELLO DOES THIS WORK")
'''

# Initialization of tensors
x = tf.constant(4, shape=(1,1), dtype=tf.float32) # 4 is a scalar (1x1 matrix)
y = tf.constant([[1,2,3], [4,5,6]]) # 2x3 matrix
print(x)
print(y)

z = tf.ones((3,3)) # 3x3 matrix of ones
print(z)

a = tf.eye(3) # I for the intgedity matrix (eye LOL)
print(a)

b = tf.random.normal((3,3), mean=0, stddev=1) # 3x3 matrix of random numbers
print(b)

c = tf.random.uniform((1,3), minval=0, maxval=1) # 1x3 matrix of random numbers
print(c)

d = tf.range(start=1, limit=10, delta=2) # 1, 3, 5, 7, 9
print(d)

d = tf.cast(d, dtype=tf.float64) # Casts x to a float64
print(d) # Other options: tf.float(16,32,64), tf.int(8,16,32,64), tf.bool



# Mathematical operations
x = tf.constant([1,2,3])
y = tf.constant([9,8,7])

z = tf.add(x,y) # Element-wise addition
z = x + y # Also element-wise addition, most likely the better option
print(z)

z = tf.subtract(x,y) # Element-wise subtraction
z = x - y # Also element-wise subtraction, most likely the better option
print(z)

z = tf.divide(x,y) # Element-wise division
z = x / y # Also element-wise division, most likely the better option
print(z)

z = tf.multiply(x,y) # Element-wise multiplication
z = x * y # Also element-wise multiplication, most likely the better option
print(z)

z = tf.tensordot(x, y, axes=1) # Dot product
print(z)

# Indexing
