from flask import Flask , render_template, request
import pyodbc
app=Flask(__name__)

# set up the connection
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\OneDrive\Desktop\New_Test_Project\Recipe.accdb;"
)


# set up a cursor object to execute SQL queries

cnxn = pyodbc.connect(conn_str)

# create a cursor object to execute SQL queries
cursor = cnxn.cursor()

# define your SQL query
query = 'SELECT * FROM Recipe'



i=None
@app.route('/index', methods=['GET', 'POST'])
           
def index():
    global i
    if i is None:
        i=1
    else:
        i=i
       
    # fetch a row from the database
    cursor.execute(query)
    row = cursor.fetchone()
    
    #print(row[1])
    
    if request.method == 'POST':

        if 'button1' in request.form:
        # Do something when the button is clicked
            i=i+1
            return render_template('show.html', header=row[i])
        elif 'button2' in request.form:
            i=i-1
            return render_template('show.html', header=row[i])
        else:
            return render_template('show.html', row=row)

       
    else:
        # Render the template with the button
        return render_template('index.html')

@app.route('/show', methods=['GET', 'POST'])
def show():

    # fetch a row from the database
    cursor.execute(query)
    row = cursor.fetchone()
    
    #print(row[1])

    if request.method == 'POST':
        # Do something when the button is clicked

        
        return render_template('show.html', header=row[3])
       
    else:
        # Render the template with the button
        return render_template('index.html')






if __name__ == '__main__':
    app.run()
