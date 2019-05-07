import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



if __name__=='__main__':
    directory=os.getcwd()
    name=directory+"\\"+"snapshots_results"
    os.chdir(name)
    files=os.listdir()
    fig=plt.figure(figsize=(100, 100))
    columns=3
    rows = 1
    i=1
   
    for file in files:
        img=mpimg.imread(file)
        fig.add_subplot(rows, columns, i)
        plt.imshow(img)
        i+=1 
        plt.figure(figsize=(60,60))
        plt.axis('off')   
    plt.savefig("result.png") 
 
   
        