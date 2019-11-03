

AA = list()
f = open("ver","r")
while True:
                        linea = f.readline().strip()
                        if not linea: break                              
                        AA.append(linea)      
f.close()
for i in range(len(AA)):
                        f = open(AA[i],"w")
                        while True:
                                                linea = f.readline().strip()
                                                if not linea: break                              
                                                linea.replace('href="octave.html"','href="octave.html"')
                        f.close()
