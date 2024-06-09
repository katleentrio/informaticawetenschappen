import os
import random
import json

# set fixed seed for generating test cases
random.seed(123456789)

# locate evaldir
evaldir = os.path.join("..", "evaluation")
if not os.path.exists(evaldir):
    os.makedirs(evaldir)

def write_json( data:dict ):
    """ A function to write JSON file"""
    with open(os.path.join("..", "evaluation", "tests.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent = 2)

# generate test data
ntests = 20
cases = [ ]
woorden = open('../workdir/words.txt').read().split("\n")
alfabet = "abcdefghijklmnopqrstuvwxyz"
indices = range(24)
gokken = []

while len( cases ) < ntests:
    seed = random.randint(1,10000)
    cases.append( (seed,) )
    if random.randint(0,3) == 0:
        gokjes = random.sample( range(8),8 )
    else:
        gokjes = random.sample( indices,14 )
    gokken.append(gokjes)
    
# generate unit tests for functions
exportdata = {"tabs": [] }
exportdata["tabs"].append( {"name": "Feedback",
                            "contexts": [] } )

i = -1

for test in cases:
    exportdata["tabs"][0]["contexts"].append({})
    i += 1
        
    seed = test[0]
    # generate before expression
    beforecase = {"python": {"data": "import random; random.seed("+str(seed)+")"}}
    exportdata["tabs"][0]["contexts"][i]["before"] = beforecase
    
    exportdata["tabs"][0]["contexts"][i]["testcases"] = []
    
    # PROGRAM IMPLEMENTATION
    outputtxt = ""
    inputtxt = ""
    random.seed(seed) #setting the seed
    
    woord = random.choice(woorden)

    aantal_correct = 0
    aantal_tekens = 8
    aantal_gokken = 0
    tekens = "????????"
    j = 0
    al_gehad = []
    while aantal_correct < aantal_tekens and aantal_gokken < 6:
        outputtxt += tekens+"\n"
        index = gokken[i][j]
        j +=1
        if index >= 8:
            gok = alfabet[index]
        else:
            gok = woord[index]
        
        inputtxt += gok+"\n"
        correct = False
        if gok not in tekens:
            for k in range(8):
                letter = woord[k]
                if gok == letter:
                    aantal_correct += 1
                    correct = True
                    
                    tijdelijk = list(tekens)
                    tijdelijk[k] = gok
                    tekens = "".join(tijdelijk)
            
        if correct == False:
            aantal_gokken += 1
            outputtxt += "Niet gevonden\n"

    if aantal_correct == 8:
        outputtxt += tekens+"\n"
        outputtxt += "Gelukt!\n"
    else:
        outputtxt += f"Het woord was {woord}\n"
    

    # generate test expression
    inputdescr = str.replace(inputtxt, "\n", " - ")  
    testcase = {"description": "Uitvoeren met seed "+str(seed)+" leidt tot het onderstaande (met als achtereenvolgende invoer "+inputdescr[:-3]+")",
                "input": {},
                "output": {} }
    

    # fill in the testcase
    testcase["input"]["stdin"] = {"type": "text", 
                                  "data": inputtxt }
    testcase["output"]["stdout"] = {"type": "text", 
                                    "data": outputtxt }

    exportdata["tabs"][0]["contexts"][i]["testcases"].append( testcase )

write_json( exportdata )