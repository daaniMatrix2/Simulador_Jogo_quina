import tkinter as tk
from tkinter import ttk, messagebox
import random

# Valores de premiação padrão
DEFAULT_PREMIO_DUQUE = 2.50
DEFAULT_PREMIO_TERNO = 5.00
DEFAULT_PREMIO_QUADRA = 150.00
DEFAULT_PREMIO_QUINA = 50000.00

class SimuladorQuinaApp:
    def __init__(self, root):
        """Inicializa a aplicação da interface gráfica."""
        self.root = root
        self.root.title("Simulador de Jogos da Quina com Verificador")
        self.root.geometry("450x880")  # Largura x Altura (aumentada)
        self.root.resizable(False, False)

        self.jogos_gerados_lista = [] # Para armazenar os jogos como listas de inteiros
        # Estilo
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("TButton", font=("Helvetica", 11, "bold"))
        style.configure("Header.TLabel", font=("Helvetica", 12, "bold"))

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        # --- Seção de Entrada ---
        input_frame = ttk.LabelFrame(main_frame, text="Configuração", padding="10")
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Números base (ex: 1,2,3,4,5,6,7,8,9,10):").grid(row=0, column=0, columnspan=3, padx=5, pady=(10,0), sticky="w")
        self.entry_base_numeros = ttk.Entry(input_frame, width=40, font=("Helvetica", 11))
        self.entry_base_numeros.grid(row=1, column=0, columnspan=3, padx=5, pady=(0,10), sticky="ew")
        input_frame.grid_columnconfigure(0, weight=1) # Faz a coluna do entry expandir


        ttk.Label(input_frame, text="Quantidade de jogos:").grid(row=2, column=0, padx=5, pady=10, sticky="w")
        self.entry_num_jogos = ttk.Entry(input_frame, width=10, font=("Helvetica", 11))
        self.entry_num_jogos.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.generate_button = ttk.Button(input_frame, text="Gerar Jogos", command=self.gerar_jogos)
        self.generate_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

        # --- Seção de Sorteio (NOVO) ---
        sorteio_frame = ttk.LabelFrame(main_frame, text="Simular Sorteio", padding="10")
        sorteio_frame.pack(fill="x", pady=(10,0))

        ttk.Label(sorteio_frame, text="Números Sorteados (5 números, ex: 1,2,3,4,5):").grid(row=0, column=0, columnspan=2, padx=5, pady=(5,0), sticky="w")
        self.entry_numeros_sorteados = ttk.Entry(sorteio_frame, width=30, font=("Helvetica", 11), state="disabled")
        self.entry_numeros_sorteados.grid(row=1, column=0, padx=5, pady=(0,10), sticky="ew")

        self.verify_button = ttk.Button(sorteio_frame, text="Verificar Acertos", command=self.verificar_acertos, state="disabled")
        self.verify_button.grid(row=1, column=1, padx=10, pady=(0,10), sticky="e")
        sorteio_frame.grid_columnconfigure(0, weight=1) # Faz a coluna do entry expandir

        # --- Seção de Configuração de Prêmios (NOVO) ---
        premios_frame = ttk.LabelFrame(main_frame, text="Configuração de Prêmios (R$)", padding="10")
        premios_frame.pack(fill="x", pady=(10,0))

        ttk.Label(premios_frame, text="Duque:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_premio_duque = ttk.Entry(premios_frame, width=10, font=("Helvetica", 11))
        self.entry_premio_duque.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.entry_premio_duque.insert(0, f"{DEFAULT_PREMIO_DUQUE:.2f}")

        ttk.Label(premios_frame, text="Terno:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_premio_terno = ttk.Entry(premios_frame, width=10, font=("Helvetica", 11))
        self.entry_premio_terno.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        self.entry_premio_terno.insert(0, f"{DEFAULT_PREMIO_TERNO:.2f}")

        ttk.Label(premios_frame, text="Quadra:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_premio_quadra = ttk.Entry(premios_frame, width=10, font=("Helvetica", 11))
        self.entry_premio_quadra.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.entry_premio_quadra.insert(0, f"{DEFAULT_PREMIO_QUADRA:.2f}")

        ttk.Label(premios_frame, text="Quina:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_premio_quina = ttk.Entry(premios_frame, width=10, font=("Helvetica", 11))
        self.entry_premio_quina.grid(row=1, column=3, padx=5, pady=5, sticky="w")
        self.entry_premio_quina.insert(0, f"{DEFAULT_PREMIO_QUINA:.2f}")

        # --- Seção de Resultados ---
        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        results_frame.pack(fill="both", expand=True, pady=(10,0))


        self.label_preco = ttk.Label(results_frame, text="Preço Total: R$ 0.00", style="Header.TLabel")
        self.label_preco.pack(pady=(0, 10))

        # Área de texto para os jogos com barra de rolagem
        text_frame = ttk.Frame(results_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.text_jogos = tk.Text(
            text_frame, 
            wrap="word", 
            font=("Courier", 12), # Fonte monoespaçada para alinhamento
            height=10, # Ajustar altura conforme necessidade
            width=40
        )
        self.text_jogos.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_jogos.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.text_jogos.config(yscrollcommand=scrollbar.set, state="disabled")
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

        # --- Estatísticas de Acertos (NOVO) ---
        estatisticas_acertos_frame = ttk.Frame(results_frame)
        estatisticas_acertos_frame.pack(fill="x", pady=(10,0))

        self.label_quina = ttk.Label(estatisticas_acertos_frame, text="Quina: 0", font=("Helvetica", 10))
        self.label_quina.pack(side=tk.LEFT, padx=5)
        self.label_quadra = ttk.Label(estatisticas_acertos_frame, text="Quadra: 0", font=("Helvetica", 10))
        self.label_quadra.pack(side=tk.LEFT, padx=5)
        self.label_terno = ttk.Label(estatisticas_acertos_frame, text="Terno: 0", font=("Helvetica", 10))
        self.label_terno.pack(side=tk.LEFT, padx=5)
        self.label_duque = ttk.Label(estatisticas_acertos_frame, text="Duque: 0", font=("Helvetica", 10))
        self.label_duque.pack(side=tk.LEFT, padx=5)

        self.label_ganhos_totais = ttk.Label(results_frame, text="Ganhos Totais: R$ 0.00", style="Header.TLabel")
        self.label_ganhos_totais.pack(pady=(10, 0))


    def gerar_jogos(self):
        """Valida a entrada, calcula o preço e exibe os jogos gerados."""
        # Resetar estado da verificação
        self.jogos_gerados_lista.clear()
        self.entry_numeros_sorteados.config(state="disabled")
        self.entry_numeros_sorteados.delete(0, tk.END)
        self.verify_button.config(state="disabled")
        self._resetar_labels_estatisticas()

        try:
            num_jogos = int(self.entry_num_jogos.get())
            if num_jogos <= 0:
                messagebox.showerror("Erro", "Por favor, insira um número maior que zero.")
                return
        except ValueError:
            messagebox.showerror("Erro de Entrada", "Por favor, digite um número inteiro válido.")
            return

        base_numeros_str = self.entry_base_numeros.get()
        numeros_disponiveis = list(range(1, 81)) # Padrão Quina

        if base_numeros_str:
            try:
                base_numeros_list = [int(num.strip()) for num in base_numeros_str.split(',')]
                # Validação dos números base
                if not base_numeros_list: # Lista vazia após split de string vazia ou só com vírgulas
                    messagebox.showwarning("Aviso", "Nenhum número base fornecido. Usando o padrão de 1 a 80.")
                elif len(set(base_numeros_list)) < 5: # Usar set para contar únicos
                    messagebox.showerror("Erro nos Números Base", "Você deve fornecer pelo menos 5 números base únicos.")
                    return
                for num in base_numeros_list:
                    if not (1 <= num <= 80):
                        messagebox.showerror("Erro nos Números Base", f"O número {num} está fora do intervalo válido da Quina (1-80).")
                        return
                numeros_disponiveis = sorted(list(set(base_numeros_list))) # Remove duplicados e ordena
            except ValueError:
                messagebox.showerror("Erro nos Números Base", "Por favor, insira números base válidos separados por vírgula (ex: 1,5,10,23,45).")
                return

        # Preço atual de uma aposta simples da Quina
        preco_por_jogo = 2.50
        preco_total = num_jogos * preco_por_jogo

        # Atualiza o label do preço
        self.label_preco.config(text=f"Preço Total: R$ {preco_total:.2f}")

        # Limpa os resultados anteriores e gera os novos
        self.text_jogos.config(state="normal") # Habilita para edição
        self.text_jogos.delete("1.0", tk.END)
        
        jogos_para_exibir_texto = []
        for i in range(1, num_jogos + 1):
            if len(numeros_disponiveis) < 5:
                 messagebox.showerror("Erro", f"Não há números suficientes na lista base ({len(numeros_disponiveis)}) para gerar um jogo de 5 dezenas.")
                 self.text_jogos.config(state="disabled")
                 return
            jogo = sorted(random.sample(numeros_disponiveis, 5))
            self.jogos_gerados_lista.append(jogo) # Armazena o jogo (lista de int)
            # Formata os números para terem 2 dígitos (ex: 01, 05, 12)
            jogo_formatado = [f"{num:02d}" for num in jogo]
            linha_jogo = f"Jogo {i:02d}: {', '.join(jogo_formatado)}"
            jogos_para_exibir_texto.append(linha_jogo)

        self.text_jogos.insert(tk.END, "\n".join(jogos_para_exibir_texto))
        self.text_jogos.config(state="disabled") # Desabilita para o usuário não editar

        # Habilitar campos e botão de verificação se jogos foram gerados
        if self.jogos_gerados_lista:
            self.entry_numeros_sorteados.config(state="normal")
            self.verify_button.config(state="normal")

    def _resetar_labels_estatisticas(self):
        self.label_quina.config(text="Quina: 0")
        self.label_quadra.config(text="Quadra: 0")
        self.label_terno.config(text="Terno: 0")
        self.label_duque.config(text="Duque: 0")
        self.label_ganhos_totais.config(text="Ganhos Totais: R$ 0.00")

    def verificar_acertos(self):
        """Verifica os acertos dos jogos gerados com os números sorteados."""
        if not self.jogos_gerados_lista:
            messagebox.showinfo("Aviso", "Gere os jogos primeiro antes de verificar os acertos.")
            return

        numeros_sorteados_str = self.entry_numeros_sorteados.get()
        if not numeros_sorteados_str:
            messagebox.showerror("Erro", "Por favor, insira os 5 números sorteados.")
            return

        try:
            sorteados_lista_str = [s.strip() for s in numeros_sorteados_str.split(',')]
            if len(sorteados_lista_str) != 5:
                messagebox.showerror("Erro nos Números Sorteados", "Você deve inserir exatamente 5 números separados por vírgula.")
                return
            
            numeros_sorteados_validados = []
            for num_str in sorteados_lista_str:
                if not num_str: # Checa string vazia (ex: 1,2,,4,5)
                    messagebox.showerror("Erro nos Números Sorteados", "Número inválido ou faltando na lista de sorteados. Use vírgulas para separar.")
                    return
                num = int(num_str)
                if not (1 <= num <= 80):
                    messagebox.showerror("Erro nos Números Sorteados", f"O número {num} está fora do intervalo válido da Quina (1-80).")
                    return
                if num in numeros_sorteados_validados:
                     messagebox.showerror("Erro nos Números Sorteados", f"O número {num} está duplicado. Insira 5 números únicos.")
                     return
                numeros_sorteados_validados.append(num)
        except ValueError:
            messagebox.showerror("Erro nos Números Sorteados", "Por favor, insira 5 números válidos separados por vírgula (ex: 1,5,10,23,45).")
            return

        self._resetar_labels_estatisticas()
        cont_quina, cont_quadra, cont_terno, cont_duque = 0, 0, 0, 0
        ganhos_totais = 0.0
        
        # Ler valores de premiação dos campos de entrada ou usar padrão
        try:
            premio_duque_val = float(self.entry_premio_duque.get()) if self.entry_premio_duque.get() else DEFAULT_PREMIO_DUQUE
        except ValueError:
            premio_duque_val = DEFAULT_PREMIO_DUQUE
            messagebox.showwarning("Aviso de Prêmio", f"Valor inválido para Duque. Usando padrão: R${DEFAULT_PREMIO_DUQUE:.2f}")
        try:
            premio_terno_val = float(self.entry_premio_terno.get()) if self.entry_premio_terno.get() else DEFAULT_PREMIO_TERNO
        except ValueError:
            premio_terno_val = DEFAULT_PREMIO_TERNO
            messagebox.showwarning("Aviso de Prêmio", f"Valor inválido para Terno. Usando padrão: R${DEFAULT_PREMIO_TERNO:.2f}")
        try:
            premio_quadra_val = float(self.entry_premio_quadra.get()) if self.entry_premio_quadra.get() else DEFAULT_PREMIO_QUADRA
        except ValueError:
            premio_quadra_val = DEFAULT_PREMIO_QUADRA
            messagebox.showwarning("Aviso de Prêmio", f"Valor inválido para Quadra. Usando padrão: R${DEFAULT_PREMIO_QUADRA:.2f}")
        try:
            premio_quina_val = float(self.entry_premio_quina.get()) if self.entry_premio_quina.get() else DEFAULT_PREMIO_QUINA
        except ValueError:
            premio_quina_val = DEFAULT_PREMIO_QUINA
            messagebox.showwarning("Aviso de Prêmio", f"Valor inválido para Quina. Usando padrão: R${DEFAULT_PREMIO_QUINA:.2f}")
            
        self.text_jogos.config(state="normal")
        self.text_jogos.delete("1.0", tk.END)

        # Configuração de tags para destaque
        self.text_jogos.tag_configure("quina_linha", foreground="red", font=("Courier", 12))
        self.text_jogos.tag_configure("quadra_linha", foreground="blue", font=("Courier", 12))
        self.text_jogos.tag_configure("terno_linha", foreground="green", font=("Courier", 12))
        self.text_jogos.tag_configure("duque_linha", foreground="#B8860B", font=("Courier", 12)) # DarkGoldenrod
        self.text_jogos.tag_configure("normal_linha", foreground="black", font=("Courier", 12))
        self.text_jogos.tag_configure("numero_acertado", font=("Courier", 12, "bold"))

        for i, jogo_gerado_int_list in enumerate(self.jogos_gerados_lista):
            acertos = set(jogo_gerado_int_list) & set(numeros_sorteados_validados)
            num_acertos = len(acertos)
            
            tag_linha_atual, sufixo_acertos = "normal_linha", ""

            premio_jogo_atual = 0.0
            if num_acertos == 5:
                cont_quina += 1
                tag_linha_atual = "quina_linha"
                premio_jogo_atual = premio_quina_val
                sufixo_acertos = f" (QUINA! - R${premio_jogo_atual:.2f} - {sorted(list(acertos))})"
            elif num_acertos == 4:
                cont_quadra += 1
                tag_linha_atual = "quadra_linha"
                premio_jogo_atual = premio_quadra_val
                sufixo_acertos = f" (Quadra - R${premio_jogo_atual:.2f} - {sorted(list(acertos))})"
            elif num_acertos == 3:
                cont_terno += 1
                tag_linha_atual = "terno_linha"
                premio_jogo_atual = premio_terno_val
                sufixo_acertos = f" (Terno - R${premio_jogo_atual:.2f} - {sorted(list(acertos))})"
            elif num_acertos == 2:
                cont_duque += 1
                tag_linha_atual = "duque_linha"
                premio_jogo_atual = premio_duque_val
                sufixo_acertos = f" (Duque - R${premio_jogo_atual:.2f} - {sorted(list(acertos))})"
            
            ganhos_totais += premio_jogo_atual

            self.text_jogos.insert(tk.END, f"Jogo {i+1:02d}: ", tag_linha_atual)
            for k_idx, num_jogado in enumerate(jogo_gerado_int_list):
                num_jogado_str = f"{num_jogado:02d}"
                tags_num = (tag_linha_atual, "numero_acertado") if num_jogado in acertos else tag_linha_atual
                self.text_jogos.insert(tk.END, num_jogado_str, tags_num)
                if k_idx < len(jogo_gerado_int_list) - 1: self.text_jogos.insert(tk.END, ", ", tag_linha_atual)
            
            self.text_jogos.insert(tk.END, sufixo_acertos + "\n", (tag_linha_atual, "numero_acertado") if sufixo_acertos else tag_linha_atual)

        self.text_jogos.config(state="disabled")
        self.label_quina.config(text=f"Quina: {cont_quina}")
        self.label_quadra.config(text=f"Quadra: {cont_quadra}")
        self.label_terno.config(text=f"Terno: {cont_terno}")
        self.label_duque.config(text=f"Duque: {cont_duque}")
        self.label_ganhos_totais.config(text=f"Ganhos Totais: R$ {ganhos_totais:.2f}")

        if sum([cont_quina, cont_quadra, cont_terno, cont_duque]) == 0:
            messagebox.showinfo("Resultado da Verificação", "Nenhum jogo premiado (Duque ou superior) com os números sorteados.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorQuinaApp(root)
    root.mainloop()