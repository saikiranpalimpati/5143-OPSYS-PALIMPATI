# SAIKIRAN PALIMPATI
# ASSIGNMENT 4 - OPERATING SYSYTEMS
# TO RUN THE PROGRAM FROM THE COMMAND PROMPT THE COMMAND BELOW IS EXECUTED.
# python driver.py filename=snapshots   
# SNAPSHOTS IS THE FOLDER WITH INPUT FILES
# IN THIS PROGRAM WE CALCULATE THE NUMBER OF PAGEFAULTS OCCURED WHILE A FEW SET OF PROCESS EXECUTE
# THE PLOTS ARE SAVED IN A FOLDER WITH NAME snapshots_results("filename_results")


#heder files
import sys
import os
import time
import random
import matplotlib.pyplot as plt

#function to format the input string
def str_binary(n,padd=12):
    binfrmt = '{fill}{align}{width}{type}'.format(fill='0', align='>', width=padd, type='b')
    n = format(n,binfrmt)
    return n


#error handling 
def usage(e):
    print("do it right...")
    print(e)
    sys.exit()


#extract the arhuments from command prompt
def myargs(sysargs):
    args = {}

    for val in sysargs[1:]:
        k,v = val.split('=')
        args[k] = v
    return args


#read the input file
def read_file(fin,delimiter="\n"):
    
    if os.path.isfile(fin):
        with open(fin) as f:
            data = f.read()
        data = data.strip()
        return data.split(delimiter)
    usage("Error: file does not exist in function 'read_file'...")
    return None




#replacement algorithms 
def replace_a_page_from_pm(replacement_algorithm,dicitionare,time):
    
    if (replacement_algorithm=="FIFO"):
        return FIFOreplacementAlgorithm(dicitionare)

    elif(replacement_algorithm=="LRU"):
        return LRUreplacementAlgorithm(dicitionare,time)

    elif(replacement_algorithm=="LFU"):
        return LFUreplacementAlgorithm(dicitionare,time)

    elif(replacement_algorithm=="RANDOMN"):
        return randomnReplacement(dicitionare)


#first in first out in this one the process that came first to the physical memory is given out
def FIFOreplacementAlgorithm(dictionare):
        return list(dictionare.keys())[0]



#least recently used : in this one the process that has not been accessed in a while is picked out
def LRUreplacementAlgorithm(dictionare,time):
    presentime=time
    least_recent=""
    for i in dictionare:
        j=dictionare[i].last_access
        # print("page",i," last access",j)
        if (j<presentime):
            presentime=j
            least_recent=i

    return least_recent


# least frequently used : in ths algorithm the process that has not been frequntly used is picked out
def LFUreplacementAlgorithm(dictionare,time):
    
    least_recent_page=""
    frequency=sys.maxsize
    
    for i in dictionare:
        no_of_access = dictionare[i].access_count
        time_in_PM = dictionare[i].time_InPm
        total_time_in_pm=time-time_in_PM
        frequency_of_pageusage = no_of_access / total_time_in_pm
        # print("process",i," is started at",total_time_in_pm," and is accessed ", no_of_access," frequency of",i," is ",frequency_of_pageusage)
        if (frequency_of_pageusage<frequency):
            least_recent_page=i
            frequency=frequency_of_pageusage
    return least_recent_page




#randomReplacement algorithm : in this one the process is picked out randomly
def randomnReplacement(dictionare):
    pagenumber=""
    page_list=[]
    for i in dictionare:
        page_list.append(i)
    randint=random.randint(0,len(page_list)-1)
    pagenumber=page_list[randint]
    return pagenumber


#pageframe : has the attributes of page
class page_frame(object):
    def __init__(self):
        self.valid_bit = False  # in memory
        self.dirty = False      # updated
        self.time_InPm = 0
        self.last_access = 0    # time stamp
        self.access_count = 0   # sum of accesses
    




