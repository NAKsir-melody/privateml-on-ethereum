import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf

# input data
x = tf.placeholder(tf.float32, [None, 784]) #any number of row is good
x_image = tf.reshape(x, [-1,28,28,1])
w_conv1 = tf.Variable(tf.truncated_normal([5,5,1,16], stddev=0.1))
b_conv1 = tf.Variable(tf.constant(0.1, shape=[16]))

conv2d = tf.nn.conv2d(x_image, w_conv1, strides=[1,1,1,1], padding = 'SAME')
relu= tf.nn.relu(conv2d+b_conv1)
pool = tf.nn.max_pool(relu, ksize=[1,4,4,1], strides = [1,4,4,1], padding = 'SAME')

pool_vec = tf.reshape(pool, [-1, 7*7*16])

#w = tf.Variable(tf.zeros([784, 10]))
w = tf.Variable(tf.zeros([7*7*16, 10]))
b = tf.Variable(tf.zeros([10]))
#y = tf.nn.softmax(tf.matmul(x,w) + b)
y = tf.nn.softmax(tf.matmul(pool_vec,w) + b)
# output
y_target= tf.placeholder(tf.float32, [None, 10])

#set training option
#error function = diff of y and y_ cross_entropy
#optimize method is GD with error minimize
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_target * tf.log(y), reduction_indices=[1]))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_target: batch_ys})

#result report
prediction = tf.equal( tf.argmax(y,1), tf.argmax(y_target,1) )
accuracy = tf.reduce_mean(tf.cast(prediction, tf.float32))

print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_target: mnist.test.labels}))

saver = tf.train.Saver()
save_path = saver.save(sess,"./sigmoid")


