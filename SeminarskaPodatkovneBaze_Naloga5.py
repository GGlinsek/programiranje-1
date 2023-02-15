import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QComboBox,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QWidget,QGridLayout
)

import pyodbc


c = pyodbc.connect('DSN=DOMA;UID=pb;PWD=pbvaje')
cursor = c.cursor()


def podatki_zaposlenih(mesec, leto):
    query1 = "SELECT d.dept_no, COUNT(DISTINCT e.emp_no) FROM employees e INNER JOIN dept_emp d_e USING(emp_no) INNER JOIN departments d USING(dept_no) WHERE ((YEAR(d_e.to_date)=" + str(
        leto) + " AND MONTH(d_e.to_date)>=" + str(mesec) + ") OR YEAR(d_e.to_date)>" + str(
        leto) + ") AND ((YEAR(d_e.from_date)=" + str(leto) + " AND MONTH(d_e.from_date)<=" + str(
        mesec) + ") OR YEAR(d_e.from_date)<" + str(leto) + ") GROUP BY d.dept_name;"

    rezultat = cursor.execute(query1)
    return rezultat


def najdi_vse(dept):
    po_letih_in_mesecih = {}
    prvi_hire_date = cursor.execute("SELECT MIN(hire_date) FROM employees;")
    for x in prvi_hire_date:
        leto_hire = x[0].year
    zadnji_to_date = cursor.execute("SELECT MAX(to_date) FROM titles WHERE to_date != '9999-01-01'")
    for x in zadnji_to_date:
        leto_to = x[0].year
    for leto in range(leto_hire, leto_to + 1):
        for mesec in range(1, 13):
            podatki = podatki_zaposlenih(mesec,leto)
            for department in podatki:
                po_letih_in_mesecih[str(mesec) + "." + str(leto) + " " + department[0]] = department[1]
    return po_letih_in_mesecih


departments = []
for department in cursor.execute("SELECT dept_no FROM departments ORDER BY dept_no"):
    departments.append(department[0])

def neki(vrednosti):
    x = []
    y = {}
    for key, value in vrednosti.items():
        if key.split(" ")[0] not in x:
            x.append(key.split(" ")[0])
        if key.split(" ")[1] not in y:
            y[key.split(" ")[1]] = []
        y[key.split(" ")[1]].append(value)
    return x,y


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Prikaz grafov")

        layout = QGridLayout()
        SpinBoxLeto = QSpinBox()
        SpinBoxLeto.setMinimum(1985)
        SpinBoxLeto.setMaximum(2002)
        SpinBoxMesec = QSpinBox()
        SpinBoxMesec.setMinimum(1)
        SpinBoxMesec.setMaximum(12)
        izbiraOddelka = QComboBox()
        izbiraOddelka.addItems(departments)
        button1 = QPushButton("Prikaži graf zaposlenih v vseh oddelkih v tem letu in mesecu")
        button1.setCheckable(True)
        button1.clicked.connect(lambda: graf_zaposlenih_mesecu_letu(SpinBoxMesec.value(),SpinBoxLeto.value()))
        button2 = QPushButton("Prikaži graf gostote zaposelnih v vseh letih v oddelku")
        button2.setCheckable(True)
        button2.clicked.connect(lambda: graf_gostote_oddelka_v_vseh_letih(izbiraOddelka.currentText()))

        widget = QWidget()
        layout.addWidget(SpinBoxLeto, 0,0)
        layout.addWidget(SpinBoxMesec,0,1)
        layout.addWidget(izbiraOddelka,1,0)
        layout.addWidget(button1 ,0,2)
        layout.addWidget(button2,1,2)



        widget.setLayout(layout)
        self.setCentralWidget(widget)

        def graf_zaposlenih_mesecu_letu(mesec, leto):
            podatki = podatki_zaposlenih(mesec, leto)

            oddelek = []
            stevilo_zaposlenih = []
            for x in podatki:
                oddelek.append(x[0])
                stevilo_zaposlenih.append(x[1])
            plt.bar(oddelek,stevilo_zaposlenih)
            plt.title("graf zaposlenih "+ str(mesec) + "." + str(leto))
            plt.show()


        def graf_gostote_oddelka_v_vseh_letih(oddelki):
            x,y = neki(najdi_vse(oddelki))
            plt.plot(x,y[oddelki])
            plt.title("število zaposlenih v oddelku "+ oddelki + " skozi čas")
            plt.show()





app = QApplication(sys.argv)
window = MainWindow()
window.show()


app.exec()


c.commit()
c.close()