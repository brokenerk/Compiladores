#!python3
from AFN import AFN
from AFD import AFD
from CustomSet import CustomSet
epsilon = '\u03B5'

def menu():
    print('*********************************************************')
    print('************* C O M P I L A D O R E S *******************')
    print('1. Crear automata')
    print('2. Unir')
    print('3. Concatenar')
    print('4. Cerradura Positiva')
    print('5. Cerradura Epsilon')
    print('6. Cerradura de kleen')
    print('7. Opcional')
    print('8. Convertir a Afd')
    print('9. Automatota')
    print('10. Mostrar AFN')
    print('11. Mostrar AFD')
    print('12. Añadir token')
    print('')

if __name__ == "__main__":
    afn = [] 
    afd = []
    idAfd=-1
    while(1):
        menu()
        option = input('Ingresa una opción: ')
        
        if option == '1':

            print(' ************* Crear automata ***************')
            symbol = input('Ingresa una letra: ')
            afn.append(AFN.createBasic(symbol))
            input('Ingresa una tecla parca continuar')

        elif option == '2':

            print('')
            print('****************** Unir *********************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id del primer automata: '))
            afnb = int(input('Ingresa el id del segundo automata: '))
            afn.append( afn[afna-1].join(afn[afnb-1]) )
            input('Ingresa una tecla parca continuar')

        elif option == '3':

            print('')
            print('**************** Concatenar ******************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id del primer automata: '))
            afnb = int(input('Ingresa el id del segundo automata: '))
            afn.append( afn[afna-1].concat(afn[afnb-1]))
            input('Ingresa una tecla parca continuar')
        
        elif option == '4':

            print('')
            print('************* Cerradura Positiva **************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            afn.append( afn[afna-1].positiveClosure() )
            input('Ingresa una tecla parca continuar')

        elif option == '5':
            
            print('')
            print('************* Cerradura Epsilon Edo Inicial ***************')
            
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = input('Ingresa el id  automata: ')
            cs = CustomSet(afn[afna-1].getStates())
            e = afn.append(afn[afna-1].getStart())

            statesEpsilon = cs.positiveClosure(e)
            print("Cerradura {} estado inicial".format(epsilon))
            for edo in statesEpsilon:
            	print("E: {}".format(edo.getId()))

            input('Ingresa una tecla parca continuar')
            
        elif option == '6':
            
            print('')
            print('************* Cerradura de kleen ***************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            afn.append(afn[afna-1].kleeneClosure)
            input('Ingresa una tecla parca continuar')

        elif option == '7':
            
            print('')
            print('***************** Opcional *********************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            afn.append(afn[afna-1].optional())
            input('Ingresa una tecla parca continuar')

        elif option == '8':
            
            print('************** Convertir a Afd *****************')
            idAfd+=1
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            csAux = CustomSet(afn[afna-1].getStates())
            afd.append(afn[afna-1].convertToAFD(csAux))
            afd[idAfd].displayTable()
            
            input('Ingresa una tecla parca continuar')

        elif option == '9':
            print('**************** Automatota ********************')
            print('')
            afns = set([])
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            num = int(input('Ingresa el numero de  automatas que quieres agregar: '))
            for i in range(0, num):
                print('Ingresa el Id del Automata: ')
                id = int(input())
                afns.add(afn[id-1])
            afn.append(AFN.addNewStart(afns))

            input('Ingresa una tecla parca continuar')
        
        elif option == '10':

            print('')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            afn[afna-1].display()
            input('Ingresa una tecla parca continuar')
        
        elif option == '11':

            print('')
            for a in afd:
                print('Afn: {}'.format(a.getId()))
            afda = int(input('Ingresa el id del AFD: '))
            afd[afda-1].displayTable()
            input('Ingresa una tecla parca continuar')

        elif option == '12':

            print('')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))
            token = input('Ingresa el token del automata: ')
            afn[afna-1].setToken(token)

        else:
            input('Opcion incorrecta, ingresa una tecla parca continuar')
