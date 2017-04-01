#Main method Rfor running models
import numpy as np
from scipy.sparse import *
from sklearn.decomposition import NMF
import os
from DataLoader import *
from NMF_ATNN import *
from autograd.optimizers import sgd
import utils
from utils import *
import NMF_ATNN
from sklearn.decomposition import NMF
import multiprocessing as mp

full_data  = DataLoader().LoadData(file_path="../Data/ml-100k/u.data",data_type=DataLoader.MOVIELENS)
full_data = full_data[:1000,:1700]
#Reduce the matrix to toy size
pre_train, pre_test = full_data[:200,:100], full_data[:400,:100]

#[Model Parameters
train_indx = [(np.array(range(200))),(np.array(range(100)))]
test_idndx = [np.random.choice(range(1000),40),np.random.choice(range(1700),20)]

can_usr_idx, can_mov_idx = get_canonical_indices(full_data, [utils.num_user_latents, utils.num_movie_latents])
train = fill_in_gaps([can_usr_idx, can_mov_idx], train_indx, full_data)
test = fill_in_gaps([can_usr_idx, can_mov_idx], test_idndx, full_data)

print "user idx ", can_usr_idx
print "movie idx", can_mov_idx

#Training Parameters
num_epochs = 20
num_iters = 5
step_size = 0.005

parameters = build_params(train.shape)
#Pretrain rating net and latents
grads = lossGrad(train)
#num_proc =  2#mp.cpu_count()
#grad_funs = gen_grads(train,num_proc)
#print grad_funs
#parameters = black_adam(grad_funs,parameters,step_size=step_size,
#                        num_iters=num_epochs, callback=dataCallback(train),num_proc=num_proc)
parameters = adam(grads,parameters, step_size=step_size,
                         num_iters=num_epochs, callback=dataCallback(train))
#Print performance on each model
invtrans = getInferredMatrix(parameters,train)
print "\n".join([str(x) for x in ["Train", print_perf(parameters,data=train), train, np.round(invtrans)]])

invtrans = getInferredMatrix(parameters,test)
print "\n".join([str(x) for x in ["Test", print_perf(parameters,data=test), test, np.round(invtrans)]])

