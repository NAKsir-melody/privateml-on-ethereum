#!/usr/bin/env python

import argparse
import numpy as np
from numpy import array
import os
import tensorflow as tf
from tensorflow.python.platform import gfile
import scipy
from scipy import misc


with tf.Graph().as_default() as graph: # Set default graph as graph
    with tf.Session() as sess:
                f = open("/home/naksir/WORK/cryptonian/ML/MNIST/input.txt")
                line = f.readline()
                fpath = "/home/naksir/WORK/cryptonian/ML/MNIST/" + line.strip()
                image = scipy.misc.imread(fpath)
                image = image.astype(float)
                #scipy.misc.imshow(image)
                img_data = array(image).reshape(1, 784)
               # print image
                '''

                img_data = [line.strip() for line in open("/home/naksir/WORK/cryptonian/ML/MNIST/input.txt", 'r')]
                '''
                image = np.reshape(img_data,(1, 784))
                saver = tf.train.import_meta_graph('/home/naksir/WORK/cryptonian/ML/MNIST/sigmoid.meta')

                l_output=graph.get_tensor_by_name("Softmax:0")
                l_input=graph.get_tensor_by_name("Placeholder:0")

                print "Shape of input : ", tf.shape(l_input)
                tf.train.Saver().restore(sess, '/home/naksir/WORK/cryptonian/ML/MNIST/sigmoid')
                pred_prob = sess.run( l_output, feed_dict = {l_input : image} )
                probabilities = pred_prob[0, 0:]

                with open("/home/naksir/WORK/cryptonian/ML/MNIST/labels.txt") as f:
                    names = f.read().splitlines()

                sorted_inds = [i[0] for i in sorted(enumerate(-probabilities), key=lambda x:x[1])]

                for i in range(1):
                    index = sorted_inds[i]
                    print('Probability %0.2f%% => [%s]' % (probabilities[index]*100, names[index]))

