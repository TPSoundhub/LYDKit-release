# En variabel med navnet 'a' som initielt får tildelt værdi nul (tallet 0)
a = 0
# En while løkke der gentages sålænge betingelsen (a<=5) "a er mindre eller lig med 5" er opfyldt
while a<=5:
    # udfører en handling/en funktion der udskriver værdien af variablen a i shell
    print(a)
    # en betinget sætning, der tester om a er større elelr mindre end 3 og udskriver det i shell
    if a<3:
        print("a mindre end 3")
    elif a>3:
        print("a større end 3")
    else:
        print("a er lig med 3")
    # der lægges 1 til værdien af variablen a
    a = a+1
print("while løkken er nu slut - Bemærk at koden både kan køre på PC/MAC og på Micro:Bitten")   