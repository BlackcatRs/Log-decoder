import shutil
import time
import subprocess
import select

f = subprocess.Popen(['tail','-F','/path/to/log/file'],\
        stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p = select.poll()
p.register(f.stdout)

srcMac=""
src=""
dstMac=""
dst=""
proto=""
appName=""

while True:
    if p.poll(1):
        #print(f.stdout.readline().decode("utf-8"))
        if "drop" in f.stdout.readline().decode("utf-8") :

            tableau=f.stdout.readline().decode("utf-8").split()

            for value in tableau:
                if "srcMac" in value:
                    srcMac=value
                    src=tableau[(tableau.index(value)) + 1]

                if "dstMac" in value:
                    dstMac=value
                    dst=tableau[(tableau.index(value)) + 1]

                if "proto" in value:
                    proto=value

                # recuperer le nom d'application
                if "appName=" in value:

                    # variable appName contient le nom d'application
                    appName=value

                    # l'index de la variable appName dans le tableau
                    i=tableau.index(value) +1 #19+1

                    # recuperer le nom complet d'application
                    while 1:
                        if "msg=" in (tableau[i]) : #20
                            break
                        else:
                            appName+=" "
                            appName+=tableau[i] #20

                        # compteur utlise par tableau precendent
                        i+=1 #21

                # affiche le champs msg
                if "msg=" in value:
                    # variable message contient la valeur de value et va contenir le message complet
                    message=value

                    # l'index de value
                    i=tableau.index(value) #14

                    # concatenation des donnees recuperee dan la variable message
                    while 1:
                        i+=1 #15
                        if "=" in (tableau[i]) : #15
                            break
                        else:
                            message+=" "
                            message+=tableau[i] #15

                    # extraire d'information est fini et passe au log suivant
                    break

            #print(message, "\n")
            print(srcMac + " -> " + dstMac)
            print(src + " -> " + dst)
            print(appName)
            print(proto)
            print(message)

            columns = shutil.get_terminal_size().columns
            print("------------------------------------------------------------\n".center(columns))



    time.sleep(1)
