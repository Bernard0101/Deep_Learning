from perceptron import Perceptron, TrainPerceptron
import numpy as np
import pandas as pd

#the dataset and it`s preprocessing
data = pd.read_csv('dataset.csv')
features = data[['Age', 'Education']].values
labels = data['Salary'].values

#perceptron objects 
p=Perceptron(learning_rate=00.1, n_features=features.shape[1])

#perceptron training objects
pt=TrainPerceptron(model=p, features=features, labels=labels)

#the derivative of leaky ReLU
def activation_leaky_ReLU_derivative(Z, alpha=0.01):
    #print(f"Z: {Z}")
    return alpha if Z.all() < 0 else 1

#Leaky ReLU
def activation_leaky_ReLU(z, alpha=0.01):
    return np.where(z >= 0, z, alpha * z)

#the derivative of mse loss
def MSE_Loss_derivative(y_pred, y_label):
   # print(f"\n\npred: {y_pred}, label:{y_label[0]}")
    return y_pred-y_label[0]

#mse Loss
def MSE_Loss(losses, mse_error=0):
    if np.ndim(losses)!=0:
        mse_error=np.mean(losses ** 2)
    else:
        mse_error=losses
    return mse_error

class MultilayerPerceptron():
    def __init__(self, n_features=len(features), input_nodes=2, hidden_layers=5, hidden_nodes=[3]):
        self.hidden_layers=hidden_layers
        self.input_nodes=input_nodes
        self.hidden_nodes=hidden_nodes
        self.input_weights=np.random.randn(n_features, input_nodes)
        self.hidden_weights=np.array([np.random.randn(hidden_nodes[i], hidden_nodes[i-1])for i in range(1, len(hidden_nodes))], dtype=object)
        #self.biases=[np.random.randn(hidden_nodes) for j in range(hidden_layers)] + [np.random.rand(1)]
        

    #input node, that returns a list of predictions with the size of input nodes
    def input_layer(self, input_nodes=1):
        out_features=[]
        for i in range(input_nodes):
            predictions=pt.predict()
            out_features.append(predictions)
        #print(f"input weights: \n{out_features}")
        return out_features
            

    #hidden layer, that returns a list of the new predictions with the size of hidden nodes
    def hidden_layer(self, predictions, hidden_nodes=3, layer=0):
        out_hidden_features=[]
        node_weights=self.hidden_weights[layer-1]
        for node in range(self.hidden_nodes[layer]):
            weights=node_weights[node]
            Z=0
            #print(f"\nlayer:{layer}\nnode:{node}\npredictions: \n{predictions},\nweights: \n{weights}")
            Z=np.dot(predictions, weights)
            #Z+=self.biases[-1]
            out_hidden_features.append(Z)
        out_hidden_features=np.squeeze(out_hidden_features)
        #print(f"out_features{out_hidden_features}")
        return out_hidden_features


    

    #the activation layer of the neural network
    def activation_layer(self, out_hidden_features):
        p=[]
        #print(f"\n\nactivation weights: {out_hidden_features}")
        if np.ndim(out_hidden_features)!=0:
            for preds in out_hidden_features:
                p.append(activation_leaky_ReLU(preds))
                predictions=np.squeeze(p)
        else:
            predictions=activation_leaky_ReLU(out_hidden_features)
        #print(f"\n\nactivation predizzioni:{predictions}\n\n")
        return predictions
    

    #the calculation of the mse loss 
    def Calculate_Loss(self, predictions, errors=[], mse_Loss=0):
        if np.ndim(predictions)!=0:
            for label, pred in zip(labels, predictions):
                error=pred-label
                errors.append(error)
            mse_Loss=MSE_Loss(losses=errors)
        else:
            error=predictions-labels[2]
            mse_Loss=MSE_Loss(losses=error)
        return mse_Loss


    def Forward(self):
        #the initial input layer 
        #print("starting forward pass")
        in_features=nn.input_layer(input_nodes=self.input_nodes)

        #all the hidden layers and also its activation functions
        in_features=nn.hidden_layer(predictions=in_features, hidden_nodes=3, layer=1)
        in_features=nn.activation_layer(out_hidden_features=in_features)
        in_features=nn.hidden_layer(predictions=in_features, hidden_nodes=9, layer=2)
        in_features=nn.activation_layer(out_hidden_features=in_features)
        in_features=nn.hidden_layer(predictions=in_features, hidden_nodes=3, layer=3)
        in_features=nn.activation_layer(out_hidden_features=in_features)
        out_features=nn.hidden_layer(predictions=in_features, hidden_nodes=1, layer=4)
       # in_features=nn.activation_layer(out_hidden_features=in_features)
        #out_features=nn.hidden_layer(predictions=in_features, hidden_nodes=3, layer=3)

        #the final prediction
        #print(f"\n\n\nthe final preds ff{out_features}")
        return out_features


    #the backpropagation algorithm and its gradient descent calcculation
    def Backpropagation(self, predictions, learning_rate):
        #print("iniziando l`algritmo de backpropagation\n\n\n")
        for hidden_layer in range(self.hidden_layers, 0, -1):
            #print(f"_____________________________\nlayer: {hidden_layer+1}\n")
            for idx_node, node in enumerate(self.hidden_weights[hidden_layer]):
                #print(f"node: {idx_node+1}\n\n")
                for idx_weight, weight in enumerate(node):
                    derivata_perdita=MSE_Loss_derivative(y_pred=weight, y_label=labels)
                    derivata_ativazzione=activation_leaky_ReLU_derivative(Z=weight)
                    gradiente_errori=derivata_perdita*derivata_ativazzione
                    #print(weight)
                    #print(f"gradiente discendente: {gradiente_errori}\n\n\n")
                    new_weight=weight-learning_rate*gradiente_errori
                    self.hidden_weights[hidden_layer][idx_node][idx_weight]=new_weight
        #print(self.hidden_weights)
        return self.hidden_weights
                                
                    


            


        






nn=MultilayerPerceptron(input_nodes=2, hidden_nodes=[2, 3, 9, 3, 1], hidden_layers=3)
#print(f"hidden_nodes: \n\n {nn.hidden_nodes}\n\n")
#print(f"input weights: \n\n {nn.input_weights}\n shape: {nn.input_weights.shape}\n type: {type(nn.input_weights)}\n\n")
#print(f"hidden_weights: \n\n {nn.hidden_weights}\n shape: {nn.hidden_weights.shape}\n type: {type(nn.hidden_weights)}\n\n")

class TrainMLP():
    def __init__(self, model, epochs=10, learning_rate=0.01):
        self.model=model
        self.epochs=epochs
        self.learning_rate=learning_rate
    
    def training(self, losses=[]):
        for epoch in range(self.epochs):
            #feedforward
            y_pred=nn.Forward()
            #print("\n\n\n\n--------------------------------------------------------")
            #print(f"final predictions: {y_pred}")

            #calculate the loss
            mse_Loss=nn.Calculate_Loss(predictions=y_pred)
            #print(f"mse Loss: {mse_Loss}")


            nn.Backpropagation(predictions=y_pred, learning_rate=self.learning_rate)
            if epoch % 2 == 0:
                print(f"epoch: {epoch}| predictions: {y_pred}| loss: {mse_Loss}")
            


nn_train=TrainMLP(epochs=10, model=nn)
nn_train.training()