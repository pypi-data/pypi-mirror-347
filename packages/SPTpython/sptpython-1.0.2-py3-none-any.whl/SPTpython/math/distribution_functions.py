import numpy as np
import scipy.integrate

#############
# SINGLE PDFs
#############
def exponential(x,k1):
    return k1*np.exp(-x*k1)

def log10_exponential(x,a):
    return np.power(10,x)*np.log(10)*a*np.exp(-a*np.power(10,x))

def gaussian(x, k1, mu):
    return (1/np.sqrt(2*np.pi*np.power(k1,2)))*np.exp(-np.power(x-mu,2)/(2*np.power(k1,2)))

def pow10gaussian(x, k1, mu):
    return (1/np.sqrt(2*np.pi*np.power(k1,2))*x*np.log(10))*np.exp(-np.power(np.log10(x)-mu,2)/(2*np.power(k1,2)))

def log10exponential_w_uncertainty(x, D, sigma, t):
    sigmasquare_gaussian = 2*D*t + np.power(sigma, 2)
    return np.log(10)/(2*sigmasquare_gaussian)*np.power(10,x)*np.exp(-np.power(10,x)/(2*sigmasquare_gaussian))

def log10_chi(x,D,k,sigma, t):
    # from Landfield and Wang, 2022
    sigmasquare_chi = 2*D*t + np.power(sigma, 2)
    return np.log(10)/(np.power(2,k)*scipy.special.gamma(k))*np.power(np.power(10,x)*k/sigmasquare_chi,k)*np.exp(-(np.power(10,x)*k)/(2*sigmasquare_chi))

def log10_chi_distributed_D(x,k,lam,sigma, t):
    prefactor = (lam*np.log(10)*np.power(np.power(10,x)*k,k))/(np.power(2,k)*scipy.special.gamma(k))
    integrate_function = lambda D, this_x:np.power(2*D*t+np.power(sigma, 2),-k)*np.exp((-(np.power(10,this_x)*k)/(2*(2*D*t+np.power(sigma, 2))))-lam*D)
    integral_values = np.zeros(len(x))
    for idx, this_x in enumerate(x):
        integral_values[idx] = scipy.integrate.quad(integrate_function, 0, np.inf, args=(this_x,))[0]
    return prefactor*integral_values

#############
# DOUBLE PDFs
#############

def two_log10_exponential(x,k1,k2,a):
    return a*log10_exponential(x,k1) + (1-a)*log10_exponential(x,k2)

def gaussian_and_log10_exponential(x,k1,mu,k2,a):
    return a*gaussian(x,k1,mu) + (1-a)*log10_exponential(x,k2)

def pow10gaussian_and_exponential(x,k1,mu,k2,a):
    return a*pow10gaussian(x,k1,mu) + (1-a)*exponential(x,k2)

def two_log10exponential_w_uncertainty(x, D1, D2, a,sigma, t, debug = False):
    if debug:
        print(f"Inputs: D2:{D2}, sigma:{sigma}, a:{a}")
    # Currently assuming zero diffusivity on first population
    return a*log10exponential_w_uncertainty(x, D1, sigma, t) + (1-a)*log10exponential_w_uncertainty(x, D2, sigma, t)

def two_log10_chis(x, k1, D2, k2, a,sigma, t, debug = False):
    if debug:
        print(f"Inputs: k1:{k1}, sigma:{sigma}, D2:{D2}, k2:{k2}, a:{a}")
    return a*log10_chi(x, 0, k1,sigma, t) + (1-a)*log10_chi(x,D2,k2,sigma, t)

def distributed_D_and_log10chi(x, k1, k2, lam, a,sigma, t, debug = False):
    if debug:
        print(f"Inputs: sigma:{sigma}, k1:{k1}, k2:{k2}, lam:{lam}, a:{a}")
    return a*log10_chi(x, 0, k1,sigma, t)+(1-a)*log10_chi_distributed_D(x, k2, lam,sigma, t)


####################
# JACOBIAN FUNCTIONS
####################

def jac_2chi(x, k1, D2, k2, a,sigma, t):
    output = np.zeros((len(x),5))
    output[:,0] = a*partialchi_partialk(x,0,k1,sigma,t)
    output[:,1] = (1-a)*partialchi_partiald(x,D2,k2,sigma,t)
    output[:,2] = (1-a)*partialchi_partialk(x,D2,k2,sigma,t)
    output[:,3] = log10_chi(x,0,k1,sigma,t) - log10_chi(x,D2,k2,sigma,t)
    output[:,4] = a*(partialchi_partialsigma(x,0,k1,sigma,t))+(1-a)*(partialchi_partialsigma(x,D2,k2,sigma,t))
    return output

