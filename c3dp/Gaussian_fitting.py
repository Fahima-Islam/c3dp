import numpy as np
import os, sys
parent_dir = os.path.abspath(os.pardir)
libpath = os.path.join(parent_dir, 'c3dp_source')
result_path=os.path.join(parent_dir, 'results')

if not libpath in sys.path:
    sys.path.insert(0, libpath)


from matplotlib import pyplot as plt

def gauss(x, amplitude, position, sigma):
    return amplitude/np.sqrt(2*np.pi)/sigma * np.exp( -(x-position)**2/2./sigma**2)

def findvalue(seq, val, rtol=0.03):    # value that works for your example
    return np.where(np.isclose(seq, val, rtol=rtol))[0]

from lmfit import Model
gmodel = Model(gauss)





coll_exp=np.load(os.path.join(result_path, 'I_d_coll_exp_masked.npy'))
clampSi_exp_masked=np.load(os.path.join(result_path, 'I_d_clampCell_Si_exp_masked.npy'))

params = gmodel.make_params( amplitude=0.5,position=3.13, sigma=0.8)
d=clampSi_exp_masked[0,:]
I=clampSi_exp_masked[1,:]

coll_d=coll_exp[0,:]
coll_I=coll_exp[1,:]

bg= gmodel.fit(I, params, x=d)

I_minus_bg=I-bg.best_fit

ind_d_3pt12=findvalue(d,3.13)

ind_d_3pt12_coll=findvalue(coll_d,3.13)



result = gmodel.fit(I[ind_d_3pt12], params, x=d[ind_d_3pt12])
result_coll = gmodel.fit(coll_I[ind_d_3pt12_coll], params, x=coll_d[ind_d_3pt12_coll])

plt.figure(figsize=(10,6))

print (result_coll.params['sigma'].value-result.params['sigma'].value)


plt.plot(d[ind_d_3pt12], I[ind_d_3pt12],'pink', label='Without Collimator ')
plt.plot(d[ind_d_3pt12], result.best_fit, 'r--', label='Without Collimator fitted with Gaussian model')
plt.plot(coll_d[ind_d_3pt12_coll], coll_I[ind_d_3pt12_coll]*22,'blue', label='With collimator')
plt.plot(coll_d[ind_d_3pt12_coll], result_coll.best_fit*22, 'g--',  label='With Collimator fitted with Gaussian model')

plt.text(1.2, 190000, r'$\delta d= 0.005 \AA$', fontsize=10)
plt.text(1.2, 181000, r'where $\delta d$ is difference in width between fitted with and without'"\n"r'collimator profile',
         fontsize=10)
plt.text(1.2, 171000, r'Corresponding $TOF$ for $d=3.13 \AA$ is $10.37$ $milli second$ ',
         fontsize=10)

plt.text(1.2, 165000, r'Hence, $\delta TOF=0.015$ $millisecond$',
         fontsize=10)

plt.xlim(1.,4.)

plt.legend()
plt.xlabel('d-spacing ($\AA$)')
plt.ylabel('Intensity (Arbitary Units)')

plt.show()

