#!/usr/bin/python

from Tkconstants import RIGHT, LEFT, RAISED, X, BOTTOM, TOP, END
from Tkinter import Tk, Frame, BOTH, Entry, BooleanVar, LabelFrame
import tkFileDialog
from ttk import Button, Style, Label, Combobox, Radiobutton
import alpha


class Example(Frame):
    input_method = ""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.init_gui()

    def init_gui(self):
        #Events
        def change_text_button():
            if encrypt.get():
                btn_encrypt.config(text="Criptografar")
            else:
                btn_encrypt.config(text="Descriptografar")

        def generate_key():
            directory = tkFileDialog.asksaveasfilename(defaultextension='.key')
            alpha.generate_random_key(16, directory)

        def set_input_key_method(event):
            self.input_method = event.widget.get()
            txt_chave.delete(0, END)
            if self.input_method == "Arquivo":
                txt_chave.insert(0, tkFileDialog.askopenfilename())

        def set_arquivo_entrada():
            txt_arquivo_entrada.delete(0, END)
            txt_arquivo_entrada.insert(0, tkFileDialog.askopenfilename())

        def set_arquivo_saida():
            txt_arquivo_saida.delete(0, END)
            txt_arquivo_saida.insert(0, tkFileDialog.asksaveasfilename())

        def run_alpha():
                key = alpha.read_file(txt_chave.get())
                alpha.encipher(txt_arquivo_entrada.get(), key, 16, 16, encrypt.get(), txt_arquivo_saida.get())

        self.parent.title("Alpha Cipher")
        self.style = Style()
        self.style.theme_use("default")

        frame_radio = Frame(self, border=1)
        frame_radio.pack(fill=X, expand=1, side=TOP)
        encrypt = BooleanVar()
        rad_encrypt = Radiobutton(frame_radio, text="Criptografar", variable=encrypt, value=True, command=change_text_button)
        rad_encrypt.pack(fill=BOTH, expand=1, side=RIGHT)
        rad_decrypt = Radiobutton(frame_radio, text="Descriptografar", variable=encrypt, value=False, command=change_text_button)
        rad_decrypt.pack(fill=BOTH, expand=1, side=RIGHT)

        btn_gerar_chave = Button(self, text="Gerar Chave", command=generate_key)
        btn_gerar_chave.pack(fill=X, expand=1)

        frame_label = Frame(self, border=1)
        frame_label.pack(fill=X, expand=1, side=TOP)
        lbl_metodo = Label(frame_label, text="Metodo de entrada da chave:")
        lbl_metodo.pack(fill=BOTH, expand=1, side=LEFT)
        cbo_entrada = Combobox(frame_label, state='readonly', values=['Decimal', 'Hexadecimal', 'Arquivo'])
        cbo_entrada.bind('<<ComboboxSelected>>', set_input_key_method)
        cbo_entrada.current(1)
        cbo_entrada.pack(fill=BOTH, expand=1, side=RIGHT)
        txt_chave = Entry(self)
        txt_chave.pack(fill=X, expand=1)

        frame_entrada = LabelFrame(self, text="Arquivo de Entrada")
        frame_entrada.pack(fill=BOTH, expand=1, side=TOP)
        txt_arquivo_entrada = Entry(frame_entrada)
        txt_arquivo_entrada.pack(fill=X, expand=1, side=LEFT)
        btn_arquivo_entrada = Button(frame_entrada, text="Pesquisar", width=9, command=set_arquivo_entrada)
        btn_arquivo_entrada.pack(fill=X, expand=0, side=RIGHT)

        frame_saida = LabelFrame(self, text="Arquivo de Saida")
        frame_saida.pack(fill=BOTH, expand=1, side=TOP)
        txt_arquivo_saida = Entry(frame_saida)
        txt_arquivo_saida.pack(fill=X, expand=1, side=LEFT)
        btn_arquivo_saida = Button(frame_saida, text="Pesquisar", width=9, command=set_arquivo_saida)
        btn_arquivo_saida.pack(fill=X, expand=0, side=RIGHT)

        btn_encrypt = Button(self, text="Descriptografar", command=run_alpha)
        btn_encrypt.pack(fill=X, expand=1)

        self.pack(fill=X, expand=1)



    def center_window(self):
        w = 290
        h = 200
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():

    root = Tk()
    app = Example(root)
    app.center_window()
    root.mainloop()


if __name__ == '__main__':
    main()

