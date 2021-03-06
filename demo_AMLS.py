""" Generates data to show the effect of rescaling. Low density basisfunctions used. """

import pandas
from rbf import *
import basisfunctions, testfunctions
import matplotlib.pyplot as plt
from matplotlib import cm
import time
import mesh
import math
from mpl_toolkits.mplot3d import Axes3D
from random import randint
from scipy import spatial
from halton import *

start = time.time()
j = 0
#nPointsRange = [1000,2000,4000,8000,10000,12000,16000]
for i in range(0,1):
	nPoints = 5
	nPointsOut = 5
	haltonPoints = halton_sequence(nPoints, 2)
	print("Number of points: ",nPoints)
	#in_mesh = np.linspace((1,2),(10,20),nPoints)
	in_mesh = np.random.random((nPoints,2))
	for i in range(0,nPoints):
		in_mesh[i,0] = haltonPoints[0][i]*haltonPoints[0][i]
		in_mesh[i,1] = haltonPoints[1][i]
	out_mesh = np.random.random((nPointsOut,2))
	#print("in_mesh: ", in_mesh)
	plt.scatter(in_mesh[:,0], in_mesh[:,1], label = "In Mesh",s=2)
	plt.scatter(out_mesh[:,0], out_mesh[:,1], label = "Out Mesh",s=2)
	plt.show()

	tree = spatial.KDTree(list(zip(in_mesh[:,0],in_mesh[:,1])))
	nearest_neighbors = []
	shape_params = []
	for j in range(0,nPoints):
		queryPt = (in_mesh[j,0],in_mesh[j,1])
		nnArray = tree.query(queryPt,2)
		#print(nnArray[0][1])
		nearest_neighbors.append(nnArray[0][1])
		shape_params.append(0)

	maxNN = max(nearest_neighbors)
	func = lambda x,y: np.sin(10*x)+(0.0000001*y)
	one_func = lambda x: np.ones_like(x)
	in_vals = func(in_mesh[:,0],in_mesh[:,1])
	out_vals = func(out_mesh[:,0],out_mesh[:,1])
	#for j in range(0,nPoints):
	#	shape_params[j]=4.55228/(5*maxNN)
	for k in range(10,11):
		for j in range(0,nPoints):
			shape_params[j]=4.55228/(k*nearest_neighbors[j])
		#shape_parameter = 4.55228/((k)*maxNN)
		#print("shape_parameter: ",shape_parameter)
		bf = basisfunctions.Gaussian(list(shape_params))
		#func = lambda x: (x-0.1)**2 + 1
	
		#print(in_vals)	
	#	evaluatine_vals = func(evaluate_mesh)
#		basis_vals = func(basis_mesh)

		interp = AMLS(bf, in_mesh, in_vals, rescale = False)
		interp_out_vals, Q = interp(out_mesh)

		inverse = AMLSInverse(bf, in_mesh, in_vals, rescale = False)		
		C, Cinv = inverse(out_mesh)

		print("C ", C)
		print("Cinv: ", Cinv)
		print("np.identity(nPoints): ", np.identity(nPoints) - C)
		CIapprox = np.identity(nPoints) * 0
		AA = np.identity(nPoints) - C
		CInew = np.identity(nPoints) * 0
		for tt in range(1,20):
			CInew = np.identity(nPoints) * 0
			for jj in range(0,tt):
				CInew += AA	
			CIapprox += CInew
		print("CIapprox: ", CIapprox)

		#error_LOOCV = LOOCV(bf, in_mesh, in_vals, rescale = False)
		#errors = error_LOOCV() 
		print("Max Error: ", max(out_vals - interp_out_vals))
		print("Average Error: ", abs(np.average(out_vals - interp_out_vals)))
	
	#error_LOOCVSVD = LOOCVSVD(bf, in_mesh, in_vals, rescale = False)
	#errorsSVD = error_LOOCVSVD() 
	#print("Error SVD: ", max(errorsSVD))
	#print("Error Difference: ", errors - errorsSVD)

	#end = time.time()
	#print("Elapsed time: ", end - start)

	#resc_interp = NoneConsistent(bf, in_mesh, in_vals, rescale = True)
	#one_interp = NoneConsistent(bf, in_mesh, one_func(in_mesh), rescale = False)
	'''
	plt.scatter(in_mesh[:,0], in_mesh[:,1], label = "In Mesh")
	plt.scatter(plot_mesh[:,0], plot_mesh[:,1], label = "Out Mesh")
	
	#plt.legend()
	#plt.show()

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')

	ax.scatter(in_mesh[:,0],in_mesh[:,1], in_vals, c='r', marker='o')

	ax.set_xlabel('X coordinate')
	ax.set_ylabel('Y ycoordinate')
	ax.set_zlabel('Magnitude')

	#plt.show()
	'''

	#fig = plt.figure()
	#ax = Axes3D(fig)
	#plt.scatter(in_mesh[:,0],in_mesh[:,1], errors, c = 'b', marker='o')

	#plt.plot(evaluate_mesh, interp(evaluate_mesh), "--", label = "Interpolant $S_f$")
	#plt.plot(evaluate_mesh, evaluate_vals, "--", label = "Interpolant $S_r$ of $g(x) = 1$")
	#plt.plot(evaluate_mesh, evaluate_vals - interp(evaluate_mesh), "--", label = "Error on selected points")


	#plt.tight_layout()
	#plt.plot(in_mesh, in_vals, label = "Rescaled Interpolant")

	#fig = plt.figure()
	#ax = Axes3D(fig)
	#surf = ax.plot_trisurf(in_mesh[:,0], in_mesh[:,1], in_vals)
	#fig.colorbar(surf, shrink=0.5, aspect=5)
	#plt.savefig('testSurrogate.pdf')
	#plt.show()

	#fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')

	#ax.scatter(in_mesh[:,0],in_mesh[:,1], errors, c='r', marker='o')

	#ax.set_xlabel('X coordinate')
	#ax.set_ylabel('Y ycoordinate')
	#ax.set_zlabel('Error Magnitude')

	#plt.show()

	#rint("RMSE no rescale =", interp.RMSE(func, plot_mesh))
	#print("RMSE rescaled   =", resc_interp.RMSE(func, plot_mesh))

end = time.time()
print("Elapsed time: ", end - start)

'''
	plt.plot(plot_mesh, interp.error(func, plot_mesh))
	plt.plot(plot_mesh, resc_interp.error(func, plot_mesh))
	plt.grid()
	plt.show()

	df = pandas.DataFrame(data = { "Target" : func(plot_mesh),
                               "Interpolant" : interp(plot_mesh),
                               "RescaledInterpolant" : resc_interp(plot_mesh),
                               "OneInterpolant" : one_interp(plot_mesh),
                               "Error" : interp.error(func, plot_mesh),
                               "RescaledError" : resc_interp.error(func, plot_mesh)},
                      index = plot_mesh)

	df.to_csv("rescaled_demo.csv", index_label = "x")
'''
