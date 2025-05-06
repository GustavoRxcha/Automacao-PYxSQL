from tkinter import Button

fundo = '#f9fafb'
cor_texto = '#1f2937'
botao1 = '#6366f1'
botao2 = '#a5b4fc'
hover = '#7c3aed'
borda = '#d1d5db'
tags = '#6366f1'
vermelho = '#f87171'
verde = '#10b981'

def aplicar_hover(botao, cor_hover, cor_normal):
    botao.bind("<Enter>", lambda e: e.widget.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: e.widget.config(bg=cor_normal))

def aplicar_hover_em_todos(frame, cor_hover, cor_original):
    for widget in frame.winfo_children():
        if isinstance(widget, Button):
            widget.bind("<Enter>", lambda e, c=cor_hover: e.widget.config(bg=c))
            widget.bind("<Leave>", lambda e, c=cor_original: e.widget.config(bg=c))