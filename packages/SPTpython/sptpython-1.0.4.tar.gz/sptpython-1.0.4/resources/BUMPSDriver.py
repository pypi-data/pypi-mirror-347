# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 09:32:55 2021

@author: Borges Liu
"""
import bumps.names as bmp
from bumps.fitters import fit
from bumps.formatnum import format_uncertainty
import numpy as np
import inspect
import matplotlib.pyplot as plt
import dill
import pandas as pd

class BUMPS():
    
    def __init__(self):
        try:
            import bumps
        except  ValueError:
            print('You must download bumps to continue')
        
        self.models=list()
        self.functions=list()
        self.parameters=list()
        self.settings={'dream': {'samples':1e5,'burn':100,'population':5,'thinning':1,'steps':500}}
        
    def addfunction(self,function,pars):
        
        ##this automatically scrapes your fit functions into the function list
        
        self.functions.append(function)
#                print(type(locals()[item]))
        print('function added')
        
        self.parameters.append(pars)
        print('parameters added')
        
        
    def addmodel(self,x,y,dy,index=-1):
        
        try:
            function=self.functions[index]##takes the last index - assumes by default that you added the parameters
            parameters=self.parameters[index]
        except ValueError:
            print('Function or Parameter list are empty')
            
        details=inspect.signature(function)
#        print(details)
        self.models = bmp.Curve(function,x,y,dy)
        
        ##iterate through parameters
        for key in details.parameters:
            #p=getattr(self.models[index],key)
            
            for par in parameters:
                if(par.name==key):
#                    print(key)
                    setattr(self.models,key,par)
    
    def setproblem(self,models):
        self.problem = bmp.FitProblem(models)
        
    def fitproblem(self,method='dream'):
        d=self.settings[method]
        
        self.result = fit(self.problem,
                          method='dream',
                          samples = d['samples'],
                          burn=d['burn'], 
                          pop=d['population'], 
                          init='eps', 
                          thin=d['thinning'], 
                          steps=d['steps'], 
                          store='test',
                          alpha = '0.01',
                          outliers = 'none',
                          trim = False,
                          verbose=True)
    
    def plotfit(self,scale,style='log-log'):
        
        plt.figure(figsize=(3,3),dpi=300)
        
        #colors=['r','b','g','c','k']
        model= self.models
        x=model.x
        y=model.y
        dy=model.dy
        
        f=model.fn##function
        p=[]
        
        for par in self.parameters[0]:
            p.append(par.value)
           
        
            
        print(p)
        plt.errorbar(x,y/scale,yerr=dy/scale,linestyle='',marker='o',label='data',markersize=1, capsize=1,linewidth=0,c='r')
        plt.plot(x,f(x,*p)/scale,linestyle='-',label='model',linewidth=0.5,c='b')
            
        plt.xlabel('x')
        plt.ylabel('y')
        
        if('log' in style):
            plt.xscale('log')
            plt.yscale('log')
            
        plt.legend()
        plt.show()
        return f(x,*p)
    def getparameters(self):
        
        # d={}
        
        
        # model = self.models
            
        # problem=self.problem
        # result=self.result
        
        # d['label']=[]
        # d['par']=[]
        # d['par_err']=[]
        
        # for key in problem.model_parameters()['models'].keys():
        #     count=0
        #     for j,l in enumerate(problem.labels()):
        #         if l==key:
        #             d['label'].append(key)
        #             d['par'].append(result.x[j])
        #             d['par_err'].append(result.dx[j])
        #             count+=1
                
        # if(count!=1):
        #     d['label'].append(key)
        #     d['par'].append(problem.model_parameters()['models'][key].value)
        #     d['par_err'].append(0)
        model= self.models
        x=model.x
        y=model.y
        dy=model.dy
        
        f=model.fn##function
        p=[]
        
        for par in self.parameters[0]:
            p.append(par.value)
    
        return p
    
    def savefitresult(self,fname='save.xlsx'):
        d={}
        pars=self.getparameters()
        ##write fit result summary to excel file with filename
        for i,model in enumerate(self.models):
            
            p=[]
            for par in self.parameters[i]:
                p.append(par.value)
           
            f=model.fn##function
            
            d['model_%d'%(i)]={}
            d['model_%d'%(i)]['x']=model.x
            d['model_%d'%(i)]['y']=model.y
            d['model_%d'%(i)]['y_fit']=f(model.x,*p)
            d['model_%d'%(i)]['dy']=model.dy
            
            d['model_%d'%(i)]['par_labels']=pars[i]['label']
            d['model_%d'%(i)]['par_vals']=pars[i]['par']
            d['model_%d'%(i)]['par_err']=pars[i]['par_err']
            
            # Create a Pandas Excel writer using XlsxWriter as the engine.
            writer = pd.ExcelWriter(fname, engine='xlsxwriter')
            
            # Write each dataframe to a different worksheet.
            for key in d.keys():
                df = pd.DataFrame.from_dict(d[key], orient='index').T
                df.to_excel(writer, sheet_name=key)
            
            writer.save()
#            df.to_excel(fname)
        return d 
        
    def save(self):
        return dill.dumps(self)
    
    def load(self,obj):
        self.__dict__.update(dill.loads(obj).__dict__)