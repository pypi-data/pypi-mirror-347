from appBanco.interface import *

def main():
    users = []
    contas = []

    while True:
        opcao = menu()
        if opcao == "1":
            Extratos(users)
        elif opcao == "2":
            Depositos(users)
        elif opcao == "3":
            Saques(users)
        elif opcao == "4":
            novoUser(users)
        elif opcao == "5":
            nConta = len(contas) + 1
            novaConta(nConta, users, contas)
        elif opcao == "6":
            mostrarContas(contas)
        elif opcao == "7":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
