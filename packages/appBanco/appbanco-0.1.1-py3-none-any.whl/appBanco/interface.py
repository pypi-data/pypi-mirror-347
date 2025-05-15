import textwrap
from .banco import Cliente, Deposito, Saque, cCorrente, encontrarUser, recAccUser

def menu():
    menu = """
    oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo
    [1] Extratos
    [2] Depósitos
    [3] Saques
    [4] Criar novo usuário
    [5] Criar nova conta
    [6] Mostrar contas
    [7] Sair
    oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo
    => """
    return input(textwrap.dedent(menu))

def Extratos(users):
    cpf = input("Qual o seu CPF? ")
    user = encontrarUser(cpf, users)
    if not user:
        print("Usuário não encontrado!")
        return
    conta = recAccUser(user)
    if not conta:
        return
    print("oOoOoOoOoOo EXTRATO oOoOoOoOoOo\n")
    transacoes = conta.reg.transacoes
    if not transacoes:
        print("Sem movimentações.")
    else:
        for t in transacoes:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo")

def Depositos(users):
    cpf = input("Qual o seu CPF? ")
    user = encontrarUser(cpf, users)
    if not user:
        print("Usuário não encontrado!")
        return
    valor = float(input("Quanto você quer depositar? "))
    conta = recAccUser(user)
    if conta:
        user.transacaoAction(conta, Deposito(valor))

def Saques(users):
    cpf = input("Qual o seu CPF? ")
    user = encontrarUser(cpf, users)
    if not user:
        print("Usuário não encontrado!")
        return
    valor = float(input("Quanto você quer sacar? "))
    conta = recAccUser(user)
    if conta:
        user.transacaoAction(conta, Saque(valor))

def novoUser(users):
    cpf = input("Qual CPF deseja cadastrar? ")
    if encontrarUser(cpf, users):
        print("Esse CPF já está cadastrado!")
        return
    nome = input("Qual é o seu nome? ")
    ddn = input("Quando você nasceu? ")
    endereco = input("Onde você reside (rua, bairro, cidade)? ")
    user = Cliente(cpf=cpf, nome=nome, ddn=ddn, endereco=endereco)
    users.append(user)
    print("Usuário registrado com sucesso!")

def novaConta(nConta, users, contas):
    cpf = input("Qual CPF deseja cadastrar? ")
    user = encontrarUser(cpf, users)
    if not user:
        print("Usuário não encontrado!")
        return
    conta = cCorrente.novaAcc(user, nConta)
    user.addConta(conta)
    contas.append(conta)
    print("Sua conta foi criada com sucesso!")

def mostrarContas(contas):
    for conta in contas:
        print("oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo")
        print(textwrap.dedent(str(conta)))
        print("oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo")
