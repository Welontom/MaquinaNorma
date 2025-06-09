class MaquinaNorma:
    def __init__(self):
        self.registradores = {r: 0 for r in 'ABCDEFGH'}
        self.programa = []
        self.linha_atual = 0

    def set_registradores(self, valores_iniciais):
        for reg, val in valores_iniciais.items():
            if reg in self.registradores:
                self.registradores[reg] = val

    def carregar_programa(self, caminho_arquivo):
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                linha = linha.strip()
                if linha:
                    numero, instrucao = linha.split(":", 1)
                    self.programa.append((int(numero.strip()), instrucao.strip()))

    def executar(self):
        while self.linha_atual < len(self.programa):
            numero_linha, instrucao = self.programa[self.linha_atual]
            proxima_linha = self.executar_instrucao(instrucao)
            if proxima_linha is None:
                self.linha_atual += 1
            else:
                indices = [i for i, (num, _) in enumerate(self.programa) if num == proxima_linha]
                if indices:
                    self.linha_atual = indices[0]
                    
                else:
                    print(f"Linha {proxima_linha} não encontrada. Encerrando execução.")
                    break

    def executar_instrucao(self, instrucao):

        comando = instrucao[:3]
        reg = instrucao[3]       
        goto = instrucao[4:6] 
        
        print(instrucao)
        print("Estado atual dos registradores:")
        for k, v in self.registradores.items():
            print(f"{k}: {v}")

        if (comando not in {"ADD", "SUB", "ZER"} or reg not in self.registradores):
            print(f"Instrução inválida: {instrucao}")
            return None

        if comando == "ADD":
            self.registradores[reg] += 1
            return int(goto) 

        elif comando == "SUB":
            if self.registradores[reg] > 0:
                self.registradores[reg] -= 1
                return int(goto) 
            else:
                return None

        elif comando == "ZER":
            desvio = instrucao[6:]
            if self.registradores[reg] == 0:
                return int(goto) 
            else:
                return int(desvio)

    def imprimir_registradores(self):
        print("Estado atual dos registradores:")
        for k, v in self.registradores.items():
            print(f"{k}: {v}")


# Exemplo de uso
if __name__ == "__main__":
    maquina = MaquinaNorma()
    maquina.set_registradores({'A': 6, 'B':2})
    maquina.carregar_programa('programas/mod.txt')
    maquina.executar()
    maquina.imprimir_registradores()