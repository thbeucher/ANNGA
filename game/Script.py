import os

for el in os.listdir(os.getcwd()):
    if not "Script" in el and ".py" in el:
        print("Generation du fichier c")
        com = "cython " + el + " --embed=WinMain"
        os.system(com)
        print("Generation de l'executable")
        com2 = "gcc " + el[:el.index(".")] + ".c -IC:\Python34\include -LC:\Python34\libs -lpython34 -o " + el[:el.index(".")] + ".exe"
        os.system(com2)
