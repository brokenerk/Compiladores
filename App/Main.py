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
    
    while(1):
        menu()
        option = input('Ingresa una opción: ')
        
        if option == '1':

            print(' ************* Crear automata ***************')
            symbol = input('Ingresa una letra: ')
            afn.append(AFN.createBasic(symbol))
            input('Ingresa una tecla para continuar')

        elif option == '2':
            index = 0
            indexAfnA = 0
            indexAfnB = 0
            print('')
            print('****************** Unir *********************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id del primer automata: '))
            afnb = int(input('Ingresa el id del segundo automata: '))

            idx = 0
            while idx < len(afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1
            
            idx = 0
            while idx < len (afn):
                if afnb == afn[idx].getId():
                    indexAfnB = idx
                    break
                else:
                    idx+=1

            afn.append(afn[indexAfnA].join(afn[indexAfnB]))
            
            while index < len (afn):
                if afnb == afn[index].getId() or afna == afn[index].getId():
                    afn.pop(index)
                else:
                    index+=1
            
            input('Ingresa una tecla para continuar')

        elif option == '3':
            index = 0
            indexAfnA = 0
            indexAfnB = 0

            print('')
            print('**************** Concatenar ******************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id del primer automata: '))
            afnb = int(input('Ingresa el id del segundo automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1
            
            idx = 0
            while idx < len (afn):
                if afnb == afn[idx].getId():
                    indexAfnB = idx
                    break
                else:
                    idx+=1

            afn.append(afn[indexAfnA].concat(afn[indexAfnB]))

            while index < len (afn):
                if afnb == afn[index].getId() or afna == afn[index].getId():
                    afn.pop(index)
                else:
                    index+=1
            
            input('Ingresa una tecla para continuar')
        
        elif option == '4':
            index = 0
            indexAfnA = 0

            print('')
            print('************* Cerradura Positiva **************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            afn.append(afn[indexAfnA].positiveClosure())

            while index < len (afn):
                if afna == afn[index].getId():
                    afn.pop(index)
                    break
                else:
                    index+=1

            input('Ingresa una tecla para continuar')

        elif option == '5':
            index = 0
            indexAfnA = 0

            print('')
            print('************* Cerradura Epsilon Edo Inicial ***************')
            
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            cs = CustomSet(afn[indexAfnA].getStates())
            e = afn[indexAfnA].getStart()
            statesEpsilon = cs.epsilonClosure(e)
            print("Cerradura {} estado inicial".format(epsilon))
            for edo in statesEpsilon:
            	print("E: {}".format(edo.getId()))

            input('Ingresa una tecla para continuar')
            
        elif option == '6':
            index = 0
            indexAfnA = 0

            print('')
            print('************* Cerradura de kleen ***************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            afn.append(afn[indexAfnA].kleeneClosure())

            while index < len (afn):
                if afna == afn[index].getId():
                    afn.pop(index)
                    break
                else:
                    index+=1

            input('Ingresa una tecla para continuar')

        elif option == '7':
            
            index = 0
            indexAfnA = 0

            print('')
            print('***************** Opcional *********************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1
            
            afn.append(afn[indexAfnA].optional())

            while index < len (afn):
                if afna == afn[index].getId():
                    afn.pop(index)
                    break
                else:
                    index+=1
            
            input('Ingresa una tecla para continuar')

        elif option == '8':
            
            indexAfnA = 0

            print('************** Convertir a Afd *****************')
            
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            csAux = CustomSet(afn[indexAfnA].getStates())
            afd.append(afn[indexAfnA].convertToAFD(csAux))
            
            input('Ingresa una tecla para continuar')

        elif option == '9':
            indexAfnA = 0
            print('**************** Automatota ********************')
            print('')
            afns = set([])
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            num = int(input('Ingresa el numero de  automatas que quieres agregar: '))

            for i in range(0, num):
                print('Ingresa el Id del Automata: ')
                id = int(input())
                idx = 0
                while idx < len (afn):
                    if id == afn[idx].getId():
                        indexAfnA = idx
                        break
                    else:
                        idx+=1

                afns.add(afn[indexAfnA])

            afn.append(AFN.specialJoin(afns))

            for a in afns:
                index=0
                while index < len (afn):
                    if a.getId() == afn[index].getId():
                        afn.pop(index)
                    else:
                        index+=1

            input('Ingresa una tecla para continuar')
        
        elif option == '10':
            indexAfnA = 0
            idx = 0

            print('')
            print('**************** Mostrar AFN ****************')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id AFN: '))

            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            afn[indexAfnA].display()
            input('Ingresa una tecla para continuar')
        
        elif option == '11':
            indexAfdA = 0

            print('')
            print('**************** Mostrar AFD**************** ')
            for a in afd:
                print('Afn: {}'.format(a.getId()))
            afda = int(input('Ingresa el id del AFD: '))

            while idx < len (afd):
                    if afda == afd[idx].getId():
                        indexAfdA = idx
                        break
                    else:
                        idx+=1

            afd[indexAfdA].displayTable()
            input('Ingresa una tecla para continuar')

        elif option == '12':
            indexAfnA = 0

            print('')
            print('**************** Añadir token **************** ')
            for a in afn:
                print('Afn: {}'.format(a.getId()))
            afna = int(input('Ingresa el id  automata: '))

            idx = 0
            while idx < len (afn):
                if afna == afn[idx].getId():
                    indexAfnA = idx
                    break
                else:
                    idx+=1

            token = input('Ingresa el token del automata: ')

            afn[indexAfnA].setToken(token)

        else:
            input('Opcion incorrecta, ingresa una tecla para continuar')
