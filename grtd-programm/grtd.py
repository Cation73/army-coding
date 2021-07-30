# импортирование библиотек
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pandas as pd
import os
import math
import sqlite3

# основное окно
class window(QtWidgets.QWidget):
    # инициализирование и изменение базовых параметров окна
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Газодинамический расчет для турбореактивного двигателя')
        self.setWindowIcon(QtGui.QIcon('era.jfif'))
        self.font = QtGui.QFont('Times New Roman')
        start_font_size = 14
        self.font.setPixelSize(start_font_size)
        self.k_font = start_font_size / 243

        self.main_window_widget()
        self.main_functions()

    # функция, которая "строит" главное окно
    def main_window_widget(self):
        # компановка виджетов
        self.form = QtWidgets.QFormLayout(self)
        # виджеты ввода
        self.high_le = QtWidgets.QDoubleSpinBox(decimals = 1)
        self.high_le.setRange(0, 16)
        self.high_le.setValue(0.0)
        self.high_le.setSingleStep(0.5)
        self.calculatedmode_le = QtWidgets.QLineEdit()
        self.calculatedmode_le.setText('False')
        self.v_le = QtWidgets.QDoubleSpinBox(decimals = 1)
        self.v_le.setRange(0, 1000)
        self.v_le.setValue(0.0)
        self.v_le.setSingleStep(1)
        self.m_le = QtWidgets.QDoubleSpinBox(decimals = 1)
        self.m_le.setRange(0, 100)
        self.m_le.setValue(0.0)
        self.m_le.setSingleStep(1)
        
        self.k = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.k.setRange(0.1, 10)
        self.k.setValue(1.4)
        self.k.setSingleStep(0.1)
        self.sigma_vox = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.sigma_vox.setRange(0.001, 1)
        self.sigma_vox.setValue(0.985)
        self.sigma_vox.setSingleStep(0.001)
        self.t_r = QtWidgets.QSpinBox()
        self.t_r.setRange(10, 10000)
        self.t_r.setValue(1370)
        self.t_r.setSingleStep(10)
        self.pi_k_sum = QtWidgets.QSpinBox()
        self.pi_k_sum.setRange(1, 100)
        self.pi_k_sum.setValue(15)
        self.pi_k_sum.setSingleStep(1)
        
        self.eta = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.eta.setRange(0.001, 100)
        self.eta.setValue(28.966)
        self.eta.setSingleStep(1)
        self.eta_pk = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.eta_pk.setRange(0.01, 1)
        self.eta_pk.setValue(0.9)
        self.eta_pk.setSingleStep(0.1)
        self.sigma_ks = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.sigma_ks.setRange(0.001, 1)
        self.sigma_ks.setValue(0.955)
        self.sigma_ks.setSingleStep(0.01)
        self.h_u = QtWidgets.QSpinBox()
        self.h_u.setRange(1, 1000000)
        self.h_u.setValue(43100)
        self.h_u.setSingleStep(100)
        
        self.eta_g = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.eta_g.setRange(0.001, 1)
        self.eta_g.setValue(0.985)
        self.eta_g.setSingleStep(0.01)
        self.t_10 = QtWidgets.QSpinBox()
        self.t_10.setRange(1, 1000)
        self.t_10.setValue(159)
        self.t_10.setSingleStep(1)
        self.t_50 = QtWidgets.QSpinBox()
        self.t_50.setRange(1, 1000)
        self.t_50.setValue(179)
        self.t_50.setSingleStep(1)
        self.t_90 = QtWidgets.QSpinBox()
        self.t_90.setRange(1, 1000)
        self.t_90.setValue(208)
        self.t_90.setSingleStep(1)

        self.d_20 = QtWidgets.QDoubleSpinBox(decimals = 1)
        self.d_20.setRange(1, 10000)
        self.d_20.setValue(791.5)
        self.d_20.setSingleStep(1)
        self.a_aroma = QtWidgets.QDoubleSpinBox(decimals = 1)
        self.a_aroma.setRange(0.1, 100)
        self.a_aroma.setValue(16.6)
        self.a_aroma.setSingleStep(1)
        self.g_otb = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.g_otb.setRange(0.001, 1)
        self.g_otb.setValue(0.015)
        self.g_otb.setSingleStep(0.01)
        self.g_ohl = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.g_ohl.setRange(0.001, 1)
        self.g_ohl.setValue(0.04)
        self.g_ohl.setSingleStep(0.01)
        
        self.nu_mex = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.nu_mex.setRange(0.001, 1)
        self.nu_mex.setValue(0.995)
        self.nu_mex.setSingleStep(0.01)
        self.k_g = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.k_g.setRange(0.01, 10)
        self.k_g.setValue(1.33)
        self.k_g.setSingleStep(0.1)
        self.nu_tvd = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.nu_tvd.setRange(0.01, 1)
        self.nu_tvd.setValue(0.91)
        self.nu_tvd.setSingleStep(0.01)
        self.fi_pc = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.fi_pc.setRange(0.01, 1)
        self.fi_pc.setValue(0.98)
        self.fi_pc.setSingleStep(0.01)
        
        self.p = QtWidgets.QSpinBox()
        self.p.setRange(1, 10000)
        self.p.setValue(100)
        self.p.setSingleStep(1)
        self.p_ud_st = QtWidgets.QSpinBox()
        self.p_ud_st.setRange(1, 10000)
        self.p_ud_st.setValue(579)
        self.p_ud_st.setSingleStep(10)
        self.c_ud_st = QtWidgets.QDoubleSpinBox(decimals = 3)
        self.c_ud_st.setRange(0.001, 10)
        self.c_ud_st.setValue(0.112)
        self.c_ud_st.setSingleStep(0.01)
        self.c_v = QtWidgets.QSpinBox()
        self.c_v.setRange(1, 1000)
        self.c_v.setValue(160)
        self.c_v.setSingleStep(10)
        self.c_k = QtWidgets.QSpinBox()
        self.c_k.setRange(1, 1000)
        self.c_k.setValue(100)
        self.c_k.setSingleStep(10)
        
        self.c_r = QtWidgets.QSpinBox()
        self.c_r.setRange(1, 1000)
        self.c_r.setValue(150)
        self.c_r.setSingleStep(10)
        self.c_y = QtWidgets.QSpinBox()
        self.c_y.setRange(1, 1000)
        self.c_y.setValue(250)
        self.c_y.setSingleStep(10)
        self.c_t = QtWidgets.QSpinBox()
        self.c_t.setRange(1, 1000)
        self.c_t.setValue(320)
        self.c_t.setSingleStep(10)
        self.c_c = QtWidgets.QSpinBox()
        self.c_c.setRange(1, 1000)
        self.c_c.setValue(562)
        self.c_c.setSingleStep(10)
        
        self.d_v = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.d_v.setRange(0.01, 10)
        self.d_v.setValue(0.45)
        self.d_v.setSingleStep(0.1)
        self.z_tvd = QtWidgets.QSpinBox()
        self.z_tvd.setRange(0, 10)
        self.z_tvd.setValue(1)
        self.z_tvd.setSingleStep(1)
        self.nu_high_pressure = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.nu_high_pressure.setRange(0.01, 100)
        self.nu_high_pressure.setValue(1.75)
        self.nu_high_pressure.setSingleStep(0.1)
        self.z_tnd = QtWidgets.QSpinBox()
        self.z_tnd.setRange(0, 10)
        self.z_tnd.setValue(1)
        self.z_tnd.setSingleStep(1)

        self.nu_low_pressure = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.nu_low_pressure.setRange(0.01, 100)
        self.nu_low_pressure.setValue(1.35)
        self.nu_low_pressure.setSingleStep(0.1)
        self.nu_knd_kvd = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.nu_knd_kvd.setRange(0.01, 1)
        self.nu_knd_kvd.setValue(0.28)
        self.nu_knd_kvd.setSingleStep(0.1)
        self.ro_lnd = QtWidgets.QSpinBox()
        self.ro_lnd.setRange(1, 10000)
        self.ro_lnd.setValue(8200)
        self.ro_lnd.setSingleStep(100)
        self.ro_lvd = QtWidgets.QSpinBox()
        self.ro_lvd.setRange(1, 10000)
        self.ro_lvd.setValue(8250)
        self.ro_lvd.setSingleStep(100)
        
        self.fi = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.fi.setRange(0.01, 1)
        self.fi.setValue(0.55)
        self.fi.setSingleStep(0.1)
        self.t_resource = QtWidgets.QSpinBox()
        self.t_resource.setRange(1, 100000)
        self.t_resource.setValue(25000)
        self.t_resource.setSingleStep(1000)
        self.takeoff_rate = QtWidgets.QDoubleSpinBox(decimals = 2)
        self.takeoff_rate.setRange(0.01, 1)
        self.takeoff_rate.setValue(0.05)
        self.takeoff_rate.setSingleStep(0.1)
        self.sigma_tvd = QtWidgets.QSpinBox()
        self.sigma_tvd.setRange(1, 1000)
        self.sigma_tvd.setValue(280)
        self.sigma_tvd.setSingleStep(10)
        self.sigma_tnd = QtWidgets.QSpinBox()
        self.sigma_tnd.setRange(1, 1000)
        self.sigma_tnd.setValue(300)
        self.sigma_tnd.setSingleStep(10)
        
        # создание окна помощи
        self.bar = QtWidgets.QMenuBar(self)
        self.file_menu = self.bar.addMenu('Помощь')
        self.description = QtWidgets.QAction('Описание программы', self)
        self.file_menu.addAction(self.description)
        
        
        
        self.label = QtWidgets.QLabel()
        # кнопка закрытия
        self.btnQuit = QtWidgets.QPushButton('Закрыть окно')
        # вспылающая подсказка по кнопке
        self.btnQuit.setToolTip('Нажмите кнопку, чтобы закрыть окно')
        self.btnQuit.setToolTipDuration(-1)
        # кнопка расчета скорости
        self.f_s = QtWidgets.QPushButton('Расчет')
        self.f_s.setToolTip('Нажмите кнопку, чтобы произвести расчет')
        self.f_s.setToolTipDuration(-1)
        # вертикальный контейнер
        self.hbox = QtWidgets.QHBoxLayout()
        # добавление в вертикальный контейнер элементов
        self.hbox.addWidget(self.f_s)
        self.hbox.addWidget(self.btnQuit)
        self.form.setRowWrapPolicy(self.form.WrapLongRows)
        # добавление строк с текстом и соответствующим полем ввода
        self.form.addRow('Введите высоту полета (м):', self.high_le)
        self.form.addRow('Скорость полета (м/c):', self.v_le)
        self.form.addRow('Число Маха:', self.m_le)
        self.form.addRow('Укажите, скорость полета определяется на расчетном режиме или нет (True или False): ', 
                         self.calculatedmode_le)
        
        self.form.addRow('Показатель адиабаты для сухого воздуха: ', self.k)
        self.form.addRow('Коэффициент восстановления полного давления в воздухозаборнике двигателя (для стендовых условий можно σвх=0.98..0.99): ', 
                         self.sigma_vox)
        self.form.addRow('Температура газа перед турбиной (K): ', self.t_r)
        self.form.addRow('Общая степень повышения  давления воздуха в компрессорe: ', self.pi_k_sum)
        
        self.form.addRow('Масса одного киломоля воздуха для вычисления R (Дж/кг*K): ', self.eta)
        self.form.addRow('Политропный КПД ступени осевого компрессора: ', self.eta_pk)
        self.form.addRow('Коэффициент восстановления полного давления (σкс 0.95...0.97)', self.sigma_ks)
        self.form.addRow('Рабочая теплотворная способность авиационного топлива (кДж/кг): ', self.h_u)
        
        self.form.addRow('Коэффициент выделения тепла: ', self.eta_g)
        self.form.addRow('По ГОСТ 2177-99 температура кипения 10% отгона (градусов Цельсия): ', self.t_10)
        self.form.addRow('По ГОСТ 2177-99 температура кипения 50% отгона (градусов Цельсия): ', self.t_50)
        self.form.addRow('По ГОСТ 2177-99 температура кипения 90% отгона (градусов Цельсия): ', self.t_90)
        self.form.addRow('По ГОСТ 3900-85 плотность топлива при 20 градусов Цельсия (кг/м^3): ', self.d_20)
        
        self.form.addRow('По ГОСТ Р 52063-2003 доля ароматических углеводородов: ', self.a_aroma)
        self.form.addRow('Относительный расход воздуха, отбираемый от компресссора высокого давления на нужды воздушного судна (0.01...0.02): ', 
                         self.g_otb)
        self.form.addRow('Относительного расход воздуха на охлаждение температуры газа перед турбиной: ', self.g_ohl)
        self.form.addRow('Коэффициент, учитывающий затраты мощности на привод вспомогательных агрегатов (0.995-0.998): ', 
                         self.nu_mex)
        
        self.form.addRow('Показатель адиабаты продуктов сгорания: ', self.k_g)
        self.form.addRow('Адиабатический КПД турбины по параметрам заторможенного потока: ', self.nu_tvd)
        self.form.addRow('Коэффициент скорости (0.97...0.985): ', self.fi_pc)
        self.form.addRow('Взлетная тяга (кН): ', self.p)
        
        self.form.addRow('Удельная тяга (на основании данных о двигателе): ', self.p_ud_st)
        self.form.addRow('Расход топлива (на основании данных о двигателе, кг/Н*ч): ', self.c_ud_st)
        self.form.addRow('Осевая скорость на входе в компрессор низкого давления (160...200, м/c): ', self.c_v)
        self.form.addRow('Осевая скорость на выходе из компрессора высокого давления (м/c): ', self.c_k)
        
        self.form.addRow('Осевая скорость на входе в компрессор высокого давления (150...160, м/c): ', self.c_r)
        self.form.addRow('Осевая скорость на выходе из турбины высокого давления (250...280, м/c): ', self.c_y)
        self.form.addRow('Осевая скорость на выходе из турбины низкого давления (300...350, м/c): ', self.c_t)
        self.form.addRow('Осевая скорость в обрезе выходного сопла (м/c): ', self.c_c)

        self.form.addRow('Относительный диаметр втулки в данном сечении у двигателя: ', self.d_v)
        self.form.addRow('Количество ступеней турбины высокого давления: ', self.z_tvd)
        self.form.addRow('Коэффициент нагрузки ступени высокого давления: ', self.nu_high_pressure)
        self.form.addRow('Количество ступеней турбины низкого давления: ', self.z_tnd)
        
        self.form.addRow('Коэффициент нагрузки ступени низкого давления: ', self.nu_low_pressure)
        self.form.addRow('Коэффициент нагрузки ступеней компрессора (0.25...0.4): ', self.nu_knd_kvd)
        self.form.addRow('Плотность материала лопатки низкого давления (кг/м^3): ', self.ro_lnd)
        self.form.addRow('Плотность материала лопатки высокого давления (кг/м^3): ', self.ro_lvd)

        self.form.addRow('Коэффициент, учитывающий уменьшением напряжения растяжения из-за изменения толщины профилей лопатки по высоте (0.5...0.6): ', 
                         self.fi)
        self.form.addRow('Назначенный ресурс двигателя (20000...25000, час): ', self.t_resource)
        self.form.addRow('Доля работы двигателя на взлетном режиме: ', self.takeoff_rate)
        self.form.addRow('Допускаемое напряжение длительной прочности для лопаток турбины высокого давления (МПа): ', self.sigma_tvd)     
        self.form.addRow('Допускаемое напряжение длительной прочности для лопаток турбины низкого давления (МПа): ', self.sigma_tnd)   
        
        # добавление поля прокрутки
        self.mygroupbox = QtWidgets.QGroupBox()
        self.form.addRow(self.label)
        self.form.addRow(self.hbox)
        self.f_s.clicked.connect(self.main_functions)
        self.btnQuit.clicked.connect(self.btn_click_close)
        self.mygroupbox.setLayout(self.form)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(self.mygroupbox)
        self.scroll.setFixedHeight(600)
        self.scroll.setFixedWidth(900)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
    
    # расчетные функции
    def main_functions(self):
        self.output_window = output_window()
        # нахождение температуры и давления наружного воздуха, а также скорости звука по таблице 3
        #data = pd.read_csv(os.path.join(os.path.dirname(__file__), '../gui_version/standard_atmosphere.csv'))
        #data['high'] = data['high'].astype('float64')
        #data = pd.DataFrame(data)
        conn = sqlite3.connect(os.path.realpath('../gui_version/standard_atmosphere.db'))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = pd.read_sql(sql = 'SELECT * FROM standard_atmosphere', con = conn)
        
        self.t_k = data[data['high'] == self.high_le.value()]['t_k'].values[0]
        self.p_a = int(data[data['high'] == self.high_le.value()]['p_a'].values[0])
        self.a = round(data[data['high'] == self.high_le.value()]['a'].values[0], 2)

        # определение скорости полета
        # если скорость полета задается на расчетном режиме, то определяется число Маха
        if self.calculatedmode_le.text() == 'True':
            self.m_le = self.v_le
        # в условиях старта (V = 0, M = 0)
        else:
            self.v_le = self.m_le
     
        # расчет параметров заторможенного потока воздуха на входе в двигатель    
        # температура торможения из выражения для полной энергии потока в сечении
        self.t_k_n = self.t_k*(1 + (self.k.value()-1)*(self.m_le.value()**2)/2)
        # полное давление из уравнения адиабатного процесса торможения
        self.p_a_n = int(self.p_a*(self.t_k_n/self.t_k)**(self.k.value()/(self.k.value()-1)))

        # расчет параметров воздуха на входе в компрессор
        # температура из уравнения сохранения энергии для воздухозаборника
        self.t_k_v = self.t_k_n
        # давление
        if self.m_le.value() == 0:
            self.p_a_v = int(self.p_a_n * self.sigma_vox.value())
        elif 1 < self.m_le.value() <= 3:
            self.sigma_vx = (self.sigma_vox.value() - 
                             0.02241*(self.m_le.value() - 1)**2 
                             - 0.14561*(self.m_le.value() - 1)**3
                             + 0.086282*(self.m_le.value() - 1)**4
                             - 0.014342*(self.m_le.value() - 1)**5)
            self.p_a_v = int(self.p_a_n*self.sigma_vx)

        # расчет степени повышения давления в компрессоре
        self.R = 8314/self.eta.value()
        # если температура газа перед турбиной меньше или равна 1270 К, то:
        if self.t_r.value() <= 1270:
            self.l_ad_knd = (0.5*self.k.value()*self.R*self.t_k_v
                             *(self.pi_k_sum.value()**(self.k.value()-1/self.k.value()) - 1)
                             /(self.k.value()-1))
            self.pi_knd = (round((1 + self.l_ad_knd/(self.k.value()*self.R
                                                     *self.t_k_v/(self.k.value()-1)))**(self.k.value()/self.k.value()-1), 2))
            self.pi_kvd = round(self.pi_k_sum.value()/self.pi_knd, 2)
        else:
            self.pi_knd = round(self.pi_k_sum.value()**0.5, 2)
            self.pi_kvd = round(self.pi_knd, 2)
       
        # определение удельной работы сжатия (на 1 кг воздуха) и параметров воздушного потока за компрессором низкого давления
        # политропный КПД ступени осевого компрессора - упрощенный расчет
        self.c_pv = round(self.k.value()*self.R/(self.k.value()-1), 1)
        self.eta_knd = (round(((self.pi_knd**((self.k.value()-1)/self.k.value()))-1)
                              /((self.pi_knd**((self.k.value()-1)/(self.k.value()*self.eta_pk.value())))-1),2))
        self.p_x_knd = int(self.p_a_v*self.pi_knd)
        self.l_knd = int(self.c_pv*self.t_k_v*((self.pi_knd**((self.k.value()-1)/self.k.value())) - 1)/self.eta_knd)
        self.t_x_knd = round(self.t_k_v + self.l_knd/self.c_pv, 2)
    
        # расчет параметров воздуха и работы сжатия за компрессором высокого давления
        self.eta_kvd = (round(((self.pi_kvd**((self.k.value()-1)/self.k.value())) - 1)
                              /((self.pi_kvd**((self.k.value()-1)/(self.k.value()*self.eta_pk.value()))) - 1), 2))
        self.l_kvd = int(self.c_pv*self.t_x_knd*(self.pi_kvd**((self.k.value()-1)/self.k.value())-1)/self.eta_kvd)
        self.t_k_kvd = int(self.t_x_knd + self.l_kvd/self.c_pv)
        self.p_k_kvd = int(self.p_x_knd*self.pi_kvd)
      
        # расчет давления газа на входе в турбину высокого давления
        self.p_g = int(self.p_k_kvd*self.sigma_ks.value())
   
        # определение основных параметров камеры сгорания  
        # средняя условная теплоемкость процесса теплоподвода
        self.c_n = 0.9 + (0.0001*(2*self.t_r.value() + self.t_k_kvd))
        # количество теплоты, сообщаемое воздуху q_ks
        self.q_ks = round(self.c_n*(self.t_r.value() - self.t_k_kvd), 2)
        # отношение расходов топлива и воздуха в камере сгорания
        self.g_t = round(self.q_ks/(self.h_u.value()*self.eta_g.value()), 4)
        # по гост-2177-99 определяется температура кипения 10%, 50%, 90% отгона и определяется средняя температура кипения
        self.t_b = (self.t_10.value()+self.t_50.value()+self.t_90.value())/3
        # по гост 3900-85 определяется плотность топрива при 20 градусах цельсия -d_20
        # расчет плотности при 15 градусах цельсия
        self.d_15 = 0.994*self.d_20.value() + 9.3
        # по гост р 52063-2003 определяется доля ароматических углеводородов - a_aroma
        # расчет массовой доли водорода
        self.h_mass_fraction = ((92.012 + 0.1449*self.t_b - 0.7022*self.a_aroma.value())/self.d_15) + 0.0002652*self.a_aroma.value() \
            + 0.000001298*self.a_aroma.value()*self.t_b - 0.0001347*self.t_b + 0.02003
        # расчет массовой доли углеводорода
        self.c_mass_fraction = 1 - self.h_mass_fraction
        # стехиометрический коэффициент
        self.l_o = 11.515*self.c_mass_fraction + 34.329*self.h_mass_fraction
        # коэффициент избытка воздуха на выходе из камеры сгорания
        self.a_sum = round(1/(self.l_o*self.g_t), 2)
        # газовая постоянная продуктов сгорания
        self.r_g = round((8314/self.eta.value())*(1+1.0862*self.g_t)/(1+self.g_t), 1)
  
        # удельная работа расширения газа в турбине высокого давления
        #g_ohl = 0.01+0.09*((t_r/1000)-1)+0.2*(((t_r/1000)-1)**2)+0.16*(((t_r/1000)-1)**3)
        # возможно ошибка в формуле g_ohl
        self.l_tvd = int(self.l_kvd/((1+self.g_t)*(1-self.g_otb.value()-self.g_ohl.value())*self.nu_mex.value()))
       
        # определение степени понижения давления в турбине высокого давления
        self.pi_tvd = (round((1-((self.l_tvd*(self.k_g.value() - 1))
                                 /(self.r_g*self.t_r.value()*self.nu_tvd.value()*self.k_g.value())))
                             **((-1)/((self.k_g.value()-1)/self.k_g.value())), 4))
   
        # расчет параметров потока газа на выходе из турбины высокого давления
        # температура газа на выходе из неохлаждаемой турбины
        self.t_y = int(self.t_r.value() - ((self.l_tvd)/((self.k_g.value()/(self.k_g.value()-1))*self.r_g)))
        # относительный расход газа в турбине высокого давления
        self.g_r = round((1+self.g_t)*(1-self.g_ohl.value()-self.g_otb.value()), 3)
        # средние теплоемкости газа, воздуха и газовоздушной смеси
        self.c_pr = round(0.9+self.t_y*3*10**(-4), 4)
        self.c_pv = round(0.9+self.t_k_kvd*3*10**(-4), 4)
        self.temporary_variable = (((self.c_pr*self.g_r*self.t_y)+
                                    (self.c_pv*self.g_ohl.value()*self.t_k_kvd))/(self.g_r + self.g_ohl.value()))
        # температура газа на выходе из охлаждаемой турбины
        self.t_yy = int(((0.81+self.temporary_variable*12*10**(-4))**0.5 - 0.9)/(6*10**(-4)))
        # давление газа на выходе из турбины высокого давления
        self.p_y = int(self.p_g/self.pi_tvd)
  
        # работа расширения газа в турбине НД
        self.l_tnd = int(self.l_knd/(self.g_r + self.g_ohl.value()))
   
        # расчет степени расширения газа в турбине низкого давления и параметры потока на выходе из нее
        self.pi_tnd = ((1-((self.l_tnd*(self.k_g.value() - 1))
                           /(self.r_g*self.t_yy*self.nu_tvd.value()*self.k_g.value())))
                       **((-1)/((self.k_g.value()-1)/self.k_g.value())))
        self.t_t = round(self.t_yy - (self.l_tnd/((self.k_g.value()/(self.k_g.value()-1))*self.r_g)), 1)
        self.p_t = int(self.p_y/self.pi_tnd)
   
        # расчет выходного сопла ТРД
        # распологаемая степень понижения давления газа в сопле
        self.pi_cp = round(self.p_t/self.p_a, 3)
        # критическая степень понижения давления для суживающегося реактивного сопла
        self.pi_kr = round(((self.k_g.value() + 1)/2)**((self.k_g.value())/(self.k_g.value()-1)), 3)
        # действительная степень расширения газа в данном сопле
        self.pi_c = self.pi_cp*1
        # статистическое давление в выходном сечение сопла
        self.p_c = round(self.p_t/self.pi_kr)
        # cредняя скорость истечения газа из сопла
        self.c_c_full_rash = (round(self.fi_pc.value()*
                                    math.sqrt(2*((self.k_g.value()/(self.k_g.value()-1))
                                    *self.r_g*self.t_t*(1-(1/self.pi_c)
                                    **((self.k_g.value()-1)/self.k_g.value())))), 2))
        self.c_c_not_full_rash = (round(self.fi_pc.value()*(2*((self.k_g.value())
                                                               /(self.k_g.value()+1))*self.r_g*self.t_t)**0.5, 2))
        self.t_c = round((self.t_t - (self.c_c_not_full_rash**2/(2*(self.k_g.value()/(self.k_g.value()-1))*self.r_g))), 2)
  
        # расчет удельной тяги и расхода топлива ТРД при полном расширении в выходном сопле
        # при полном расширении в выходном сопле
        self.p_ud_poln = round(self.c_c_full_rash*(self.g_r + self.g_ohl.value()), 2)
        self.c_ud_poln = round((3600*self.g_t*(1-self.g_ohl.value()-self.g_otb.value()))/self.p_ud_poln, 4)
        # при неполном расширении газа
        self.m_g = (round((((self.k_g.value())*((2/(self.k_g.value()+1))
                                                **((self.k_g.value()+1)/(self.k_g.value()-1))))/self.r_g)**0.5, 4))
        self.lambda_c = self.c_c_not_full_rash/(math.sqrt((2*self.k_g.value()*self.r_g*self.t_t)/(self.k_g.value()+1)))
        self.y_lambda = ((((self.k_g.value()+1)/2)**(1/(self.k_g.value()-1)))
                         *(self.lambda_c)/(1-((self.k_g.value()-1)/(self.k_g.value()+1))*self.lambda_c**2))
        self.f_c = ((self.g_r+self.g_ohl.value())*(self.t_t)**0.5)/(self.m_g*self.p_c*self.y_lambda)
        self.f_cc = round(((self.g_r+self.g_ohl.value())*math.sqrt(self.t_t))/(self.m_g*self.p_c*self.y_lambda), 4)
        self.g_v = (round(1000*self.p.value()/(((self.g_r+self.g_ohl.value())
                                                *self.c_c_not_full_rash) + self.f_c*(self.p_c-self.p_a)), 2))
        self.p_ud = round(1000*self.p.value()/self.g_v, 2)
        self.c_ud = round((3600*self.g_t*(1-self.g_ohl.value()-self.g_otb.value()))/self.p_ud, 4)
      
        # часовой расход топлива
        self.g_tch = round(1000*self.p.value()*self.c_ud, 1)
   
        # уточнение отборов воздуха и механической энергии от двигателя
        self.g_otbr = round(self.g_otb.value()*self.g_v, 2)
        self.n_otbr = round((1-self.nu_mex.value())*self.g_v*self.l_tvd*self.g_r/1000, 1)

        # сравнительный анализ значений Pуд и Суд
        self.procent_p_ud = round(100*(self.p_ud - self.p_ud_st.value())/self.p_ud_st.value(), 1)
        self.procent_c_ud = round(100*(self.c_ud_st.value() - self.c_ud)/self.c_ud, 1)
      
        # геометрия контрольных сечений газовоздушного тракта
        self.c_x = (round(((self.p_x_knd-self.p_k_kvd)/(self.p_a_v-self.p_k_kvd))
                          *(self.c_v.value() - self.c_k.value()) + self.c_k.value(), 1))
      
        # расчет приведенной скорости и относительной плотности тока
        self.lambda_v = round((self.c_v.value())/(((2*self.k.value())/(self.k.value()+1))*self.R*self.t_k_v)**0.5, 4)
        self.q_lambda_v = (round((((self.k.value()+1)/2)**(1/(self.k.value()-1)))
                                 *self.lambda_v*(1-((self.k.value()-1)/(self.k.value()+1))*self.lambda_v**2)
                                 **(1/(self.k.value()-1)), 4))
    
        self.lambda_k = round((self.c_k.value())/(((2*self.k.value())/(self.k.value()+1))*self.R*self.t_k_kvd)**0.5, 4)
        self.q_lambda_k = (round((((self.k.value()+1)/2)**(1/(self.k.value()-1)))
                                 *self.lambda_k*(1-((self.k.value()-1)/(self.k.value()+1))*self.lambda_k**2)
                                 **(1/(self.k.value()-1)), 4))
    
        self.lambda_x = round((self.c_x)/(((2*self.k.value())/(self.k.value()+1))*self.R*self.t_x_knd)**0.5, 4)
        self.q_lambda_x = (round((((self.k.value()+1)/2)**(1/(self.k.value()-1)))
                                 *self.lambda_x*(1-((self.k.value()-1)/(self.k.value()+1))*self.lambda_x**2)
                                 **(1/(self.k.value()-1)), 4))
    
        self.lambda_r = round((self.c_r.value())/(((2*self.k_g.value())/(self.k_g.value()+1))*self.r_g*self.t_r.value())**0.5, 4)
        self.q_lambda_r = (round((((self.k_g.value()+1)/2)**(1/(self.k_g.value()-1)))
                                 *self.lambda_r*(1-((self.k_g.value()-1)/(self.k_g.value()+1))*self.lambda_r**2)
                                 **(1/(self.k_g.value()-1)), 4))
    
        self.lambda_y = round((self.c_y.value())/(((2*self.k_g.value())/(self.k_g.value()+1))*self.r_g*self.t_yy)**0.5, 4)
        self.q_lambda_y = (round((((self.k_g.value()+1)/2)**(1/(self.k_g.value()-1)))
                                 *self.lambda_y*(1-((self.k_g.value()-1)/(self.k_g.value()+1))*self.lambda_y**2)
                                 **(1/(self.k_g.value()-1)), 4))
    
        self.lambda_t = round((self.c_t.value())/(((2*self.k_g.value())/(self.k_g.value()+1))*self.r_g*self.t_t)**0.5, 4)
        self.q_lambda_t = (round((((self.k_g.value()+1)/2)**(1/(self.k_g.value()-1)))
                                 *self.lambda_t*(1-((self.k_g.value()-1)/(self.k_g.value()+1))*self.lambda_t**2)
                                 **(1/(self.k_g.value()-1)), 4))
        
        # проходные площади для воздуха и газа
        # m_v - нет расчета
        self.m_v = 0.0404
        self.f_v = round((self.g_v*(self.t_k_v)**0.5)/(self.m_v*self.p_a_v*self.q_lambda_v), 4)
        self.f_k = round((self.g_v*(self.t_k_kvd)**0.5)/(self.m_v*self.p_k_kvd*self.q_lambda_k), 4)
        self.f_x = round((self.g_v*(self.t_x_knd)**0.5)/(self.m_v*self.p_x_knd*self.q_lambda_x), 4)
        self.f_r = round((self.g_v*self.g_r*(self.t_r.value())**0.5)/(self.m_g*self.p_g*self.q_lambda_r), 4)
        self.f_y = round((self.g_v*(self.g_r+self.g_ohl.value())*(self.t_yy)**0.5)/(self.m_g*self.p_y*self.q_lambda_y), 4)
        self.f_t = round((self.g_v*(self.g_r+self.g_ohl.value())*(self.t_t)**0.5)/(self.m_g*self.p_t*self.q_lambda_t), 4)
        self.f_c = round(self.g_v*self.f_cc, 4)
    
        # наружный, внутренний, средний диаметры и высота лопатки в контрольных сечениях газовоздушного тракта двигателя
        # на входе в компрессор низкого давления
        self.d_vn = round(((4*self.f_v)/(math.pi*(1-(self.d_v.value())**2)))**0.5, 4)
        self.d_vvn = round(self.d_vn*self.d_v.value(), 4)
        self.d_vmean = round(0.5*(self.d_vn+self.d_vvn), 4)
        self.h_v = round(0.5*(self.d_vn-self.d_vvn), 4)
       
        # на выходе из компрессора высокого давления при постоянном наружном диаметре
        self.d_kn = round(self.d_vn, 4)
        self.d_kvn = round(((self.d_kn**2)-((4*self.f_k/math.pi)))**0.5, 4)
        self.d_kmean = round(0.5*(self.d_kn+self.d_kvn), 4)
        self.h_k = round(0.5*(self.d_kn-self.d_kvn), 4)
        
        # на выходе из компрессора высокого давления
        self.d_xn = round(self.d_vn, 4)
        self.d_xvn = round(((self.d_xn**2)-((4*self.f_x/math.pi)))**0.5, 4)
        self.d_xmean = round(0.5*(self.d_xn+self.d_xvn), 4)
        self.h_x = round(0.5*(self.d_xn-self.d_xvn), 4)
      
        # на входе в турбину высокого давления
        self.d_rmean = round(self.d_kn, 4)
        self.h_r = round(self.f_r/(math.pi*self.d_rmean), 4)
        self.d_rn = round(self.d_rmean + self.h_r, 4)
        self.d_rvn = round(self.d_rmean - self.h_r, 4)
      
        # на входе в турбину низкого давления
        self.d_ymean = round(self.d_rmean, 4)
        self.h_y = round(self.f_y/(math.pi*self.d_ymean), 4)
        self.d_yn = round(self.d_ymean + self.h_y, 4)
        self.d_yvn = round(self.d_ymean - self.h_y, 4)
      
        # на выходе из турбины низкого давления
        self.d_tmean = round(self.d_ymean, 4)
        self.h_t = round(self.f_t/(math.pi*self.d_tmean), 4)
        self.d_tn = round(self.d_tmean + self.h_t, 4)
        self.d_tvn = round(self.d_tmean - self.h_t, 4)
   
        # в обрезе выходного сопла
        self.d_c = round(((4*self.f_c)/math.pi)**0.5, 4)
   
        
        # окружная скорость на среднем диаметре
        # турбина высокого давления
        self.u_y = round(((self.l_tvd)/(self.nu_high_pressure.value()*self.z_tvd.value()))**0.5, 2) 
        # турбина низкого давления
        self.u_t = round(((self.l_tnd)/(self.nu_low_pressure.value()*self.z_tnd.value()))**0.5, 2) 
        # проверка найденных значений
        self.u_vn = round(self.u_t*self.d_vn/self.d_tmean, 2) 
        self.u_xn = round(self.u_y*self.d_xn/self.d_ymean, 2) 
        
        # необходимо сделать проверку
        #if round(u_vn, 1) == round(u_t, 1) and round(u_xn, 1) == round(u_y, 1): 
       #     print('Значения окружных скоростей сходятся')
        #else:
        #    print('Значения окружных скоростей не сходятся')
        
        # количество ступеней компрессора низкого и высокого давления
        self.z_knd = int(round(self.l_knd/(self.nu_knd_kvd.value()*self.u_vn**2), 0))
        self.z_kvd = int(round(self.l_kvd/(self.nu_knd_kvd.value()*self.u_xn**2), 0))
        
        # частота вращения роторов низкого и высокого давления
        self.n_nd = round(60*self.u_vn/(math.pi*self.d_vn), 2)
        self.n_vd = round(60*self.u_xn/(math.pi*self.d_xn), 2)
        
        # приближенная температура материала лопаток последней ступени турбины
        self.t_lvd = round(0.95*(self.t_y+((self.u_y**2)/(2*(self.k_g.value()/(self.k_g.value()-1))*self.r_g))), 2)
        self.t_lnd = round(0.95*(self.t_t+((self.u_t**2)/(2*(self.k_g.value()/(self.k_g.value()-1))*self.r_g))), 2)

        # напряжение растяжения в корневом сечении рабочих лопаток последней ступени турбины
        # низкого давления
        self.sigma_rnd = round((2*math.pi*self.ro_lnd.value()*((self.n_nd/60)**2)*self.f_t*self.fi.value())/(10**6), 2)
        # высокого давления
        self.sigma_rvd = round((2*math.pi*self.ro_lvd.value()*((self.n_vd/60)**2)*self.f_y*self.fi.value())/(10**6), 2)
       
        # расчет запаса прочности 
        # в будущем надо найти формулы для сигмы
        self.t_takeoff_mode = self.t_resource.value()*self.takeoff_rate.value()
        # для лопаток турбины высокого давления
        self.p_vd = self.t_lvd*(20*math.log(self.t_takeoff_mode))
        # для лопаток турбины низкого давления
        self.p_nd = self.t_lnd*(20*math.log(self.t_takeoff_mode))
        # запас прочности для высокого давления
        self.k_sigma_vd = round(self.sigma_tvd.value()/self.sigma_rvd, 4)
        self.k_sigma_nd = round(self.sigma_tnd.value()/self.sigma_rnd, 4)
        
        # расчет показателей цилка проектируемого трд и его перспективы
        # работа цикла ТРД по результатам газодинамического расчета
        self.l_c = (1-self.nu_mex.value())*self.l_tvd + (self.p_ud_poln*self.p_ud_poln)/2
        # внутренний (эффективный КПД)
        self.nu_vn = self.l_c*self.eta_g.value()/(self.q_ks*(10**3))
        # КПД процессов сжатия и расширения
        self.eta_c = ((((self.p_k_kvd/self.p_a)**((self.k.value()-1)/self.k.value())))-1)/((self.t_k_kvd/self.t_k)-1)
        self.eta_p = (1-(self.t_c/self.t_r.value()))/(1-(self.p_c/self.p_k_kvd)**((self.k_g.value()-1)/self.k_g.value()))
        # коэффициент , учитывающий различие физических свойств газа и воздуха
        self.m = (((self.k_g.value()/(self.k_g.value()-1))*self.r_g*(1-(self.p_c/self.p_k_kvd)
                    **((self.k_g.value()-1)/self.k_g.value())))
                  /((self.k.value()/(self.k.value()-1))*self.R*(1-(self.p_c/self.p_k_kvd)
                    **((self.k.value()-1)/self.k.value()))))
        # оптимальная степень повышения давления и максимальная работа цикла
        self.pi_opt = (round((self.m*(self.t_r.value()/self.t_k)
                              *self.eta_c*self.eta_p)**(self.k.value()
                                                        /(2*(self.k.value()-1))), 3))
        self.l_cmax = (int((self.k.value()/(self.k.value()-1))*self.R*self.t_k
                           *(((self.pi_opt**((self.k.value()-1)
                                             /self.k.value())) - 1)**2)/self.eta_c))
        # степень повышения давления, при которой имеет место максимальная экономичность двигателя (Суд min)
        self.a = self.m*(self.t_r.value()/self.t_k)*self.eta_p
        self.b = (self.a - math.sqrt((self.a**2) - 
                                     self.a*(self.a+1-(self.t_r.value()/self.t_k))
                                     *((self.t_r.value()/self.t_k)*self.eta_c+1-self.eta_c)))
        self.c = self.a + 1 - (self.t_r.value()/self.t_k)
        self.pi_nu_vn_max = round((self.b/self.c)**(self.k.value()/(self.k.value()-1)), 3)
        # внутренний КПД при Суд min
        self.d = ((self.k.value()/(self.k.value()-1))*self.R*(((self.pi_nu_vn_max
                                                                **((self.k.value()-1)/self.k.value()))-1)/self.eta_c)
                  *(((self.m*(self.t_r.value()/self.t_k)*self.eta_c*self.eta_p)/(self.pi_nu_vn_max
                                                                                 **((self.k.value()-1)/self.k.value())))-1))
        self.e = ((0.9+0.0001*self.t_k*(2*(self.t_r.value()/self.t_k)
                                        +1+(((self.pi_nu_vn_max**((self.k.value()-1)/self.k.value()))-1)/self.eta_c)))
                  *((self.t_r.value()/self.t_k)-(((self.pi_nu_vn_max
                                                   **((self.k.value()-1)/self.k.value()))-1)/self.eta_c)-1))
        self.nu_vn_max = round(self.d*0.001/self.e, 3)
        # проектируемый ТРД по своим параметрам рабочегопроцесса и энергетическим показателями отличается
        # от оптимальной величины степени повышения давления на
        self.delta_pi = int(round(((self.pi_k_sum.value() - self.pi_opt)/self.pi_opt), 2)*100)
        # от максимальной работы цикла на
        self.delta_l_c = int(round((self.l_cmax - self.l_c)/self.l_c, 2)*100)
        # от экономической степени повышения давления в
        self.delta_pi_econom = round((self.pi_nu_vn_max-self.pi_k_sum.value())/self.pi_k_sum.value(), 1)
        # от максимального значения внутреннего КПД на
        self.delta_nu = int(round((self.nu_vn_max-self.nu_vn)/self.nu_vn, 2)*100)
        
        # вывод итоговых параметров во второе окно
        self.label = QtWidgets.QLabel(self.output_window)
        self.label.setText('\tПроектируемый ТРД по своим параметрам рабочего процесса и энергетическим показателям отличается:\n' 
                           + '- от оптимальной величины степени повышения давления на {0} %;\n- от максимальной работы цикла на {1} %;\n'
                           .format(self.delta_pi, self.delta_l_c)
                           + '- от экономической степени повышения давления в {0} раз;\n- от максимального значения внутреннего КПД на {1} %.'
                           .format(self.delta_pi_econom, self.delta_nu))
        self.label.show()
        # реализация кнопки сохранения файла
        self.grid_l = QtWidgets.QGridLayout(self.output_window)
        
        self.save_from = QtWidgets.QPushButton('Cохранить файл')
        self.save_from.setToolTip('Нажмите кнопку, чтобы сохранить результат расчета в формате .txt')
        self.save_from.setToolTipDuration(-1)
        self.save_from.setGeometry(QtCore.QRect(140, 340, 80, 25))
        self.grid_l.addWidget(self.save_from, 0, 0)
        self.save_from.clicked.connect(self.save_file)
        
    
    # функция записи текста в файл    
    def save_file(self):
        name = QtWidgets.QFileDialog.getSaveFileName(None, 'SaveTextFile','/', "Text Files (*.txt)")[0]
        file = open(name, 'w')
        text = self.label.text()
        file.write(text)
        file.close()
    
    def btn_click_close(self):
        self.destroy()
        
# класс второго окна - вывода результата       
class output_window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вывод итоговых значений газодинамического расчета')
        self.setWindowIcon(QtGui.QIcon('era.jfif'))
        self.font = QtGui.QFont('Times New Roman')
        start_font_size = 14
        self.font.setPixelSize(start_font_size)
        self.k_font = start_font_size / 243
        self.setFixedSize(600, 300)
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # смена стиля
    app.setStyle('Fusion')
    # смена темы
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15,15,15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)      
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    main_window = window()
    main_window.setFixedSize(950, 650)
    main_window.show()
    sys.exit(app.exec_())