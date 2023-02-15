import pyodbc


c = pyodbc.connect('DSN=DOMA;UID=pb;PWD=pbvaje')
cursor = c.cursor()




def podatki_zaposlenih(mesec, leto):
    query = "SELECT d.dept_no, COUNT(DISTINCT e.emp_no) FROM employees e INNER JOIN dept_emp d_e USING(emp_no) INNER JOIN departments d USING(dept_no) WHERE ((YEAR(d_e.to_date)="+ str(leto) + " AND MONTH(d_e.to_date)>=" + str(mesec) + ") OR YEAR(d_e.to_date)>" + str(leto) + ") AND ((YEAR(d_e.from_date)=" + str(leto) + " AND MONTH(d_e.from_date)<=" + str(mesec) + ") OR YEAR(d_e.from_date)<" + str(leto) + ") GROUP BY d.dept_name;"
    rezultat = cursor.execute(query)
    return rezultat




def najdi_vse():
    po_letih_in_mesecih = {}
    prvi_hire_date = cursor.execute("SELECT MIN(hire_date) FROM employees;")
    for x in prvi_hire_date:
        leto_hire = x[0].year
    zadnji_to_date = cursor.execute("SELECT MAX(to_date) FROM titles WHERE to_date != '9999-01-01'")
    for x in zadnji_to_date:
        leto_to = x[0].year
    for leto in range(leto_hire, leto_to+1):
        for mesec in range(1,13):
            podatki = podatki_zaposlenih(mesec, leto)
            for department in podatki:
                po_letih_in_mesecih[str(mesec)+"."+str(leto)+" "+department[0]] = department[1]
    return po_letih_in_mesecih



print(najdi_vse()[input("Vnesi željeno poizvedbo v formatu month.year dept_no: ")])


c.commit()
c.close()