def jac_2exp(x, D1, D2, a,sigma, t, sigma_param = False):
    if sigma_param:
        output = np.zeros((len(x),3))
        output[:,0] = a*partialexp_partiald(x,D1,sigma,t)
        output[:,1] = (1-a)*partialexp_partiald(x,D2,sigma,t)
        output[:,2] = log10exponential_w_uncertainty(x,D1,sigma,t) - log10exponential_w_uncertainty(x,D2,sigma,t)
    else:
        output = np.zeros((len(x),4))
        output[:,0] = a*partialexp_partiald(x,D1,sigma,t)
        output[:,1] = (1-a)*partialexp_partiald(x,D2,sigma,t)
        output[:,2] = log10exponential_w_uncertainty(x,D1,sigma,t) - log10exponential_w_uncertainty(x,D2,sigma,t)
        output[:,3] = a*partialexp_partialsigma(x,D1,sigma,t)+(1-a)*partialexp_partialsigma(x,D2,sigma,t)
    return output

def partialchi_partialk(x,D,k,sigma,t):
    inner = (np.power(10,x)*k)/(np.power(sigma,2)+2*D*t)
    common_part = (-1+np.log(2)-np.log(inner)+scipy.special.polygamma(0,k))
    
    first = -1/((np.power(sigma,2)+2*D*t)*scipy.special.gamma(k))
    second = np.power(2,-1-k)*np.exp(-np.power(10,x)*k/(2*(2*D*t+np.power(sigma,2))))
    third = np.power(inner,k)
    fourth = np.log(10)
    sum = np.power(10,x)+2*np.power(sigma,2)*common_part + 4*D*t*common_part
    return first*second*third*fourth*sum

def partialchi_partialsigma(x,D,k,sigma,t):
    inner = (np.power(10,x)*k)/(np.power(sigma,2)+2*D*t)

    top = -np.power(2,-k)*np.exp(-np.power(10,x)*k/(2*(2*D*t+np.power(sigma,2))))*k*sigma*np.power(inner, k)*(-np.power(10,x)+2*np.power(sigma,2)+4*D*t)*np.log(10)
    bottom = np.power(np.power(sigma, 2)+2*D*t,2)*scipy.special.gamma(k)

    return top/bottom

def partialchi_partiald(x,D,k,sigma,t):
    inner = (np.power(10,x)*k)/(np.power(sigma,2)+2*D*t)

    top = -np.power(2,-k)*np.exp(-np.power(10,x)*k/(2*(2*D*t+np.power(sigma,2))))*k*t*np.power(inner, k)*(-np.power(10,x)+2*np.power(sigma,2)+4*D*t)*np.log(10)
    bottom = np.power(np.power(sigma, 2)+2*D*t,2)*scipy.special.gamma(k)

    return top/bottom

def partialexp_partiald(x,D,sigma,t):
    sigmasquare_gaussian = 2*D*t + np.power(sigma, 2)
    inner = -np.power(10,x)/(2*sigmasquare_gaussian)
    sum = np.power(10,x)-2*np.power(sigma,2)-4*D*t
    
    top = np.power(2,-1+x)*np.power(5,x)*np.exp(inner)*t*sum*np.log(10)
    bottom = np.power(sigmasquare_gaussian,3)
    
    return top/bottom

def partialexp_partialsigma(x,D,sigma,t):
    sigmasquare_gaussian = 2*D*t + np.power(sigma, 2)
    inner = -np.power(10,x)/(2*sigmasquare_gaussian)
    sum = np.power(10,x)-2*np.power(sigma,2)-4*D*t
    
    top = np.power(2,-1+x)*np.power(5,x)*np.exp(inner)*sigma*sum*np.log(10)
    bottom = np.power(sigmasquare_gaussian,3)
    
    return top/bottom

#######################
# Expectation Functions
#######################

def expected_2log10_chi(k1, D2, k2, a,sigma, t):
    expected_val_1 = scipy.integrate.quad(lambda x:x*log10_chi(x,0,k1,sigma,t),-50,50)
    expected_val_2 = scipy.integrate.quad(lambda x:x*log10_chi(x,D2,k2,sigma,t),-50,50)

    return expected_val_1[0], expected_val_2[0]

def expected_2log10_exp(D1,D2, a,sigma, t):
    expected_val_1 = scipy.integrate.quad(lambda x:x*log10exponential_w_uncertainty(x,D1,sigma,t),-50,50)
    expected_val_2 = scipy.integrate.quad(lambda x:x*log10exponential_w_uncertainty(x,D2,sigma,t),-50,50)
    
    return expected_val_1[0], expected_val_2[0]

if __name__ == '__main__':
    print(scipy.integrate.quad(lambda x: two_log10exponential_w_uncertainty(x,1,1,1,1),-20,20))