# módulo para formatação de texto eficiente
import textwrap

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

def main():
    saldo = 0
    LIMITE_VALOR_SAQUE = 500
    extrato = ""
    contador_saque_diario = 0
    LIMITE_SAQUES = 3
    
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
            print("\n********** EXTRATO **********")
            print("NÃO TEVE MOVIMENTAÇÕES" if not extrato else extrato)
            print(f"Saldo atual R$ {saldo:.2f}")
            print("*****************************")

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione a operação desejada.")

main()