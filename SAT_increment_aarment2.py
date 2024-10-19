#                           DFS SAT
#                       aarment2 Project01

import time
import random
import string
import csv
import sys
import matplotlib.pyplot as plt


# Following is an example of a wff with 3 variables, 3 literals/clause, and 4 clauses
Num_Vars=3
Num_Clauses=4
wff=[[1,-2,-2],[2,3,3],[-1,-3,-3],[-1,-2,3],[1,2,-3]]


# Following is an example of a wff with 3 variables, 3 literals/clause, and 8 clauses
Num_Clauses=8
wff=[[-1,-2,-3],[-1,-2,3],[-1,2,-3],[-1,2,3],[1,-2,-3],[1,-2,3],[1,2,-3],[1,2,3]]


def check_dfs(Wff, Nvars, Nclauses, Assignment, index):
    if index > Nvars:       # BASE: only reaches this point if all literals have been assigned a truth value (tested)
        for clause in Wff:
            Satisfiable = False
            for literal in clause:
                VarValue = Assignment[abs(literal)]
                if (literal > 0 and VarValue == 1) or (literal < 0 and VarValue == 0):
                    Satisfiable = True
                    break
            if not Satisfiable: 
                return False
        return True   

    Assignment[index] = 1   # Assigns true to variable at current index
    if check_dfs(Wff, Nvars, Nclauses, Assignment, index + 1):
        return True

    Assignment[index] = 0   # Assigns true to variable at current index
    if check_dfs(Wff, Nvars, Nclauses, Assignment, index + 1):
        return True

    return False

def build_wff(Nvars, Nclauses, LitsPerClause):  # generates randomized test cases
    wff = []
    for i in range(1, Nclauses+1):
        clause = []
        for j in range(1, LitsPerClause+1):
            var = random.randint(1, Nvars)
            if random.randint(0,1) == 0:
                var = -var
            clause.append(var)
        wff.append(clause)
    return wff

def test_wff(wff, Nvars, Nclauses):
    Assignment = list((0 for x in range(Nvars+1)))     # initializes literal assignments to all false
    start = time.time()
    SatFlag = check_dfs(wff, Nvars, Nclauses, Assignment, 1)
    end = time.time()
    exec_time = int((end-start)*1e6)
    return [wff, Assignment, SatFlag, exec_time]


def run_cases(TestCases, ProbNum, resultsfile, tracefile, cnffile):
    # TestCases: list of 4tuples describing problem
    #   0: Nvars = number of variables
    #   1: NClauses = number of clauses
    #   2: LitsPerClause = Literals per clause
    #   3: Ntrials = number of trials
    # ProbNum: Starting nunber to be given to 1st output run
    # resultsfile: path to file to hold output
    # tracefile: path to file to hold output
    # cnffile: path to file to hold output
    # For each randomly built wff, print out the following list
    #   Problem Number
    #   Number of variables
    #   Number of clauses
    #   Literals per clause
    #   Result: S or U for satisfiable or unsatisfiable
    #   A "1"
    #   Execution time
    #   If satisfiable, a binary string of assignments
    # Info
    if not(ShowAnswer):
        print("S/U will NOT be shown on cnf file")
