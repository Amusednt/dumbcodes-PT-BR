# Importar as bibliotecas necessárias
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# Definir a classe do app
class NotaApp(App):
    # Método para construir a interface do app
    def build(self):
        # Criar um layout vertical
        layout = BoxLayout(orientation='vertical')
        
        # Criar um campo de texto para digitar a nota
        self.texto = TextInput(multiline=True, size_hint_y=0.8)
        
        # Criar um botão para salvar a nota
        btn_salvar = Button(text='Salvar')
        
        # Vincular o botão ao método para salvar a nota
        btn_salvar.bind(on_press=self.salvar_nota)
        
        # Adicionar os widgets ao layout
        layout.add_widget(self.texto)
        layout.add_widget(btn_salvar)
        
        # Retornar o layout
        return layout
    
    # Método para salvar a nota
    def salvar_nota(self, instance):
        # Aqui você implementaria a lógica para salvar a nota,
        # por exemplo, em um arquivo ou banco de dados.
        print(self.texto.text)

# Executar o app
if __name__ == '__main__':
    NotaApp().run()