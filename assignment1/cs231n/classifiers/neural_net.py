from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from past.builtins import xrange

def softmax(z,j):
    return np.divide(np.exp(z[j]),np.sum(np.exp(z)))

class TwoLayerNet(object):
  """
  A two-layer fully-connected neural network. The net has an input dimension of
  N, a hidden layer dimension of H, and performs classification over C classes.
  We train the network with a softmax loss function and L2 regularization on the
  weight matrices. The network uses a ReLU nonlinearity after the first fully
  connected layer.

  In other words, the network has the following architecture:

  input - fully connected layer - ReLU - fully connected layer - softmax

  The outputs of the second fully-connected layer are the scores for each class.
  """

  def __init__(self, input_size, hidden_size, output_size, std=1e-4):
    """
    Initialize the model. Weights are initialized to small random values and
    biases are initialized to zero. Weights and biases are stored in the
    variable self.params, which is a dictionary with the following keys:

    W1: First layer weights; has shape (D, H)
    b1: First layer biases; has shape (H,)
    W2: Second layer weights; has shape (H, C)
    b2: Second layer biases; has shape (C,)

    Inputs:
    - input_size: The dimension D of the input data.
    - hidden_size: The number of neurons H in the hidden layer.
    - output_size: The number of classes C.
    """
    self.params = {}
    self.params['W1'] = std * np.random.randn(input_size, hidden_size)
    self.params['b1'] = np.zeros(hidden_size)
    #self.params['b1'] = std * np.random.randn(hidden_size)
    self.params['W2'] = std * np.random.randn(hidden_size, output_size)
    self.params['b2'] = np.zeros(output_size)
    #self.params['b2'] = std * np.random.randn(output_size)

  def loss(self, X, y=None, reg=0.0):
    """
    Compute the loss and gradients for a two layer fully connected neural
    network.

    Inputs:
    - X: Input data of shape (N, D). Each X[i] is a training sample.
    - y: Vector of training labels. y[i] is the label for X[i], and each y[i] is
      an integer in the range 0 <= y[i] < C. This parameter is optional; if it
      is not passed then we only return scores, and if it is passed then we
      instead return the loss and gradients.
    - reg: Regularization strength.

    Returns:
    If y is None, return a matrix scores of shape (N, C) where scores[i, c] is
    the score for class c on input X[i].

    If y is not None, instead return a tuple of:
    - loss: Loss (data loss and regularization loss) for this batch of training
      samples.
    - grads: Dictionary mapping parameter names to gradients of those parameters
      with respect to the loss function; has the same keys as self.params.
    """
    # Unpack variables from the params dictionary
    W1, b1 = self.params['W1'], self.params['b1']
    W2, b2 = self.params['W2'], self.params['b2']
    N, D = X.shape
    H = W1.shape[1] # Number of hidden units
    
    # Compute the forward pass
    scores = None
    #############################################################################
    # TODO: Perform the forward pass, computing the class scores for the input. #
    # Store the result in the scores variable, which should be an array of      #
    # shape (N, C).                                                             #
    #############################################################################
    hidden_layer = np.maximum(0,np.dot(X,W1) + b1)
    scores = np.dot(hidden_layer,W2) + b2
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################
    
    # If the targets are not given then jump out, we're done
    if y is None:
      return scores

    # Compute the loss
    loss = None
    #############################################################################
    # TODO: Finish the forward pass, and compute the loss. This should include  #
    # both the data loss and L2 regularization for W1 and W2. Store the result  #
    # in the variable loss, which should be a scalar. Use the Softmax           #
    # classifier loss.                                                          #
    #############################################################################
    #scores -= np.amax(scores, axis=1).reshape(N,1) # Normalize
    exp_scores = np.exp(scores)
    loss = -np.sum(np.log(np.divide(exp_scores[range(N),y],np.sum(exp_scores, axis=1))))
    loss /= N # Normalize
    loss += reg*(np.sum(W1*W1) + np.sum(W2*W2)) # Add contribution from regularization
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################

    # Backward pass: compute gradients
    grads = {}
    #############################################################################
    # TODO: Compute the backward pass, computing the derivatives of the weights #
    # and biases. Store the results in the grads dictionary. For example,       #
    # grads['W1'] should store the gradient on W1, and be a matrix of same size #
    #############################################################################
    
    probs = np.divide(exp_scores, np.sum(exp_scores, axis=1, keepdims=True))
    
    dscores = probs
    dscores[range(N), y] -= 1 # dL/da - Loss gradient wrt to activations on final layer
    
    dW2 = np.dot(hidden_layer.T, dscores) / N
    db2 = np.sum(dscores, axis=0) / N
    
    dW2 += reg*2.0*W2
    grads['W2'] = dW2
    grads['b2']=db2
    
    
    # First Layer
    dhidden = np.dot(dscores, W2.T)
    dhidden[hidden_layer <= 0] = 0.0 # Remove influence from ReLU units with activations <= 0
    
   
    dW1 = np.dot(X.T, dhidden) / N
    db1 = np.sum(dhidden, axis=0) / N

    dW1 += reg*2.0*W1
    grads['W1'] = dW1
    grads['b1'] = db1
    
    # Vectorized Second Layer - come back for this after writing rest of serialized
    # Scale each sample by the softmax of f
    # A = np.divide(np.exp(scores),np.sum(np.exp(scores),axis=1).reshape((N,1)))
    # Subtract off X[i] for correct class 
    # A[range(N),y] -= 1
    # dW = np.matmul(h1.T,A)
    # dW /= N
    # dW += reg*2.0*W2
    # grads['W2'] = dW
    
    # What I had before seeing the notes/working through matrix approach
    # Serial Second Layer
    # num_class = len(b2)
    # dW2 = np.zeros_like(W2)
    # db2 = np.zeros_like(b2)
    # del2 = np.zeros((N,num_class))
    # for i in xrange(N):
    #    for j in xrange(num_class):
    #        delta = softmax(scores[i,:],j) 
    #        if j == y[i]:
    #            delta-=1
    #        del2[i,j] = delta
    #         dW2[:,j] += h1[i,:]*delta
    #         db2[j]+= delta

    # Normalize, regularize and store gradients in dict
    # dW2 /= N
    # dW2 += reg*2.0*W2
    # grads['W2'] = dW2
    
    # db2 /= N
    # grads['b2']=db2
    
    # First Layer
    #dfda = np.where(hidden_layer < 0, 0, 1)
    #del1 = np.zeros((N,H))
    #for i in xrange(N):
    #    del1[i,:] = np.dot(W2,del2[i,:]) * dfda[i,:]
    #    for j in xrange(H):
    #        dW1[:,j] += X[i,:]*del1[i,j]
    #        db1[j] += del1[i,j]
        #for j in xrange(num_class):
    
    #############################################################################
    #                              END OF YOUR CODE                             #
    #############################################################################

    return loss, grads

  def train(self, X, y, X_val, y_val,
            learning_rate=1e-3, learning_rate_decay=0.95,
            reg=5e-6, num_iters=100,
            batch_size=200, verbose=False, mu=None, mu_rate = 1.03, mu_max=0.99):
    """
    Train this neural network using stochastic gradient descent.

    Inputs:
    - X: A numpy array of shape (N, D) giving training data.
    - y: A numpy array f shape (N,) giving training labels; y[i] = c means that
      X[i] has label c, where 0 <= c < C.
    - X_val: A numpy array of shape (N_val, D) giving validation data.
    - y_val: A numpy array of shape (N_val,) giving validation labels.
    - learning_rate: Scalar giving learning rate for optimization.
    - learning_rate_decay: Scalar giving factor used to decay the learning rate
      after each epoch.
    - reg: Scalar giving regularization strength.
    - num_iters: Number of steps to take when optimizing.
    - batch_size: Number of training examples to use per step.
    - verbose: boolean; if true print progress during optimization.
    """
    num_train = X.shape[0]
    iterations_per_epoch = max(num_train / batch_size, 1)
    
    # Use SGD to optimize the parameters in self.model
    loss_history = []
    train_acc_history = []
    val_acc_history = []

    vW1 = 0.0
    vW2 = 0.0
    vb1 = 0.0
    vb2 = 0.0
    
    for it in xrange(num_iters):
      X_batch = None
      y_batch = None

      #########################################################################
      # TODO: Create a random minibatch of training data and labels, storing  #
      # them in X_batch and y_batch respectively.                             #
      #########################################################################
      ibatch = np.random.choice(num_train, batch_size, replace=True)
    
      X_batch = X[ibatch]
      y_batch = y[ibatch]
      #########################################################################
      #                             END OF YOUR CODE                          #
      #########################################################################

      # Compute loss and gradients using the current minibatch
      loss, grads = self.loss(X_batch, y=y_batch, reg=reg)
      loss_history.append(loss)

      #########################################################################
      # TODO: Use the gradients in the grads dictionary to update the         #
      # parameters of the network (stored in the dictionary self.params)      #
      # using stochastic gradient descent. You'll need to use the gradients   #
      # stored in the grads dictionary defined above.                         #
      #########################################################################
      if mu is not None:
          # SGD + Nestorov Momentum
          vW1_prev = vW1
          vW2_prev = vW2
          vb1_prev = vb1
          vb2_prev = vb2
            
          vW1 = mu*vW1 - learning_rate*grads['W1']
          vW2 = mu*vW2 - learning_rate*grads['W2']
          vb1 = mu*vb1 - learning_rate*grads['b1'].reshape(self.params['b1'].shape)
          vb2 = mu*vb2 - learning_rate*grads['b2'].reshape(self.params['b2'].shape)
            
          self.params['W1'] += (1+mu)*vW1 - mu*vW1_prev
          self.params['W2'] += (1+mu)*vW2 - mu*vW2_prev
          self.params['b1'] += (1+mu)*vb1 - mu*vb1_prev
          self.params['b2'] += (1+mu)*vb2 - mu*vb2_prev
      
      else:
          # Vanilla SGD
          self.params['W1'] -= learning_rate*grads['W1']
          self.params['b1'] -= learning_rate*grads['b1']#.reshape(self.params['b1'].shape)
          self.params['W2'] -= learning_rate*grads['W2']
          self.params['b2'] -= learning_rate*grads['b2']#.reshape(self.params['b2'].shape)

      #########################################################################
      #                             END OF YOUR CODE                          #
      #########################################################################

      if verbose and it % iterations_per_epoch == 0:
        sg1 = np.sum(np.abs(grads['W1']))
        sg2 = np.sum(np.abs(grads['W2']))
        print('iteration %d / %d: loss %f sg1: %e sg2: %e' % (it, num_iters, loss, sg1, sg2))

      # Every epoch, check train and val accuracy and decay learning rate.
      if it % iterations_per_epoch == 0:
        # Check accuracy
        train_acc = (self.predict(X_batch) == y_batch).mean()
        val_acc = (self.predict(X_val) == y_val).mean()
        train_acc_history.append(train_acc)
        val_acc_history.append(val_acc)

        # Decay learning rate
        learning_rate *= learning_rate_decay
        if mu is not None:
            mu = np.minimum(mu*mu_rate, mu_max)

    return {
      'loss_history': loss_history,
      'train_acc_history': train_acc_history,
      'val_acc_history': val_acc_history,
    }

  def predict(self, X):
    """
    Use the trained weights of this two-layer network to predict labels for
    data points. For each data point we predict scores for each of the C
    classes, and assign each data point to the class with the highest score.

    Inputs:
    - X: A numpy array of shape (N, D) giving N D-dimensional data points to
      classify.

    Returns:
    - y_pred: A numpy array of shape (N,) giving predicted labels for each of
      the elements of X. For all i, y_pred[i] = c means that X[i] is predicted
      to have class c, where 0 <= c < C.
    """
    y_pred = None

    ###########################################################################
    # TODO: Implement this function; it should be VERY simple!                #
    ###########################################################################
    hidden_layer = np.maximum(0,np.dot(X,self.params['W1']) + self.params['b1'])
    scores = np.dot(hidden_layer,self.params['W2']) + self.params['b2'] 
    
    y_pred = np.argmax(scores, axis=1)
    ###########################################################################
    #                              END OF YOUR CODE                           #
    ###########################################################################

    return y_pred


