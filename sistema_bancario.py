# Adaptação do código para POO
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        # Atributos privados
        self._endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Função para o menu
def menu():
    menu ="""\n
    =============== MENU ===============
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar conta
    [nu]\tNovo usuário
    [q]\tSair

    => """
    return input(textwrap.dedent(menu))


# Recebe argumentos apenas por posição (Positional only)
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\n### Depósito realizado com sucesso! ###")
    else:
        print("\n### Operação falhou! O valor informado é inválido. ###")
    return saldo, extrato

    
# Recebe argumentos apenas por nome (Keywords only)
def sacar(*, saldo, valor, extrato, limite, numeros_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numeros_saques >= limite_saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou. Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou. O valor do saque excede o limite permitido. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou. Quantidade máximo de saques realizados. @@@")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numeros_saques += 1
        print("Saque realizado com sucesso.")
        print(f"Saques realizados hoje: {numeros_saques}")

    else:
        print("Operação falhou. O valor informado é inválido.")

    return saldo, extrato, numeros_saques


# Exibir extrato por posição e nome (Positional only e Keywords only)
def exibir_extrato(saldo, /,*, extrato):
    print("\n=============== EXTRATO ===============")
    print("NÃO TEVE MOVIMENTAÇÕES" if not extrato else extrato)
    print(f"Saldo atual:\tR$ {saldo:.2f}")
    print("==========================================")


# Função para criar um novo usuário
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF: @@@")
        return

    nome =input("Informe o seu nome completo: ")
    data_nascimento =input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("### Usuário criado com sucesso! ###")


# Função para filtrar usuarios na lista
def filtrar_usuario(cpf, usuarios):
    # Verifica se já existe algum usuário com o CPF informado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario # Retorna dicionário do usuario
    return None # CPF não encontrado, retorna None


# Função para criação de conta
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n### Conta criada com sucesso! ###")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None

# Função para listar contas existentes
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    AGENCIA = "0001"
    LIMITE_VALOR_SAQUE = 500
    LIMITE_SAQUES = 3

    saldo = 0
    extrato = ""
    contador_saque_diario = 0
    usuarios =[]
    contas = []
    
    while True:
        opcao = menu() # Chamando por funcao

        if opcao == "d":
            print("Deposito")
            valor_deposito = float(input("Informe o valor para depósito: "))
            saldo, extrato = depositar(saldo, valor_deposito, extrato)
        
        elif opcao == "s":
            print("Saque")
            valor_saque = float(input("Informe o valor do saque: "))
            saldo, extrato, contador_saque_diario = sacar(
                saldo=saldo, 
                valor=valor_saque,
                extrato=extrato,
                limite=LIMITE_VALOR_SAQUE,
                numeros_saques=contador_saque_diario,
                limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            # Forma diferente da criação usuario
            # Faz essa verificação para não armazenar na lista contas vazias pois o retorno da função se usuario for falso é none
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada.")

main()