#Tor Testing Framework, as designed and Constructed by: The Monkey Catfish Coalition
#Provides a way to create and run test cases for Tor, using a specialized version of the Tor platform

import os
import subprocess
from time import localtime, asctime

def delTemp():
     #this portion empties the temp directory 
    for j in os.listdir("./temp/"):
        os.remove("./temp/" + j)

def delReport():
    #this portion empties the report directory and creates a new report file.
    for j in os.listdir("./reports/"):
        os.remove("./reports/" + j)

def buildTor():
    os.chdir("./project/")
    print(os.getcwd());
    subprocess.call("bash configure", shell=True)
    subprocess.call("make")
    print(os.getcwd());
    subprocess.call("sudo make install",shell=True)
    os.chdir("../")

def main():

    delTemp()
    delReport()
    buildTor()
    tests=[]
    #changes to the TestAutomation directory
    os.chdir("./")
    print(os.getcwd())
    for file in os.listdir("testCases"):
        if file.endswith(".txt"):
            print(file)
            with open(os.getcwd()+"/testCases/"+file, "r") as f:
                i =0
                lines =[]
                path = ""
                for line in f:
                    lines.append(line)
                    i = i+1
                print("this is test case #: "+lines[0].strip('\n'))
                tests.append(lines[0])
                driver=lines[6].strip('\n')
                print("this will be "+lines[1].strip('\n'))
                a,b,c = lines[4].split(',')
                

                subprocess.call(["tor",driver, a, b])

                answer = findAnswer(lines[6].strip('\n'))
                print("program gave us: " +answer)
                with open("./reports/report.html","a+") as report:
                    report.write("<style>table, th, td {border: 1px solid black;}</style>")
                    report.write("<table><tr><td>Test ID: </td><td>" + lines[0]+"</td></tr>")
                    report.write("<tr><td>Time stamp: </td><td>"+ asctime(localtime())+"</td></tr>")
                    report.write("<tr><td>requirement being tested: </td><td>" + lines[1]+"</td></tr>")
                    report.write("<tr><td>Component being tested: </td><td>" +lines[2]+"</td></tr>")
                    report.write("<tr><td>Method being tested: </td><td>" +lines[3]+"</td></tr>")
                    report.write("<tr><td>Inputs used for testing: </td><td>" +lines[4]+"</td></tr>")
                    report.write("<tr><td>Expected output: </td><td>"+lines[5]+"</td></tr>")
                    
                    if answer ==("no answer found"):
                        print("no answer found!")
                        report.write("<tr><td><b> <font color=\"red\">results in a segmentation fault</font></b></td></td>")
                        report.write("</table><br>")

                    elif answer ==(lines[5].strip('\n')):
                        print("This test has passed")
                        report.write("<tr><td>The outcome was: </td><td>" + answer+"</td></tr>")
                        report.write("<tr><td>The test  <font color=\"green\">passed</font></td></tr>")
                        report.write("</table><br>")
                   
                    else:
                        print("This test has failed")
                        report.write("<tr><td>the outcome was: </td><td>" + answer+"</td></tr>")
                        report.write("<tr><td>The test <font color=\"red\">failed</font></td></tr>")
                        report.write("</table><br>")
                
            print('\n')
    subprocess.call(["see", "./reports/report.html"])
                
    
def findAnswer(case):
    answer=""
    found = False
    for (root,dirs,files) in os.walk("./temp"):
        for i in files:
            if i == "TestCase"+str(case)+".txt":
                path=(root)
                print("answer found in " + path)
                with open(path+"/TestCase"+str(case)+".txt", "r") as f:
                    for line in f:
                        answer=line.strip('\n')
                found = True
    if found == False :
        print("no answer found")
        answer="no answer found"
    return answer
    
            

main()