#page table : keeps track of each page 
class page_table(object):
    
    #initialise page table for a process
    def __init__(self,virt_mem_page_count,phys_mem_size):
        self.vm_page_count = virt_mem_page_count
        self.pm_size = phys_mem_size
        self.pageFrame={}
    
    

    #add a page to the page table
    def add_page_PageTable(self,pagenumber):
        self.pageFrame.update({pagenumber:page_frame()})
    

    #if added to physical memory update that it to the page table
    def added_to_PM(self,pagenumber,time):
        self.pageFrame[pagenumber].valid_bit=True
        self.pageFrame[pagenumber].time_InPm=time
    


    #if already present in the PM and is accesed once agin then update it
    def update_About_Access(self,pagenumber,time):
        obj=self.pageFrame[pagenumber]
        obj.last_access=time
        obj.access_count+=1
    
    
    #check if the page is in PM or not
    def checkValid(self,pagenumber):   
        if self.pageFrame[pagenumber].valid_bit==True:
            return True
        else:
            return False
    
    #if the page is removed from the pm
    def remove_from_pm(self,pagenumber):
        self.pageFrame[pagenumber].valid_bit=False
        self.pageFrame[pagenumber].dirty=0
        self.pageFrame[pagenumber].time_InPm=0
        self.pageFrame[pagenumber].last_access=0
        self.pageFrame[pagenumber].access_count=0



#physical meory class 
class physical_memory(object):
    
    def __init__(self,mem_size):
        self.mem_size = mem_size
        self.mem_table = {}
    

    #when a page is added to the physical memory
    def addToPhysicalMemory(self,pagenumber,time):
        if len(self.mem_table)>=self.mem_size:
            return False
        else:
            self.mem_table.update({pagenumber:page_frame()})
            obj=self.mem_table[pagenumber]
            obj.valid_bit=True
            obj.time_InPm=time 
            return True
    

    #when a page in the physical memory is accessed
    def updateAcess(self,pagenumber,time):
        self.mem_table[pagenumber].last_access=time
        self.mem_table[pagenumber].access_count+=1
    

    #remove the pae from physical memory
    def removeFromMemory(self,pagenumber):
        del self.mem_table[pagenumber]

    def displayPhysicalMemory(self):
        for i in self.mem_table:
            valid = i.valid_bit
            acesstime = i.last_access
            accesscount=i.access_count
            print("{} {} {}".format(valid,acesstime,accesscount)) 



#virtual memory class
class virtual_memory(object):
    def __init__(self,mem_size):
        self.mem_size = mem_size
        self.mem_table = []
    
    def addToVirtualMemory(self,pagenumber):
        self.mem_table.append(pagenumber)
    
    def checkForPageInVirtualMemory(self,pagenumber):
        if (pagenumber in self.mem_table):
            return True
        else:
            return False

#plot the pagefaults with the algorithms used for replacement
def plotImage(algorithm,pageFaultCOunt,pm,vm):
    plt.bar(algorithm,pageFaultCOunt)
    title="physicalMemory = "+str(pm)+" virualMemory = "+str(vm)
    plt.tight_layout()
    plt.suptitle(title)
    plt.xlabel('Algorithms')
    plt.ylabel('PageFault Count')


#save the plots of each individual file in a directory
def save_plot(pm,vm,file):
    directory=os.getcwd()
    result_test=directory+"_results"
    if directory==result_test:
        directory=result_test
    else:
        os.chdir(result_test)
    directory_result=file
    
    if os.path.isdir(directory_result):
        pass
    else:
        os.mkdir(directory_result)
    strin="physicalMemory = "+str(pm)+" virualMemory = "+str(vm)+".png"
    os.chdir(directory_result)
    plt.savefig(strin)
    plt.figure()
    os.chdir(directory)





