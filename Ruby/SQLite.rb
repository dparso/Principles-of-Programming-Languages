require 'sqlite3'

myDB = SQLite3::Database.new("Salary.db")
myDB.execute("create table if not exists SalaryTable (id integer primary key, name text, salary integer);")
myDB.execute("insert into SalaryTable (name, salary) values ('Alice', 5000);")
myDB.execute("insert into SalaryTable (name, salary) values ('David', 1000);")

rows = myDB.execute("select * from SalaryTable;")
puts rows