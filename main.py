import flet as ft
from calculator import CalculatorApp

def main(page: ft.Page):
    page.title = "Calculator" #названия окна приложения
    page.window_resizable = False
    page.window_height = 800
    page.window_width = 600
    page.window_full_screen = False
    #создание экземляра кальулятора
    calc = CalculatorApp()
    
    # добавляем в окно калькулятор
    page.add(calc) 

ft.app(target = main)