#main function
if __name__=='__main__':
    
    # start = time.time()
    args = myargs(sys.argv)

    if not 'filename' in args:
        usage("Error: filename not on command line...")
    
    if os.path.isdir(args['filename']):
        os.chdir(args['filename'])
        filelist=os.listdir()
        directory=os.getcwd()
        result_test=directory+"_results"
        exists=os.path.isdir(result_test)
        if exists:
            pass
        else:
            os.mkdir(result_test)
    else:
        print("please enter the directory name which contains input files")
    
    

    page_fault_each_file={}
    #Accessing each file on the input directory
    for file in filelist:
        #processing the file name
        f=os.path.basename(file)
        f = f.split('.')
        name=f[0]
        
        #np be number of processes and vm is size of virtual memory
        
        s,run,np,vm,pm = name.split('_')
        np=int(np)
        pm=int(pm)
        vm=int(vm)
        print("{} {} {} {}".format(s,run,np,vm,pm))
        # print(s)
        
        #store the whole data in a fiel to a string
        data=read_file(file," ")
        
        #thw list which contains replacement algorithms
        replace_algorithms=["FIFO","LRU","LFU","RANDOMN"]
        
        pagefualt_dict={}
        page_fault_each_algorithm={}
        
        
        
        
        #for each one of the replacement algorithm
        for algorithm in replace_algorithms:
            pageFaultCOunt=0
            timecounter=1
            
            #creating pyhsical memory
            pmobject=physical_memory(int(pm))
           
            #pagefault count for each process
            pagefault_count_each_process={}


            #creating virtual memory and a pagetable for each processes
            vm_obj=[]
            pagetable_obj=[]
            for i in range(0,int(np)):
                vm_obj.append(virtual_memory(vm))
                pagetable_obj.append(page_table(vm,pm))
                pagefault_count_each_process['process'+str(i)]=0
            
            i=1
            # data in each file
            #Accessing the data in a file
            for d in data:
                p,h = d.split(',')
                n = int(h, 16)
                b = str_binary(n,7)
                # print("{} {} \t{} ".format(p,h,n))
                p=int(p)
                vm_existance=vm_obj[p].checkForPageInVirtualMemory(n)
                Add_Page_To_PM = False
                pagenumber_pm=str(n)+"_"+str(p)
            
                #The data once converted then the process checks wether it is in the 
         
                #check wether it exists in virtual memory or not
                if(vm_existance==True):
                    #to check wether the page is in physical memory we lookup pagetable
                    page_existence_in_pm=pagetable_obj[p].checkValid(n)
                    # check wether the page is in physical memory
                    #if it exists update access count in physical memory and page tacble
                    if(page_existence_in_pm==True):
                        # print("page exist")
                        pmobject.updateAcess(pagenumber_pm,timecounter)
                        pagetable_obj[p].update_About_Access(n,timecounter)
                        # pmobject.displayPhysicalMemory()
                    elif(page_existence_in_pm==False):
                        # print("fage fault occured while adding this page")
                        pagefault_count_each_process['process'+str(p)]+=1
                        pageFaultCOunt+=1
                        # print("page should be added")
                        Add_Page_To_PM=True
                    

                #if it does not exist in virtual memory then put it in virtual memory then physical memory
                elif(vm_existance==False):
                    #pageFaultcount automatically goes up as it doesnot even exists in virtual memory
                    # print("fage fault occured while adding this page")

                    pageFaultCOunt+=1
                    pagefault_count_each_process['process'+str(p)]+=1
                    vm_obj[p].addToVirtualMemory(n)
                    pagetable_obj[p].add_page_PageTable(n)
                    Add_Page_To_PM=True
                    
                #add the page to physical memory
                if(Add_Page_To_PM==True):  
                    #check if it is getting added to physical memory
                    Page_Added_To_Pm=pmobject.addToPhysicalMemory(pagenumber_pm,timecounter)
                    #if added then let the pagetable  know that the page is added to physical memory
                    if Page_Added_To_Pm==True:
                        pagetable_obj[p].added_to_PM(n,timecounter)
                        
                        
                    #if it is not added then one of the page should be replaced
                    elif Page_Added_To_Pm==False:
                            
                        #get the page to be replaced from one of the replacement algorithms
                        pageToBeReplaced=replace_a_page_from_pm(algorithm,pmobject.mem_table,timecounter) 
                        # print("\t","page replaced is",pageToBeReplaced)  
                        #remove from physical memory
                        pmobject.removeFromMemory(pageToBeReplaced)
                        #string breakdown so that the process number and pagenumber can be breakdown
                        temp_page=pageToBeReplaced.split("_")
                        pageToBeReplaced_pagenumber=int(temp_page[0])
                        pageToBeReplaced_process=int(temp_page[1])   
                        #update the pagetable of the process
                        pagetable_obj[pageToBeReplaced_process].remove_from_pm(pageToBeReplaced_pagenumber)
                        #add the page to physical memory
                        pmobject.addToPhysicalMemory(pagenumber_pm,timecounter)
                        pagetable_obj[p].added_to_PM(n,timecounter)
                            
                #incrementing the time counter by 0.1
                timecounter+=0.1
                pagefault_count_each_process["total"]=pageFaultCOunt
                
            plotImage(algorithm,pageFaultCOunt,pm,vm)
               
                
            page_fault_each_algorithm[str(algorithm)+"algorithm"]=pagefault_count_each_process
            print("algorithm ",algorithm," no of pagefaults ",pagefault_count_each_process)
        save_plot(pm,vm,file)
            
        # page_fault_count_foreach_pm["for a PM of"+str(pm)]=page_fault_each_algorithm
            
        # page_fault_each_file["file"+str(file)+"with a VM of"+str(vm_o)]=page_fault_count_foreach_pm
  
  
