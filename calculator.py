import math
import flet as ft
from flet import (
    Column,
    Container,
    ElevatedButton,
    Page,
    Row,
    Text,
    UserControl,
    border_radius,
    colors,
    alignment,
    MainAxisAlignment,
    MaterialState,
    RoundedRectangleBorder,
    StadiumBorder,
    BorderSide,
    ButtonStyle,
    Dropdown
)

#класс калькулятор
class CalculatorApp(UserControl):

    num1 = 0.0 #первое числовое значение
    num2 = 0.0 #второе числовое значение
    operator = "" #сохраняет последнйи математический оператор
    flag_in = False #флаг ввода нового числа
    eq_last = False #флаг послднего нажатия кнопки "="
    flag_dot = False #флаг поставленной точки
    flag_result = False #флаг результата, выведенное число является результатом
    flag_dd_change = False #изменение СИ или режима
    flag_dist = False #включение режима калькулятора расстояния
    flag_time = False #включение режима калькулятора времени
    dist1 = "" #сохраняет первое расстояние
    dist2 = "" #сохраняет второе расстояние
    time1 = "" #сохраняет первое время
    time2 = "" #сохраняет второе время
    hints_save = "" #сохраняет вывод подсказки
    b_undis_list = [] #списоок активных кнопок
    b_dis_list = [] #списоок неактивных кнопок
    b_list = [] #списоок кнопок
    sup_index_list = ['\u2082', '\u2083', '\u2084', '\u2085', '\u2086', '\u2087', '\u2088', '\u2089', '\u2081\u2080', '\u2081\u2081', '\u2081\u2082', '\u2081\u2083', '\u2081\u2084', '\u2081\u2085', '\u2081\u2086']#список подстрочных индексов для сонований СИ

    def build(self):
        #настройка внешнего вида содержимого
        self.hints = Text(value = "", color=colors.BLACK, size=15)

        self.result = Text(value="0", color=colors.BLACK, size=40)

        self.dd = Dropdown(
                    label = "Основание",
                    width = 125,
                    height = 100,
                    border_radius = 20,
                    border_width = 2,
                    options = [
                        ft.dropdown.Option("2"),
                        ft.dropdown.Option("3"),
                        ft.dropdown.Option("4"),
                        ft.dropdown.Option("5"),
                        ft.dropdown.Option("6"),
                        ft.dropdown.Option("7"),
                        ft.dropdown.Option("8"),
                        ft.dropdown.Option("9"),
                        ft.dropdown.Option("10"),
                        ft.dropdown.Option("11"),
                        ft.dropdown.Option("12"),
                        ft.dropdown.Option("13"),
                        ft.dropdown.Option("14"),
                        ft.dropdown.Option("15"),
                        ft.dropdown.Option("16"),
                        ft.dropdown.Option("Расстояние"),
                        ft.dropdown.Option("Время")
                    ],
                    value = "10",
                    border_color = colors.DEEP_PURPLE_400,
                    focused_border_color = colors.DEEP_PURPLE_400,
                    on_change = self.dd_changed
                )
        
        #кнопки чисел, +/- и точки
        b_0 = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "0", color = colors.BLACK, size = 30)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ),                         
                                bgcolor=colors.WHITE,
                                expand=1,
                                height = 65,
                                style = ButtonStyle( shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) }),
                                data = "0",
                                on_click = self.button_clicked_num
                            )
        b_1 = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "1", color = colors.BLACK, size = 30)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                ),                         
                                bgcolor=colors.WHITE,
                                expand=1,
                                height = 65,
                                style = ButtonStyle( shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) }),
                                data = "1",
                                on_click = self.button_clicked_num
                            )

        for i in range(14):
            self.b_undis_list.append(
                Container(
                    expand = True,
                    content = Column (
                        controls = [
                            ElevatedButton (
                                content = Container (
                                    content = Column(
                                        controls = [Text(value = self.num_to_letter(i + 2), color = colors.BLACK, size = 30)],
                                        alignment = ft.MainAxisAlignment.CENTER
                                    )
                                ),
                                bgcolor = {
                                    MaterialState.DEFAULT: colors.WHITE,
                                    MaterialState.DISABLED: colors.WHITE12
                                },
                                expand = True,
                                width = 100,
                                style = ButtonStyle (
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2)},
                                    side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                                    shadow_color = { MaterialState.DISABLED: colors.BLACK },
                                    surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                                ),
                                data = self.num_to_letter(i + 2),
                                on_click = self.button_clicked_num,
                                disabled = False
                            )
                        ]
                    )
                )
            )

            self.b_dis_list.append(
                Container(
                    expand = True,
                    content = Column (
                        controls = [
                            ElevatedButton (
                                content = Container (
                                    content = Column(
                                        controls = [Text(self.num_to_letter(i + 2), color = colors.BLACK, size = 30)],
                                        alignment = ft.MainAxisAlignment.CENTER
                                    )
                                ),
                                bgcolor = {
                                    MaterialState.DEFAULT: colors.WHITE,
                                    MaterialState.DISABLED: colors.WHITE12
                                },
                                expand = True,
                                width = 100,
                                style = ButtonStyle (
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2)},
                                    side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                                    shadow_color = { MaterialState.DISABLED: colors.BLACK },
                                    surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                                ),
                                data = self.num_to_letter(i + 2),
                                on_click = self.button_clicked_num,
                                disabled = True
                            )
                        ]
                    )
                )
            )

            if i < 8:
                self.b_list.append(
                    ft.AnimatedSwitcher(
                        self.b_undis_list[i],
                        duration=0,
                        reverse_duration=0
                    )
                )
            else:
                self.b_list.append(
                    ft.AnimatedSwitcher(
                        self.b_dis_list[i],
                        duration=0,
                        reverse_duration=0
                    )
                )                      

        self.b_dot_undis = Container (
            expand = True,
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = ".", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.WHITE,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "dot", 
                        on_click = self.button_clicked_num,
                        disabled = False
                    )
                ]
            )
        )
        self.b_dot_dis = Container (
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = ".", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.WHITE,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "dot",
                        on_click = self.button_clicked_num,
                        disabled = True
                    )
                ]
            )
        )
        self.b_dot = ft.AnimatedSwitcher(
            self.b_dot_undis,
            duration=0,
            reverse_duration=0
        )
        self.b_plus_minus_undis = Container (
            expand = True,
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "+/-", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.WHITE,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "+/-", 
                        on_click = self.button_clicked_num,
                        disabled = False
                    )
                ]
            )
        )
        self.b_plus_minus_dis = Container (
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "+/-", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.WHITE,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "+/-",
                        on_click = self.button_clicked_num,
                        disabled = True
                    )
                ]
            )
        )
        self.b_plus_minus = ft.AnimatedSwitcher(
            self.b_plus_minus_undis,
            duration=0,
            reverse_duration=0
        )

        #кнопки математических обозначений
        b_eq = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "=", color = colors.WHITE, size = 45)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding = ft.padding.only(top = -10)
                                ),                         
                                bgcolor=colors.ORANGE,
                                expand=1,
                                height = 65,
                                style = ButtonStyle( StadiumBorder() ),
                                data = "=",
                                on_click = self.button_clicked_operation
                            )
        b_plus = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "+", color = colors.BLACK, size = 45)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding = ft.padding.only(top = -10)
                                ),                         
                                expand=1,
                                height = 65,
                                style = ButtonStyle( 
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                                    bgcolor = {
                                        MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                        MaterialState.PRESSED: colors.DEEP_ORANGE_100
                                    }),
                                data = "+",
                                on_click = self.button_clicked_operation
                            )            
        b_minus = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "-", color = colors.BLACK, size = 45)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    ),
                                    padding = ft.padding.only(top = -10)
                                ),                         
                                expand=1,
                                height = 65,
                                style = ButtonStyle( 
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                                    bgcolor = {
                                        MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                        MaterialState.PRESSED: colors.DEEP_ORANGE_100
                                    }),
                                data = "-",
                                on_click = self.button_clicked_operation
                            )
        self.b_multi_undis = Container (
            expand = True,
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "×", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "*", 
                        on_click = self.button_clicked_operation,
                        disabled = False
                    )
                ]
            )
        )
        self.b_multi_dis = Container (
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "×", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "*",
                        on_click = self.button_clicked_operation,
                        disabled = True
                    )
                ]
            )
        )
        self.b_multi = ft.AnimatedSwitcher(
            self.b_multi_undis,
            duration=0,
            reverse_duration=0
        )
        self.b_div = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "÷", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "/",
                        on_click = self.button_clicked_operation
                    )
                ]
            )
        )
        self.b_proc_undis = Container (
            expand = True,
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "%", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "%", 
                        on_click = self.button_clicked_operation,
                        disabled = False
                    )
                ]
            )
        )
        self.b_proc_dis = Container (
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "%", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "%",
                        on_click = self.button_clicked_operation,
                        disabled = True
                    )
                ]
            )
        )
        self.b_proc = ft.AnimatedSwitcher(
            self.b_proc_undis,
            duration=0,
            reverse_duration=0
        )
        self.b_rev_undis = Container (
            expand = True,
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "1/x", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "1/x", 
                        on_click = self.button_clicked_operation,
                        disabled = False
                    )
                ]
            )
        )
        self.b_rev_dis = Container (
            content = Column (
                controls = [
                    ElevatedButton (
                        content = Container (
                            content = Column (
                                controls = [Text(value = "1/x", color = colors.BLACK, size = 30)],
                                alignment = ft.MainAxisAlignment.CENTER
                            )
                        ),
                        bgcolor= { 
                            MaterialState.DEFAULT: colors.BLUE_GREY_100,
                            MaterialState.DISABLED: colors.WHITE12
                            },
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2) },
                            side = { MaterialState.DISABLED: BorderSide(1, colors.BLUE_GREY_200)},
                            shadow_color = { MaterialState.DISABLED: colors.BLACK },
                            surface_tint_color = {  MaterialState.DISABLED: colors.BLACK }
                            ),
                        data = "1/x",
                        on_click = self.button_clicked_operation,
                        disabled = True
                    )
                ]
            )
        )
        self.b_to_secodn_power = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "x^y", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "^",
                        on_click = self.button_clicked_operation
                    )
                ]
            )
        )
        self.b_square_root = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "√x", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "root",
                        on_click = self.button_clicked_operation
                    )
                ]
            )
        )

        b_CE = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "CE", color = colors.BLACK, size = 30)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),                         
                                expand=1,
                                height = 65,
                                style = ButtonStyle( 
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                                    bgcolor = {
                                        MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                        MaterialState.PRESSED: colors.DEEP_ORANGE_100
                                    }),
                                data = "CE",
                                on_click = self.button_clicked_del
                            )
        b_C = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "C", color = colors.BLACK, size = 30)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),                         
                                expand=1,
                                height = 65,
                                style = ButtonStyle( 
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                                    bgcolor = {
                                        MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                        MaterialState.PRESSED: colors.DEEP_ORANGE_100
                                    }),
                                data = "del_all",
                                on_click = self.button_clicked_del
                            )
        b_del = ElevatedButton(
                                content = Container (
                                    content = Column (
                                        controls = [Text(value = "⌫", color = colors.BLACK, size = 30)],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                    )
                                ),                         
                                expand=1,
                                height = 65,
                                style = ButtonStyle( 
                                    shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                                    bgcolor = {
                                        MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                        MaterialState.PRESSED: colors.DEEP_ORANGE_100
                                    },
                                    elevation={"pressed": 0, "": 1},
                                    animation_duration = 1500,
                                ),
                                data = "del",
                                on_click = self.button_clicked_del
                            )

        #кнопки единиц расстояния
        self.b_km = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "km", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "km",
                        on_click = self.button_clicked_dist
                    )
                ]
            )
        )
        self.b_m = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "m", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "m",
                        on_click = self.button_clicked_dist
                    )
                ]
            )
        )
        self.b_cm = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "cm", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "cm",
                        on_click = self.button_clicked_dist
                    )
                ]
            )
        )
        self.b_mm = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "mm", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "mm",
                        on_click = self.button_clicked_dist
                    )
                ]
            )
        )

        #кнопки единиц времени
        self.b_d = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "d", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "d",
                        on_click = self.button_clicked_time
                    )
                ]
            )
        )
        self.b_h = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "h", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "h",
                        on_click = self.button_clicked_time
                    )
                ]
            )
        )
        self.b_min = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "min", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "min",
                        on_click = self.button_clicked_time
                    )
                ]
            )
        )
        self.b_s = Container (
            content = Column (
                controls = [
                    ElevatedButton(
                        content = Container (
                            content = Column (
                                controls = [Text(value = "s", color = colors.BLACK, size = 30)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            )
                        ),                         
                        expand=True,
                        width = 100,
                        style = ButtonStyle( 
                            shape = { MaterialState.DEFAULT: RoundedRectangleBorder(radius = 2),},
                            bgcolor = {
                                MaterialState.DEFAULT: colors.BLUE_GREY_100,
                                MaterialState.PRESSED: colors.DEEP_ORANGE_100
                            }
                        ),
                        data = "s",
                        on_click = self.button_clicked_time
                    )
                ]
            )
        )

        self.b_div_mm_s = ft.AnimatedSwitcher(
            self.b_div,
            duration=0,
            reverse_duration=0
        )
        self.b_square_root_cm_min = ft.AnimatedSwitcher(
            self.b_square_root,
            duration=0,
            reverse_duration=0
        )
        self.b_to_secodn_power_m_h = ft.AnimatedSwitcher(
            self.b_to_secodn_power,
            duration=0,
            reverse_duration=0
        )
        self.b_rev_km_d = ft.AnimatedSwitcher(
            self.b_rev_undis,
            duration=0,
            reverse_duration=0
        )

        # элемент в котором находятся все кнопки и текстовое поле,расположенные в 5 рядов
        # используется для удобного расположения и настройки. также может быть родителем
        return Container(
            bgcolor=colors.BLUE_GREY_100,
            border_radius=border_radius.all((7)),
            padding=20,
            content=Column(
                spacing = 15,
                height = 700,
                width = 600,
                expand = True,
                controls=[
                    Row(controls=[self.hints], alignment="end", expand = 9),

                    Row(controls=[self.result], alignment="end", expand = 9),

                    Row(
                        alignment = "left",
                        width = 500,
                        expand = 9,
                        controls = [self.dd]
                    ),

                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[8], expand = 5), Container(self.b_proc, expand = 5), Container(b_CE, expand = 5), Container(b_C, expand = 5), Container(b_del, expand = 5)]
                    ),

                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[9], expand = 5), Container(self.b_rev_km_d, expand = 5), Container(self.b_to_secodn_power_m_h, expand = 5), Container(self.b_square_root_cm_min, expand = 5), Container(self.b_div_mm_s, expand = 5)]
                    ),

                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[10], expand = 5), Container(self.b_list[5], expand = 5), Container(self.b_list[6], expand = 5), Container(self.b_list[7], expand = 5), Container(self.b_multi, expand = 5)]
                    ),

                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[11], expand = 5), Container(self.b_list[2], expand = 5), Container(self.b_list[3], expand = 5),  Container(self.b_list[4], expand = 5), Container(b_minus, expand = 5)]
                    ),
                    
                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[12], expand = 5), Container(b_1, expand = 5), Container(self.b_list[0], expand = 5), Container(self.b_list[1], expand = 5), Container(b_plus, expand = 5)]
                    ),

                    Row(
                        expand = 9,
                        controls=[Container(self.b_list[13], expand = 5), Container(self.b_plus_minus, expand = 5), Container(b_0, expand = 5), Container(self.b_dot, expand = 5), Container(b_eq, expand = 5)]
                    ),
                ]
            ),
        )

    #Действие при нажатии на кнопку цифры и +/- и точки
    def button_clicked_num(self, e):
        data = e.control.data

        #Вывод цифр и +/- и точки на экран
        if (self.flag_dist == False and self.flag_time == False) or (self.flag_dist == True and ((self.is_m(self.result.value) == -1) or (self.result.value.find("mm ") == -1) or (self.result.value.find("km ") == -1) or (self.result.value.find("cm ") == -1))) or (self.flag_in == True) or (self.flag_time == True and ((self.result.value.find("d ") == -1) or (self.result.value.find("h ") == -1) or (self.result.value.find("min ") == -1) or (self.result.value.find("s ") == -1))):
            self.flag_dd_change = False
            if self.hints.value.find("Введите число") != -1 or self.hints.value.find("уже использованы") != -1 or self.hints.value.find("Не правильный формат данных") != -1:
                self.hints.value = self.hints_save

            if data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"):
                if (self.result.value == "0") or (self.flag_in == True) or (self.result.value == "Error"):
                    self.result.value = data
                    self.flag_in = False
                else:
                    self.result.value += data
            elif data == "+/-":
                if float(self.result.value) > 0:
                    self.result.value = "-" + self.result.value
                else:
                    self.result.value = str(self.num_format(self.result.value))
            elif (data == "dot") and (self.flag_dot == False):
                if (self.flag_in == False):
                    self.result.value += "."
                else:
                    self.result.value = "0."
                    self.flag_in = False
                self.flag_dot = True
        else:
            if self.flag_dist == True:
                self.hints.value = "Все допустимые меры длины использованы"
            elif self.flag_dist == True:
                self.hints.value = "Все допустимые меры времени использованы"

        self.update()

    #Действия кнопок удаления
    def button_clicked_del(self, e):
        if self.result.value == "Error":
            self.reset()
        else:
            data = e.control.data

            if (data == "del_all" or self.flag_result == True) and data != "CE":
                self.reset()
            elif data == "del":
                self.result.value = self.del_last(self.result.value)
            elif data == "CE" or flag_in == True:
                self.result.value = "0"
                self.flag_result = False

        flag_dd_change = False       

        if self.hints.value.find("Введите число") != -1 or self.hints.value.find("уже использованы") != -1 or self.hints.value.find("Не правильный формат данных") != -1:
            self.hints.value = self.hints_save

            
        self.update()

    #сбросить все вычисления
    def reset(self):
        self.result.value = "0"
        self.hints.value = ""
        self.num1 = 0.0
        self.num2 = 0.0
        self.operator = ""
        self.flag_in = False
        self.eq_last = False
        self.flag_dot = False
        self.flag_result = False
        self.dist1 = ""
        self.dist2 = ""
        self.time1 = ""
        self.time2 = ""
        self.hints_save = ""


    #удаление цифры справа
    def del_last(self, string):
        c = ""
        if len(string) == 1:
            c += "0"
        else:
            if self.flag_dist == False and self.flag_time == False:
                c += string[:-1]
            elif self.flag_dist == True:
                if self.is_m(string[-3:]) != -1:
                    c += string[:-2]
                elif string[-2] == "m":
                    c += string[:-3]
                else:
                    c += string[:-1]
            elif self.flag_time == True:
                if string[-2] == "d":
                    c += string[:-2]
                elif string[-2] == "h":
                    c += string[:-2]
                elif string[-2] == "n":
                    c += string[:-4]
                elif string[-2] == "s":
                    c += string[:-2]
                else:
                    c += string[:-1]
                    
        return c

    #Действия кнопок математических операций
    def button_clicked_operation(self, e):
        if self.hints.value.find("Введите число") != -1 or self.hints.value.find("уже использованы") != -1 or self.hints.value.find("Не правильный формат данных") != -1:
            self.hints.value = self.hints_save

        data = e.control.data

        if self.flag_time == True:
            if self.result.value.rfind("d ") == len(self.result.value) - 2 or self.result.value.rfind("h ") == len(self.result.value) - 2 or self.result.value.rfind("n ") == len(self.result.value) - 2 or self.result.value.rfind("s ") == len(self.result.value) - 2 or self.result.value.rfind("w ") == len(self.result.value) - 2:
                if data == "=" and self.operator != "":
                    self.flag_result = True
                    self.hints_out(data, self.to_norm_time(self.result.value))
                    self.eq()
                    self.eq_last = True
                elif self.operator == "" or self.eq_last == True:
                    self.eq_last = False
                    self.time1 = self.to_norm_time(self.result.value)
                    self.operator = data
                    self.hints_out(data, self.to_norm_time(self.result.value))
                else:
                    self.eq_last = False
                    self.eq()
                    self.operator = data
                    self.flag_result = True
                    self.hints_out(data, self.to_norm_time(self.result.value))

                self.flag_in = True
            else:
                self.hints_save = self.hints.value
                self.hints.value = "Не правильный формат данных"
                self.update()
        elif self.flag_dist == True:
            if self.result.value.rfind("m ") == len(self.result.value) - 2:
                if data == "=" and self.operator != "":
                    self.flag_result = True
                    self.hints_out(data, self.to_norm_dist(self.to_norm_dist(self.result.value)))
                    self.eq()
                    self.eq_last = True
                elif self.operator == "" or self.eq_last == True:
                    self.eq_last = False
                    self.dist1 = self.to_norm_dist(self.to_norm_dist(self.result.value))
                    self.operator = data
                    self.hints_out(data, self.to_norm_dist(self.to_norm_dist(self.result.value)))
                else:
                    self.eq_last = False
                    self.eq()
                    self.operator = data
                    self.flag_result = True
                    self.hints_out(data, self.to_norm_dist(self.to_norm_dist((self.result.value))))

                self.flag_in = True
            else:
                self.hints_save = self.hints.value
                self.hints.value = "Не правильный формат данных"
                self.update()
        else:
            if self.result.value == "Error":
                self.result.value = "0"
            else:
                if data == "=":
                    if self.operator != "":
                        self.flag_result = True
                        self.hints_out(data, self.result.value)
                        self.eq()
                        self.eq_last = True
                elif data in ("+", "-", "*", "/", "^"):
                    if self.operator == "" or (self.eq_last == True):
                        self.hints_out(data, self.result.value)
                        if self.operator == "":
                            self.num1 = self.to_10(self.dd.value)
                        elif self.flag_result == True:
                            self.num1 = self.to_10("10")
                        self.operator = data
                        self.flag_in = True
                        self.eq_last = False
                        self.flag_dot = False
                    elif self.operator != "" and self.flag_result == False and self.flag_in == True: #если пользователь меняет операции в начале пользования калькулятором
                        self.hints_out(data, self.result.value)
                        self.operator = data
                    else:
                        self.eq_last = False
                        self.eq()
                        self.hints_out(data, self.result.value)
                        self.operator = data
                        self.flag_dot = False
                        self.flag_result = True
                elif data in ("1/x", "root"):
                    self.hints_out(data, self.result.value)
                    self.operator = data
                    if self.flag_result == True:
                        self.num1 = self.to_10("10")
                    else:
                        self.num1 = self.to_10(self.dd.value)
                    self.eq()
                    self.flag_result = True
                elif data == "%":
                    if self.operator in ("", "1/x", "root") or self.eq_last == True:
                        self.result.value = str(self.calculate(self.to_10(self.dd.value), 1, data))
                    elif self.operator in ("+", "-", "*", "/", "^"):
                        self.result.value = str(self.calculate(self.num1, self.to_10(self.dd.value), data))
                
            self.flag_dd_change = False

        self.update()

    #вывод подсказки последнего действия
    def hints_out(self, data, num):
        if self.flag_dist == False and self.flag_time == False:
            if self.flag_dd_change == True or self.eq_last == True:
                main_substring = str(self.num_format(num)) + self.sup_index_list[8] + " " + data
            else:
                main_substring = self.result.value + self.sup_index_list[int(self.dd.value) - 2]
            
            if data == "=":
                if self.eq_last == False and self.operator == "":
                    self.hints.value += main_substring + " " + data + " "
                elif self.eq_last == False and self.operator != "":
                    self.hints.value += main_substring + " " + data + " "
                else:
                    if self.operator == "1/x":
                        self.hints.value = "1/" + str(self.num_format(num)) + self.sup_index_list[8] + " " + data 
                    elif self.operator == "root":
                        self.hints.value = "sqrt(" + str(self.num_format(num)) + self.sup_index_list[8] +  ")" + " " + data 
                    elif self.operator != "":    
                        self.hints.value = str(self.num_format(num)) + self.sup_index_list[8] + " " + self.operator + " " + str(self.num_format(str(self.num2))) + self.sup_index_list[8] +  " " + data
            elif data in ("+", "-", "*", "/", "^"):
                if self.operator in ("1/x", "root", "%"):
                    self.hints.value = main_substring + " " + data
                elif self.flag_dd_change == True or self.flag_result == True:
                    self.hints.value = main_substring
                elif self.operator == "" or (self.eq_last == True):
                    self.hints.value = main_substring + " " + data + " "
                elif self.operator in ("+", "-", "*", "/", "^"):
                    self.hints.value = main_substring + " " + data + " "
            elif data in ("%", "1/x", "root"):
                if data == "1/x":
                    self.hints.value = "1/" + main_substring.replace(data, "")  + " ="
                elif data == "root":
                    self.hints.value = "sqrt(" + main_substring.replace(data, "")  + ")" + " ="
            else:
                self.hints.value = main_substring
        elif self.flag_dist == True:
            if self.eq_last == True:
                self.hints.value = self.zero_del(num) + " " + self.operator + " " + self.zero_del(self.dist2) + " " + data
            elif data == "=":
                self.hints.value = self.zero_del(self.dist1) + " " + self.operator + " " + self.zero_del(num) + " " + data
            else:
                self.hints.value = self.zero_del(num) + " " + data
        elif self.flag_time == True:
            if self.eq_last == True:
                #self.hints.value = self.zero_del(num) + " " + self.operator + " " + self.zero_del(self.time2) + " " + data
                self.hints.value = num + " " + self.operator + " " + self.time2 + " " + data
            elif data == "=":
                #self.hints.value = self.zero_del(self.time1) + " " + self.operator + " " + self.zero_del(num) + " " + data
                self.hints.value = self.time1 + " " + self.operator + " " + num + " " + data
            else:
                #self.hints.value = self.zero_del(num) + " " + data
                self.hints.value = num + " " + data

    #вывод результата
    def eq(self):
        if self.flag_time == True:
            if self.eq_last == False:
                self.time2 = self.to_norm_time(self.result.value)
            #self.result.value = str(self.zero_del(self.calculate(self.time1, self.time2, self.operator)))
            self.result.value = str(self.calculate(self.time1, self.time2, self.operator))

            self.time1 = self.to_norm_time(self.result.value)
        elif self.flag_dist == True:
            if self.eq_last == False:
                self.dist2 = self.to_norm_dist(self.to_norm_dist(self.result.value))
            self.result.value = str(self.zero_del(self.calculate(self.dist1, self.dist2, self.operator)))

            self.dist1 = self.to_norm_dist(self.to_norm_dist(self.result.value))
        else:
            if self.eq_last == False:
                self.num2 = self.to_10(self.dd.value)
            self.result.value = str(self.calculate(self.num1, self.num2, self.operator))

            if self.result.value != "Error":
                self.num1 = self.to_10("10")
            self.flag_dot = False

        self.flag_in = True

    #мат. действия
    def calculate(self, operand1, operand2, operator):
        if self.flag_time == True:
            if operator == "+":
                index_1_s = operand1.rfind("s ")
                index_2_s = operand2.rfind("s ")
                index_1_min = operand1.rfind("min ", 0, index_1_s)
                index_2_min = operand2.rfind("min ", 0, index_2_s)
                s = str(int(operand1[index_1_min + 4:index_1_s]) + int(operand2[index_2_min + 4:index_2_s])) + "s"

                index_1_h = operand1.rfind("h ", 0, index_1_min)
                index_2_h = operand2.rfind("h ", 0, index_2_min)
                min = str(int(operand1[index_1_h + 2:index_1_min]) + int(operand2[index_2_h + 2:index_2_min])) + "min"

                #index_1_d = operand1.rfind("d ", 0, index_1_h)
                #index_2_d = operand2.rfind("d ", 0, index_2_h)
                #h = str(int(operand1[index_1_d + 2:index_1_h]) + int(operand2[index_2_d + 2:index_2_h])) + "h"
                h = str(int(operand1[:index_1_h]) + int(operand2[:index_2_h])) + "h"

                #index_1_w = operand1.rfind("w ", 0, index_1_d)
                #index_2_w = operand2.rfind("w ", 0, index_2_d)
                #d = str(int(operand1[index_1_w + 2:index_1_d]) + int(operand2[index_2_w + 2:index_2_d])) + "d"

                #w = str(int(operand1[:index_1_w]) + int(operand2[:index_2_w])) + "w"

                #return self.to_norm_time(w + " " + d + " " + h + " " + min + " " + s + " ")
                return self.to_norm_time(h + " " + min + " " + s + " ")
            elif operator == "-":
                index_1_s = operand1.rfind("s ")
                index_2_s = operand2.rfind("s ")
                index_1_min = operand1.rfind("min ", 0, index_1_s)
                index_2_min = operand2.rfind("min ", 0, index_2_s)
                s = str(int(operand1[index_1_min + 3:index_1_s]) - int(operand2[index_2_min + 3:index_2_s])) + "s"

                index_1_h = operand1.rfind("h ", 0, index_1_min)
                index_2_h = operand2.rfind("h ", 0, index_2_min)
                min = str(int(operand1[index_1_h + 3:index_1_min]) - int(operand2[index_2_h + 3:index_2_min])) + "min"

                #index_1_d = operand1.rfind("d ", 0, index_1_h)
                #index_2_d = operand2.rfind("d ", 0, index_2_h)
                #h = str(int(operand1[index_1_d + 3:index_1_h + 1]) - int(operand2[index_2_d + 3:index_2_h + 1])) + "h"
                h = str(int(operand1[:index_1_h + 1]) - int(operand2[:index_2_h + 1])) + "h"

                #index_1_w = operand1.rfind("w ", 0, index_1_d)
                #index_2_w = operand2.rfind("w ", 0, index_2_d)
                #d = str(int(operand1[index_1_w + 2:index_1_d]) - int(operand2[index_2_w + 2:index_2_d])) + "d"

                #w = str(int(operand1[:index_1_w]) - int(operand2[:index_2_w])) + "w"

                #return self.to_norm_time(w + " " + d + " " + h + " " + min + " " + s + " ")
                return self.to_norm_time(h + " " + min + " " + s + " ")
        elif self.flag_dist == True:
            if operator == "+":
                index_1_mm = operand1.rfind("mm ")
                index_2_mm = operand2.rfind("mm ")
                index_1_cm = operand1.rfind("cm ", 0, index_1_mm)
                index_2_cm = operand2.rfind("cm ", 0 ,index_2_mm)
                mm = str(int(operand1[index_1_cm + 3:index_1_mm]) + int(operand2[index_2_cm + 3:index_2_mm])) + "mm"

                index_1_m = self.is_m(operand1)
                index_2_m = self.is_m(operand2)
                cm = str(int(operand1[index_1_m + 3:index_1_cm]) + int(operand2[index_2_m + 3:index_2_cm])) + "cm"

                index_1_km = operand1.rfind("km ", 0 , index_1_m)
                index_2_km = operand2.rfind("km ", 0, index_2_m)
                m = str(int(operand1[index_1_km + 3:index_1_m + 1]) + int(operand2[index_2_km + 3:index_2_m + 1])) + "m"

                km = str(int(operand1[:index_1_km]) + int(operand2[:index_2_km])) + "km"

                return self.to_norm_dist(km + " " + m + " " + cm + " " + mm + " ")
            elif operator == "-":
                index_1_mm = operand1.rfind("mm ")
                index_2_mm = operand2.rfind("mm ")
                index_1_cm = operand1.rfind("cm ", 0, index_1_mm)
                index_2_cm = operand2.rfind("cm ", 0 ,index_2_mm)
                mm = str(int(operand1[index_1_cm + 3:index_1_mm]) - int(operand2[index_2_cm + 3:index_2_mm])) + "mm"

                index_1_m = operand1.rfind("m ", 0 , index_1_cm)
                index_2_m = operand2.rfind("m ", 0, index_2_cm)
                cm = str(int(operand1[index_1_m + 2:index_1_cm]) - int(operand2[index_2_m + 2:index_2_cm])) + "cm"

                index_1_km = operand1.rfind("km ", 0 , index_1_m)
                index_2_km = operand2.rfind("km ", 0, index_2_m)
                m = str(int(operand1[index_1_km + 3:index_1_m]) - int(operand2[index_2_km + 3:index_2_m])) + "m"

                km = str(int(operand1[:index_1_km]) - int(operand2[:index_2_km])) + "km"

                return self.to_norm_dist(km + " " + m + " " + cm + " " + mm + " ")
        else:    
            if operator == "+":
                return self.num_format(str(operand1 + operand2))
            elif operator == "-":
                return self.num_format(str(operand1 - operand2))
            elif operator == "*":
                return self.num_format(str(operand1 * operand2))
            elif operator == "/":
                if operand2 == 0:
                    return("Error")
                    self.flag_in == True
                else:
                    return self.num_format(str(operand1 / operand2))
            elif operator == "%":
                return self.num_format(str(operand1 * operand2 / 100))
            elif operator == "1/x":
                if operand1 == 0:
                    return("Error")
                    self.flag_in == True
                else:
                    return self.num_format(str(1 / operand1))
            elif operator == "^":
                num = operand1
                if self.num_format(str(operand2)).rfind(".") != -1:
                    for i in range(1, int(operand2)):
                        num *= operand1

                    num = num * (operand1 ** float("0." + str(operand2)[str(operand2).rfind(".") + 1:]))
                elif operand2 > 0:
                    for i in range(1, int(operand2)):
                        num *= operand1
                elif operand2 < 0:
                    for i in range(1, -int(operand2)):
                        num *= operand1
                    
                    num = 1.0 / num
                elif operand2 == 0:
                    num = 1
                    
                return self.num_format(str(num))
            elif operator == "root":
                if operand1 < 0:
                    return("Error")
                    self.flag_in == True
                else:
                    return self.num_format(str(math.sqrt(operand1)))
            else:
                return self.result.value

    #формат выводы числа
    def num_format(self, result):
        if result.rfind(".") == -1:
            return result
        elif result.rfind(".0") == len(result) - 2:
            return result[:-2]
        else:
            result = str('%.3f' % float(result))
            if result.rfind(".000") != -1:
                result = result.replace(".000", "")
            elif result.rfind("00") == len(result) - 2:
                result = result[:-2]
            elif result.rfind("0") == len(result) - 1:
                result = result[:-1]

            return result

    #преобразование буквенных обозначений в десятичную запись числа
    def letter_to_num(self, let):
        if let == "A":
            return "10"
        elif let == "B":
            return "11"
        elif let == "C":
            return "12"
        elif let == "D":
            return "13"
        elif let == "E":
            return "14"
        elif let == "F":
            return "15"
        else:
            return let

    #преобразование десятичных числе в буквенные обозанчения
    def num_to_letter(self, num):
        if num == 10:
            return "A"
        elif num == 11:
            return "B"
        elif num == 12:
            return "C"
        elif num == 13:
            return "D"
        elif num == 14:
            return "E"
        elif num == 15:
            return "F"
        else:
            return str(num)

    #перевод из любой СИ в 10-ую
    def to_10(self, radix):
        if radix == "10":
            return float(self.result.value)
        else:
            start = 0
            if self.result.value[0] == "-":
                start = 1

            end = len(self.result.value)
            if self.result.value.find(".") != -1:
                end = self.result.value.find(".")

            new = 0
            for i in range(start, end):
                new += int(self.letter_to_num(self.result.value[i])) * int(radix) ** (end - i - 1)

            for i in range(end + 1, len(self.result.value)):
                new += int(self.letter_to_num(self.result.value[i])) * int(radix) ** (-(i - end))

            if start == 1:
                new = -new
        
            return new

    #нормализует вид выводимого расстояния
    def to_norm_dist(self, input):
        mm = 0
        cm = 0
        m = 0
        km = 0

        index_r = input.find("mm")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            mm = int(float(num)) % 10
            cm = int(float(num)) // 10 + mm // 10
            mm = mm % 10

        index_r = input.find("cm")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            cm += int(float(num)) % 100
            index_dot = num.rfind(".")
            l = len(num)
            if len(num[index_dot + 1:]) > 1:
                l = index_dot + 1 + 1 
            if index_dot != -1:
                mm += int(num[index_dot + 1:l])
            m = int(float(num)) // 100 + cm // 100
            cm = cm % 100

        index_r = self.is_m(input)
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r + 1]
            m += int(float(num)) % 1000
            index_dot = num.rfind(".")
            l = len(num)
            if len(num[index_dot + 1:]) > 3:
                l = index_dot + 1 + 3 
            if index_dot != -1:
                mm += int(num[index_dot + 1:l])
            km = int(float(num)) // 1000 + m // 1000
            m = m % 1000

        index_r = input.find("km")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            km += int(float(num))
            index_dot = num.rfind(".")
            l = len(num)
            if len(num[index_dot + 1:]) > 6:
                l = index_dot + 1 + 6
            if index_dot != -1:
                mm += int(num[index_dot + 1:l])

        dist = str(km) + "km " + str(m) + "m " + str(cm) + "cm " + str(mm) + "mm "

        return dist

    #нормализует вид выводимого времени
    def to_norm_time(self, input):
        s = 0
        min = 0
        h = 0
        d = 0
        w = 0

        index_r = input.find("s")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            s = int(num) % 60
            min = int(num) // 60

        index_r = input.find("min")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            min += int(num) % 60
            h = int(num) // 60 + min // 60
            min = min % 60

        index_r = input.find("h")
        if index_r != -1:
            index_l = input.rfind(" ", 0, index_r) + 1
            num = input[index_l:index_r]
            h += int(num) % 24
            #d = int(num) // 24 + h // 24
            h = h % 24

        #index_r = input.find("d")
        #if index_r != -1:
            #index_l = input.rfind(" ", 0, index_r) + 1
            #num = input[index_l:index_r]
            #d += int(num) % 7
            #w = int(num) // 7 + d // 7
            #d = d % 7

        #index_r = input.find("w")
        #if index_r != -1:
            #index_l = input.rfind(" ", 0, index_r) + 1
            #num = input[index_l:index_r]
            #w += int(num)

        #time = str(w) + "w " + str(d) + "d " + str(h) + "h " + str(min) + "min " + str(s) + "s "
        time = str(h) + "h " + str(min) + "min " + str(s) + "s "

        return time

    #функция находит индекс когда в строке ввода встречается строка вида xm, x - число
    def is_m(self, input):
        index = input.find("0m ") 
      
        if index == -1:
            index = input.find("1m ")
        if index == -1:
            index = input.find("2m ")
        if index == -1:
            index = input.find("3m ") 
        if index == -1:
            index = input.find("4m ")
        if index == -1:
            index = input.find("5m ") 
        if index == -1:
            index = input.find("6m ") 
        if index == -1:
            index = input.find("7m ") 
        if index == -1:
            index = input.find("8m ") 
        if index == -1:
            index = input.find("9m ")

        return index

    #изменение активных кнопок при переключении СИ
    def dd_changed(self, e):
        if self.dd.value == "Время":
            self.flag_dist = False
            self.flag_time = True
            #self.b_rev_km_d.content = self.b_d
            self.b_rev_km_d.content = self.b_rev_dis
            self.b_to_secodn_power_m_h.content = self.b_h
            self.b_square_root_cm_min.content = self.b_min
            self.b_div_mm_s.content = self.b_s
            self.b_proc.content = self.b_proc_dis
            self.b_multi.content = self.b_multi_dis
            self.b_plus_minus.content = self.b_plus_minus_dis
            self.b_dot.content = self.b_dot_dis
            self.reset()

            for i in range(8):
                self.b_list[i].content = self.b_undis_list[i]

            for i in range(8, 14):
                self.b_list[i].content = self.b_dis_list[i]
        elif self.dd.value == "Расстояние":
            self.flag_time = False
            self.flag_dist = True
            self.b_rev_km_d.content = self.b_km
            self.b_to_secodn_power_m_h.content = self.b_m
            self.b_square_root_cm_min.content = self.b_cm
            self.b_div_mm_s.content = self.b_mm
            self.b_proc.content = self.b_proc_dis
            self.b_multi.content = self.b_multi_dis
            self.b_plus_minus.content = self.b_plus_minus_dis
            self.b_dot.content = self.b_dot_undis
            self.reset()

            for i in range(8):
                self.b_list[i].content = self.b_undis_list[i]

            for i in range(8, 14):
                self.b_list[i].content = self.b_dis_list[i]
        else:
            if self.flag_dist == True or self.flag_time == True:
                self.reset()
            self.flag_time = False
            self.flag_dist = False
            self.b_rev_km_d.content = self.b_rev_undis
            self.b_to_secodn_power_m_h.content = self.b_to_secodn_power
            self.b_square_root_cm_min.content = self.b_square_root
            self.b_div_mm_s.content = self.b_div
            self.b_proc.content = self.b_proc_undis
            self.b_multi.content = self.b_multi_undis
            self.b_plus_minus.content = self.b_plus_minus_undis
            self.b_dot.content = self.b_dot_undis
            self.flag_dd_change = True

            #при переключении основании СИ вывод правильной подсказки
            if self.eq_last == True:
                self.operator = ""
                self.flag_result = False
                self.hints_out(self.operator, self.result.value)
            elif self.flag_result == True: 
                self.flag_in = True
                self.eq_last = True
                self.hints_out(self.operator, self.result.value)
            else:
                self.result.value = "0"

            #при переключении основании СИ активация и деактивация числовых кнопок
            r = int(self.dd.value)
            for i in range(14):
                if r > (i + 2):
                    self.b_list[i].content = self.b_undis_list[i]
                else:
                    self.b_list[i].content = self.b_dis_list[i]

        self.update()

    #действия при нажатии на кнопки расстояния
    def button_clicked_dist(self, e):
        if self.hints.value.find("Введите число") != -1 or self.hints.value.find("уже использованы") != -1:
            self.hints.value = self.hints_save

        if e.control.data == "m":
            index_repeat = self.is_m(self.result.value)
        else:
            index_repeat = self.result.value.find(e.control.data)
            
        if index_repeat == -1 and self.result.value[len(self.result.value) - 1] != ".":
            if self.result.value == "0":
                self.result.value += e.control.data + " "
            elif self.result.value.rfind("m") != (len(self.result.value) - 2) or self.result.value.rfind("m") == -1:
                self.result.value += e.control.data + " "
            else:
                self.hints_save = self.hints.value
                self.hints.value = "Введите число"
        elif self.result.value[len(self.result.value) - 1] != ".":
            self.hints_save = self.hints.value
            self.hints.value = e.control.data + " " + "уже использованы"

        if self.hints.value == "Не правильный формат данных":
            self.hints.value = self.hints_save

        self.flag_dot = False

        self.update()

    #действия при нажатии на кнопки времени
    def button_clicked_time(self, e):
        if self.hints.value.find("Введите число") != -1 or self.hints.value.find("уже использованы") != -1:
            self.hints.value = self.hints_save

        if self.result.value.find(e.control.data) == -1:
            if self.result.value == "0":
                self.result.value += e.control.data + " "
            elif self.result.value[-1] not in ("d", "h", "n", "s"):
                self.result.value += e.control.data + " "
            else:
                self.hints_save = self.hints.value
                self.hints.value = "Введите число"
        else:
            self.hints_save = self.hints.value
            self.hints.value = e.control.data + " " + "уже использованы"

        if self.hints.value == "Не правильный формат данных":
            self.hints.value = self.hints_save

        self.update()

    def zero_del(self, string):
        if self.flag_dist == True:
            string = string.replace("0km ", "")
            string = string.replace("0cm ", "")
            string = string.replace("0m ", "")
            string = string.replace("0mm ", "")
        elif self.flag_time == True:
            string = string.replace("0w ", "")
            string = string.replace("0d ", "")
            string = string.replace("0h ", "")
            string = string.replace("0min ", "")
            string = string.replace("0s ", "")

        return string