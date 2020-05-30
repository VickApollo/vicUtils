import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import graphviz
from sklearn import tree
import pydot
from sklearn.metrics import confusion_matrix
from matplotlib import colors as mcolors

class Hypnus():
    '''
    * Hypnus is the god of sleep and ilusion.
            
    Hypnus is also known as Somnus.
            
    * Hypnus generates all data visualizations
    '''
    
    def __init__(self):
        pass
    
    def getTestDf(self):
        pdt = pd.DataFrame([['D',1],['A',1],['B',2],['C',3]])
        pdt.columns = [ 'CLASSE' , 'NUM' ]
        return pdt
        
    @staticmethod
    def getColorDict():
        '''            
            Method to recover a dict of colors from matplotlib
            
            Return: Dictionary of colors
        '''
        
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        return colors
    
    def setClusterColor(self , dataframe , cluster):
        
        '''
            Method to set Cluster color for data visualization
        
            Parameters:
            - dataframe : Data Frame
            - cluster   : Column with the cluster's id
            
            Return: Original Data Frame with cluster column on "_CL_" column (added)
            
            example:
                hp = Hypnus()
                pdt = hp.getTestDf()
                pdt = hp.setClusterColor(pdt , 'NUM')
                print(pdt)
                
                ...  NUM CLASSE  IXS     _CL_
                ...   0    1      D    0  #9ACD32
                ...   1    1      A    0  #9ACD32
                ...   2    2      B    1  #FFFF00
                ...   3    3      C    2  #F5F5F5
        '''
        
        size = dataframe[cluster].drop_duplicates().values.size
        toss = dict()
        colorList = Hypnus.getColorDict()
        #colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        for i in range(0,size):
            color, code = random.choice(list(colorList.items()))
            toss[i] = (color , code)
        
        lmg = dataframe[cluster].drop_duplicates().reset_index()[cluster].reset_index()
        lmg.columns = ['IXS' , cluster]
        lmg['_CL_'] = lmg['IXS'].map(lambda x: toss.get(x)[1])
        
        dataframe = dataframe.set_index(cluster).join(lmg.set_index(cluster) , how='left' , rsuffix='_r')
        
        return dataframe.reset_index().drop('IXS', axis=1)
    
    
    def plot_confusion_matrix(self , cm, classes,
                              normalize=False,
                              title='Confusion matrix',
                              cmap=plt.cm.Blues ,
                              filename='confusion_matrix.png'):
        """
        This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
        """
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
            print("Normalized confusion matrix")
        else:
            print('Confusion matrix, without normalization')

        print(cm)

        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(classes))
        plt.xticks(tick_marks, classes, rotation=45)
        plt.yticks(tick_marks, classes)

        fmt = '.2f' if normalize else 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            plt.text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")

        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.savefig(filename)
        
        
        
    def renderDecisionTree(self , estimator=None , feature_names=None ,filename='tree'):
        dot_data = tree.export_graphviz(estimator , out_file=None , feature_names=feature_names)
        graph = graphviz.Source(dot_data)

        try:
            graph.render(filename)
        except Exception as e:
            print(str(e))

    def renderFeatureImportance(self , classifier , feature_name , 
                                xlabel='Importancia Relativa' , ylabel='Importancia da Variavel' , 
                                filename='feature_importance.png' , figsize=(15,15)):
        feature_importance = classifier.feature_importances_
        feature_importance = 100. * (feature_importance / feature_importance.max())
        sorted_idx = np.argsort(feature_importances)
        pos = np.arange(sorted_idx.shape[0]) + .5
        plt.figure(figsize=figzise)
        plt.barh(pos , feature_importance[sorted_idx] , align='center')
        plt.yticks(pos , feature_name[sorted_idx])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.savefig(filename)