# Each case = Nvars,NClauses,LitsPerClause,Ntrials
    f1=open(resultsfile + ".csv",'w')
    f2=open(tracefile + ".csv",'w')
    f3=open(cnffile + ".cnf","w")
    #initialize counters for final line of output
    Nwffs = 0
    Nsat = 0
    Nunsat = 0

    # data used for plotting
    exec_times = []
    problem_sizes = []


    for i in range(0,len(TestCases)):
        TestCase=TestCases[i]
        Nvars=TestCase[0]
        NClauses=TestCase[1]
        LitsPerClause=TestCase[2]
        Ntrials=TestCase[3]

        Scount = 0
        Ucount = 0
        AvgStime = 0
        AvgUtime = 0
        MaxStime = 0
        MaxUtime = 0

        for j in range(0, Ntrials):     # generates multiple trials to help recognize trend 
            Nwffs += 1
            random.seed(ProbNum)
            wff = build_wff(Nvars,NClauses,LitsPerClause)
            results = test_wff(wff,Nvars,NClauses)
            wff = results[0]
            Assignment = results[1]
            Exec_Time = results[3]

            exec_times.append(Exec_Time)
            problem_sizes.append(NClauses)

            if results[2]:
                y='S'
                Scount += 1
                AvgStime += Exec_Time
                MaxStime= max(MaxStime,Exec_Time)
                Nsat += 1
            else:
                y='U'
                Ucount += 1
                AvgUtime += Exec_Time
                MaxUtime = max(MaxUtime,Exec_Time)
                Nunsat += 1
            x=str(ProbNum)+','+str(Nvars)+','+str(NClauses)+','+str(LitsPerClause)
            x=x+str(NClauses*LitsPerClause)+','+y+',1,'+str(Exec_Time)
            if results[2]:
                for k in range(1,Nvars+1):
                    x=x+','+str(Assignment[k])
            print(x)
            f1.write(x+'\n')
            f2.write(x+'\n')
            #Add wff to cnf file
            if not(ShowAnswer):
                y='?'
            x="c "+str(ProbNum)+" "+str(LitsPerClause)+" "+y+"\n"
            f3.write(x)
            x="p cnf "+str(Nvars)+" "+str(NClauses)+"\n"
            f3.write(x)
            for i in range(0,len(wff)):
                clause=wff[i]
                x=""
                for j in range(0,len(clause)):
                    x=x+str(clause[j])+","
                x=x+"0\n"
                f3.write(x)
            #Increment problem number for next iteration
            ProbNum=ProbNum+1
        counts='# Satisfied = '+str(Scount)+'. # Unsatisfied = '+str(Ucount)
        maxs='Max Sat Time = '+str(MaxStime)+'. Max Unsat Time = '+str(MaxUtime)
        aves='Avg Sat Time = '+str(AvgStime/Ntrials)+'. Avg UnSat Time = '+str(AvgUtime/Ntrials)
        print(counts)
        print(maxs)
        print(aves)
        f2.write(counts+'\n')
        f2.write(maxs+'\n')
        f2.write(aves+'\n')
    x=cnffile+",TheBoss,"+str(Nwffs)+","+str(Nsat)+","+str(Nunsat)+","+str(Nwffs)+","+str(Nwffs)+"\n"
    f1.write(x)
    f1.close()
    f2.close()
    f3.close()

    # Plotting Section
    plt.plot(problem_sizes, exec_times, marker = 'o')   # this plot is always updated and will show data from last run
    plt.title('Execution Time vs Problem Size')
    plt.xlabel('Problem Size (Number of clauses)')
    plt.ylabel('Execution Time (seconds)')
    plt.grid()

    plt.savefig('plots_aarment2.png')
    plt.close()

    if New_Medium_Plot == True:     # this plot is only for analyzing the results of check_medium_cases-aarment2.txt
        plt.plot(problem_sizes, exec_times, marker = 'o')
        plt.title('Execution Time vs Problem Size')
        plt.xlabel('Problem Size (Number of clauses)')
        plt.ylabel('Execution Time (seconds)')
        plt.grid()

        plt.savefig('plots_mediumcases_aarment2.png')
        plt.close()

    if New_Large_Plot == True:      # this plot is only for analyzing the results of check_large_cases-aarment2.txt
        plt.plot(problem_sizes, exec_times, marker = 'o')
        plt.title('Execution Time vs Problem Size')
        plt.xlabel('Problem Size (Number of clauses)')
        plt.ylabel('Execution Time (seconds)')
        plt.grid()

        plt.savefig('plots_largecases_aarment2.png')
        plt.close()

    


# Following generates several hundred test cases of 10 different wffs at each size
# and from 4 to 22 variables, 10 to 240 clauses, and 2 to 10 literals per clause 
TC1 =[
    [4,10,2,10],
    [8,16,2,10],
    [12,24,2,10],
    [16,32,2,10],
    [18,36,2,10],
    [20,40,2,10],
    [22,44,2,10],
    [24,48,2,10],
    [4,20,3,10],
    [8,40,3,10],
    [12,60,3,10],
    [16,80,3,10],
    [18,90,3,10],
    [20,100,3,10],
    [22,110,3,10],
    [24,120,3,10],
    [4,40,4,10],
    [8,80,4,10],
    [12,120,4,10],
    [16,160,4,10],
    [18,180,4,10],
    [20,200,4,10],
    [22,220,4,10],
    [24,240,4,10],
    [4,40,5,10],
    [8,80,5,10],
    [12,120,5,10],
    [16,160,5,10],
    [18,180,5,10],
    [20,200,5,10],
    [22,220,5,10],
    [24,240,5,10],
    [4,40,6,10],
    [8,80,6,10],
    [12,120,6,10],
    [16,160,6,10],
    [18,180,6,10],
    [20,200,6,10],
    [22,220,6,10],
    [24,240,6,10],
    ]

TC2=[
    [4,10,2,10],
    [8,16,2,10],
    [12,24,2,10]]

# Following generates a bunch of 2 literal wffs
SAT2=[
    [12,25,2,10],
    [12,26,2,10],
    [12,27,2,10],
    [12,28,2,10],
    [12,29,2,10],
    [16,30,2,10],
    [16,31,2,10],
    [18,32,2,10],
    [20,33,2,10],
    [22,34,2,10],
    ]

trace=True
ShowAnswer=True # If true, record evaluation result in header of each wff in cnffile
New_Medium_Plot=False   # If true, will change the plots_mediumcases_aarment2.png file
New_Large_Plot=False    # If true, will change the plots_largecases_aarment2.png file
ProbNum = 1
resultsfile = r'output_aarment2'
tracefile = r'tracefile-aarment2'
cnffile = r'cnffile-aarment2'   # Each of these list entries describes a series of random wffs to generate


if len(sys.argv) > 1:       # checks if user enters input file for test cases
    input_file = sys.argv[1]
    TestCases = []
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            TestCases.append([int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])])
    if input_file == 'check_medium_cases-aarment2.txt': # Will update the plot for medium cases
        New_Medium_Plot = True
    if input_file == 'check_large_cases-aarment2.txt': # Will update the plot for medium cases
        New_Large_Plot = True
    
else:
    TestCases = SAT2     # default test cases, but can be adjusted to the other ones from DumbSAT

run_cases(TestCases, ProbNum, resultsfile, tracefile, cnffile)