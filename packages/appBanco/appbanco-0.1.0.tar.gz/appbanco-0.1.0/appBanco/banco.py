from abc import ABC, abstractmethod
from datetime import datetime

class UserAcc:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def transacaoAction(self, conta, transacao):
        transacao.create(conta)

    def addConta(self, conta):
        self.contas.append(conta)

class Cliente(UserAcc):
    def __init__(self, cpf, nome, ddn, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.ddn = ddn

class Conta:
    def __init__(self, nConta, user):
        self._saldo = 0
        self._nConta = nConta
        self._agencia = "0001"
        self._user = user
        self._reg = Registro()

    @classmethod
    def novaAcc(cls, user, nConta):
        return cls(nConta, user)

    @property
    def saldo(self):
        return self._saldo

    @property
    def num(self):
        return self._nConta

    @property
    def agencia(self):
        return self._agencia

    @property
    def user(self):
        return self._user

    @property
    def reg(self):
        return self._reg

    def accSaques(self, valor):
        if valor > self._saldo:
            print("Seu saldo não é o suficiente. Tente novamente.")
        elif valor > 0:
            self._saldo -= valor
            print("Seu saque foi realizado com sucesso.")
            return True
        else:
            print("Valor inválido! Tente novamente.")
        return False

    def accDepositos(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Seu depósito foi realizado com sucesso.")
            return True
        else:
            print("Valor inválido! Tente novamente.")
            return False

class cCorrente(Conta):
    def __init__(self, nConta, user, lim=500, LIMITE_SAQUES=3):
        super().__init__(nConta, user)
        self._lim = lim
        self._LIMITE_SAQUES = LIMITE_SAQUES

    def accSaques(self, valor):
        nSaques = len([t for t in self.reg.transacoes if t["tipo"] == "Saque"])
        if valor > self._lim:
            print("Seu saque excede o limite permitido. Tente novamente.")
        elif nSaques >= self._LIMITE_SAQUES:
            print("Você já atingiu o número de saques permitidos.")
        else:
            return super().accSaques(valor)
        return False

    def __str__(self):
        return f"""
        oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo
        Agência: {self.agencia}
        Nº da conta: {self.num}
        Titular: {self.user.nome}
        oOoOoOoOoOoOoOoOoOoOoOoOoOoOoOo
        """

class Registro:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def addTransacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def create(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def create(self, conta):
        if conta.accSaques(self.valor):
            conta.reg.addTransacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def create(self, conta):
        if conta.accDepositos(self.valor):
            conta.reg.addTransacao(self)

def encontrarUser(cpf, users):
    for user in users:
        if user.cpf == cpf:
            return user
    return None

def recAccUser(user):
    if not user.contas:
        print("Você não possui uma conta!")
        return
    return user.contas[0]
