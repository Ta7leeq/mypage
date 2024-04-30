from flask import Flask , render_template, request, send_from_directory, url_for, redirect, jsonify
import pyodbc
import os
from datetime import datetime 
from datetime import date
import datetime 
import time
import sys
import gc
from dateutil.parser import parse

from gtts import gTTS

import os
import pyttsx3


import requests
from flask import Flask
import json
from flask import request
print(datetime.__file__)

print(sys.version)

app=Flask(__name__)
app.static_folder = 'static'



# set up the connection
conn_str = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\OneDrive\Desktop\New_Test_Project\Recipe.accdb;"
)

Memo = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\Test\Links1.accdb;"
)



Soso = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\Test\Bears.accdb;"
)

Gaps = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\Test\gaps.accdb;"
)

Gaps02 = (
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\Users\User\Test\gaps02.accdb;"
)


# set up a cursor object to execute SQL queries

cnxn = pyodbc.connect(conn_str)
cnxn_memo=pyodbc.connect(Memo)
cnxn_soso=pyodbc.connect(Soso)
cnxn_gaps=pyodbc.connect(Gaps)
cnxn_gaps02=pyodbc.connect(Gaps02)

# create a cursor object to execute SQL queries
cursor = cnxn.cursor()


# define your SQL query
#query = "SELECT * FROM Recipe WHERE Recipe_Name= 'Okra with meatball'"
query1 = 'SELECT * FROM Recipe'
#query2 = "SELECT * FROM RecipeIngredient WHERE RecipeID=1"
query2 = 'SELECT * FROM RecipeIngredient'
query3 = 'SELECT * FROM Ingredient'

nav_id=None

@app.route('/', methods=['GET', 'POST'])
           
def index():

       
    # fetch a row from the database
    cursor.execute(query1)
    
    #row = cursor.fetchone()
    rows1=cursor.fetchall()
    #print (rows[0][1])
    image_path = "https://blog.hootsuite.com/wp-content/uploads/2021/07/free-stock-photos-03-scaled.jpeg"
    

    print(image_path)
    return render_template('index.html',step=rows1,image_path=image_path)
    

    
    #print(row[1])

def serve_image():
    return send_from_directory(app.static_folder + 'test.jpeg')

@app.route('/process_form', methods=['POST'])
def process_form():
    # fetch a row from the database


    cursor.execute(query1)
    rows1=cursor.fetchall() 

    cursor.execute(query2)
    rows2=cursor.fetchall()

    cursor.execute(query3)
    rows3=cursor.fetchall()


    selected_step = request.form['step_select']
    # Do something with the selected step value
    R=int(selected_step)

    cursor.execute("SELECT * FROM RecipeIngredient WHERE RecipeID=?", (R,))
    rows4=cursor.fetchall()
    
    
    
    x=0
    for i in range(len(rows4)):
        
        for j in range(len(rows3)):
            if (rows3[j][0]==rows4[i][1]):
                x=x+rows3[j][2]*rows4[i][2]

    print(x)            
                
        
    
    print(R)
    
    return render_template('process_form.html',step1=rows1[R-1],step2=rows2,step3=rows3,total=str(x))

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form['name-input']
    unit = request.form['unit-input']
    price = request.form['price-input']
    # Connect to the database
    conn = pyodbc.connect(conn_str)

    # Create a cursor object
    cursor = conn.cursor()

    cursor.execute("INSERT INTO Ingredient (Ingredient_Name,Ingredient_Unit,Ingredient_Price) VALUES (?,?,?)", (name,unit,price))
    # Commit the changes to the database
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

    return "Form submitted successfully"
    
@app.route('/Recipies')
def Recipies():

    # fetch a row from the database

    # fetch a row from the database
    cursor.execute(query1)
    
    #row = cursor.fetchone()
    rows1=cursor.fetchall()
    #name = request.form['name-input']

    return render_template('Recipies.html',step=rows1) 


@app.route('/Memory')
def Memory():
    
    nav_id = request.args.get('lang')
    if nav_id is None:
        nav_id = request.args.get('nav_id')
    else:
        nav_id = request.args.get('lang')
    
    print("nav_id",nav_id)
    
    table=nav_id
    
    # fetch a row from the database
    cursor_Memo = cnxn_memo.cursor()
    query_memo= f"SELECT * FROM {table}"
   
    cursor_Memo.execute(query_memo)
    
    #row = cursor.fetchone()
    rows=cursor_Memo.fetchall()
    
    
    today = datetime.datetime.today()
    today_str=today.strftime('%Y-%m-%d')
    #print(today)

    date_obj = {}
    due_rows={}
    next_date={}
    status={}
    counter=1

    for i in range(len(rows)):
        if rows[i][3] is not None and rows[i][4] is not None :
            date_obj[i] = parse(rows[i][3])
            next_date[i] = parse(rows[i][4])
            status[i]=""
            print( next_date[i])
            if next_date[i]<today: 
                due_rows[i]=rows[i]
                
        else:
            due_rows[i]=rows[i]
            status[i]="new"

    #print(list(status.values()))

    
    
       
    
    return render_template('Memory.html',step=list(due_rows.values()),table=table)
    #return render_template('Memory.html',step=rows) 

@app.route('/QuizMemory')
def QuizMemory():
    
    
    return render_template('QuizMemory.html')
       

@app.route('/finished', methods=['POST'])
def finished():
    
    #table="German"
    print("Quality",request.form['quality'])
    print("table",request.form['table'])
    table=request.form['table']
    quality = int(request.form['quality'])
    data = request.args.get('lang')
    print("data",data)
    nav_id=table
    
    #print(quality)
    
    
    
    button_id = int(request.form['button_id'])
    print(button_id)
    
    cursor_Memo = cnxn_memo.cursor()
    #query_memo=f'SELECT * FROM German'
    query_memo = f"SELECT * FROM {table}  WHERE id = {button_id}"
    print(query_memo)
    cursor_Memo.execute(query_memo)


    
    
    rows=cursor_Memo.fetchall()
    print(rows[0][3])

    today = datetime.datetime.today()
    #dateToday = datetime.datetime.strptime(today, "%Y-%m-%d %H:%M:%S.%f")
    
    if rows[0][3] is None:
        EF = 2.5 + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        print(EF)
        nextTime=today+datetime.timedelta(hours=24)
    

    else:
        dateLast = datetime.datetime.strptime(rows[0][3],"%Y-%m-%d %H:%M:%S.%f")
        EF = float(rows[0][5]) + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))                                    
        print(EF)
        space=today-dateLast
        space_hours=int(space.total_seconds() / 3600)
        nextTime=today+datetime.timedelta(hours=EF*space_hours)


        print(today)
        print(space)
        
        print(nextTime)


   

    sql = f"UPDATE {table} SET Next_Time='{nextTime}' WHERE ID={button_id}"
    cursor_Memo.execute(sql)
    cnxn_memo.commit()
    sql = f"UPDATE {table} SET Last_Time='{today}' WHERE ID={button_id}"
    cursor_Memo.execute(sql)
    cnxn_memo.commit()  
    sql = f"UPDATE {table} SET EF='{EF}' WHERE ID={button_id}"
    cursor_Memo.execute(sql)
    cnxn_memo.commit()  

    sql = f"UPDATE {table} SET status='' WHERE ID={button_id}"
    cursor_Memo.execute(sql)
    cnxn_memo.commit()  


    # Close the cursor and connection
    cursor_Memo.close()
    #cnxn_memo.close()

    #return "Form submitted successfully"
    return redirect(url_for('Memory',nav_id=nav_id))

@app.route('/Gaps', methods=['GET', 'POST'])
def Gaps():

    sentences = ["The quick brown _____ jumps over the lazy dog.", "I have a dream that one day _____ will live in a nation where they will not be judged by the color of their skin but by the content of their character.","The quick brown _____ jumps over the lazy dog."]
    sentence_answers = {"The quick brown _____ jumps over the lazy dog.": "fox", "I have a dream that one day _____ will live in a nation where they will not be judged by the color of their skin but by the content of their character.": "little children","The quick brown _____ jumps over the lazy dog.": "fox"}
    sentences_with_gaps = []
    for sentence in sentences:
        sentence_words = sentence.split()
        gap_index = sentence_words.index("_____")
        sentence_words[gap_index] = "%s"
        sentence_with_gap = " ".join(sentence_words)
        sentences_with_gaps.append(sentence_with_gap)
    if request.method == 'POST':
        user_answers = []
        for sentence in sentences:
            user_answer = request.form[sentence]
            user_answers.append(user_answer)
        answer_messages = []
        for i in range(len(sentences)):
            if user_answers[i] == sentence_answers[sentences[i]]:
                answer_message = "Correct!"
            else:
                answer_message = "Sorry, that's incorrect. The correct answer is '{}'".format(sentence_answers[sentences[i]])
            answer_messages.append(answer_message)
        return render_template('Gaps.html', sentences=sentences_with_gaps, answer_messages=answer_messages)
    else:
        return render_template('Gaps.html', sentences=sentences_with_gaps)
    

@app.route('/', methods=['POST'])
def check_answer():
    sentence = "The quick brown " + request.form['answer'].lower() + " jumps over the lazy dog."
    if request.form['answer'].lower() == 'fox':
        result = 'Correct!'
        color = 'green'
    else:
        result = 'Incorrect. Try again.'
        color = 'red'
    return render_template('Gaps.html', sentence=sentence, result=result, color=color)



@app.route('/Games')
def Games():
   

    
    return render_template('Games.html')

@app.route('/Bears',)
def Bears():

    #table="Score"
    #nav_id = request.args.get('lang')
    #if nav_id is None:
    #    nav_id = request.args.get('nav_id')
    #else:
    #    nav_id = request.args.get('lang')
    
    #print("nav_id",nav_id)
    # fetch a row from the database
    #cursor_Soso = cnxn_soso.cursor()
    #query_Soso= f"SELECT * FROM {table}"
   
    
    #cursor_Soso.execute(query_Soso)
    
    #row = cursor.fetchone()
    #rows=cursor_Soso.fetchall()
    
    #print(rows[0][2])
    #highestScore=max(rows[0][2],rows[1][2])
    #playerName = request.form['name']
    #print(playerName)
    
    
  
    return render_template('Bears.html')

@app.route('/Quiz',)
def Quiz():


    
    
  
    return render_template('Quiz.html')


@app.route('/Quiz02',)
def Quiz02():


    
    
  
    return render_template('Quiz02.html')

@app.route('/Bear_Name', methods=['POST'])
def Bear_Name():
    username = request.form['name']
    
    print(username)

    return  render_template('Bears.html')

@app.route('/Mal')
def Mal():
  
    return render_template('Mal.html')

@app.route('/send-data', methods=['POST'])
def receive_data():
    data= json.loads(request.data) 

    
    if (data['Name']=="Mody"):

        ID=2

    else:
        ID=3

    table="Score"
    # fetch a row from the database
    cursor_Soso = cnxn_soso.cursor()
    query_Soso= f"SELECT * FROM {table}"
   
    cursor_Soso.execute(query_Soso)
    
    rows=cursor_Soso.fetchall()
    
    
    highestScore=max(rows[0][2],rows[1][2])

    if (float(data['Score'])>float(highestScore)):
        highestScore=data['Score']
        print("HighScore",highestScore)
    
    sql = f"UPDATE {table} SET Highest_Score='{highestScore}' WHERE ID={ID}"
    cursor_Soso.execute(sql)
    cnxn_soso.commit()
    
    
    
    return  render_template('Bears.html')

@app.route('/get-data')
def get_data():
    
    table="Score"
    # fetch a row from the database
    cursor_Soso = cnxn_soso.cursor()
    query_Soso= f"SELECT * FROM {table}"
   
    cursor_Soso.execute(query_Soso)
    
    rows=cursor_Soso.fetchall()
    
    
    highestScore=max(rows[0][2],rows[1][2])
    print(rows[0][2])
    print(rows[1][2])
    if rows[0][2]>rows[1][2]:
        name ="Mody"
    else:
        name ="Soso"


    data = {"message": highestScore, "id": name}
    
    return jsonify(data)


@app.route('/get-ingredients')
def get_ingredients():
    
    table="Ingredient"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    queryCount = f"SELECT COUNT(*) FROM {table}"

    cursor.execute(queryCount)
    row_count = cursor.fetchone()[0]
    print(row_count)
   
    cursor.execute(query)
    rows=cursor.fetchall()

    # Create an empty list
    ingredientslist = []
    ingredientsIdlist = []

    # Use a for loop to fill the list
    for i in range(-8, row_count-8):
        ingredientslist.append(rows[i][1])
        #print(rows[i][1])
        ingredientsIdlist.append(rows[i][0])
        #print(rows[i][0])
    
    
    table="Recipe"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    queryCount = f"SELECT COUNT(*) FROM {table}"

    cursor.execute(queryCount)
    RecipiesCount = cursor.fetchone()[0]

    cursor.execute(query)
    rowsRecipies=cursor.fetchall()

    # Create an empty list
    recipiesList = []
    recipiesIDList = []
    
    # Use a for loop to fill the list
    for j in range(-1, RecipiesCount):
        recipiesList.append(rowsRecipies[j][1])
        #print(rows[i][1])
        recipiesIDList.append(rowsRecipies[j][0])
        #print(rows[i][0])
    
    data = {"message": rows[-6][2],"numberOfRows":row_count,"Ingredients":ingredientslist,"IngredientIds":ingredientsIdlist
            ,"numberOfRowsRecipies":RecipiesCount
            ,"Recipies":recipiesList
            ,"RecipiesIds":recipiesIDList
            }


    
    
    return jsonify(data)

@app.route('/send-ingredients', methods=['POST'])
def send_ingredients():
    data= json.loads(request.data) 
    print(data)
    recipieId=int(data['RecipieName'])
    addIngredient=data['IngredientName']
    quantity=data['Quantity']
    
    
    


    table="Recipe"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    cursor.execute(query)
    
    rows=cursor.fetchall()

    
    
    #cursor.execute("INSERT INTO Recipe (Recipe_Name) VALUES (?)", (recipieName))

    cnxn.commit()

    table="RecipeIngredient"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    cursor.execute(query)
    cursor.execute("INSERT INTO RecipeIngredient (RecipeID,IngredientID,Quantity) VALUES (?,?,?)", (recipieId,addIngredient,quantity))
    cnxn.commit()

    
    
    return "Ingredients submitted successfully"


@app.route('/einkaufsWagen', methods=['POST'])
def einkaufsWagen():
    data= json.loads(request.data) 
    
    recipieId=data['einkaufsWagenItems']
    #print(recipieId)
    
    table="RecipeIngredient"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    queryCount = f"SELECT COUNT(*) FROM {table}"

    cursor.execute(queryCount)
    RecipeIngredientCount = cursor.fetchone()[0]

    cursor.execute(query)
    rowsRecipeIngredient=cursor.fetchall()
    
    table="Einkaufliste"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query= f"SELECT * FROM {table}"
    queryCount = f"SELECT COUNT(*) FROM {table}"
    cursor.execute(queryCount)
    EinkauflisteCount = cursor.fetchone()[0]
    cursor.execute(query)
    Einkaufliste=cursor.fetchall()

    table01="Ingredient"
    # fetch a row from the database
    cursor = cnxn.cursor()
    query01= f"SELECT * FROM {table01}"
    queryCount01 = f"SELECT COUNT(*) FROM {table01}"
    cursor.execute(queryCount01)
    IngredientCount = cursor.fetchone()[0]
    cursor.execute(query01)
    Ingredient=cursor.fetchall()

    
    
    EinaufsIdList = []
    
    
    
    for A in range(0, EinkauflisteCount):
        
        EinaufsIdList.append(int(Einkaufliste[A][1]))

    IngredientIdList=[]
    IngredientNameList=[]
    IngredientPriceList=[]
    IngredientUnitList=[]
    IngredientQuelleList=[]
    IngredientAbteilungList=[]
    
    for B in range(0, IngredientCount):
        
        IngredientIdList.append(int(Ingredient[B][0]))
        IngredientNameList.append(Ingredient[B][1])
        IngredientPriceList.append(Ingredient[B][2])
        IngredientUnitList.append(Ingredient[B][3])
        IngredientQuelleList.append(Ingredient[B][4])
        IngredientAbteilungList.append(Ingredient[B][5])


        #print(Ingredient[B])

    

    # Create an empty list
    recipieIngredientQtyList = []
    recipieIngredientIDList = []
    ID=[]
    ID01=[]    
    # looping inside the ReipieIngredient table 
    for k in range(0, RecipeIngredientCount):
        
        
        # Checking the Id of the Recipie inside the RecipieIngredient table matches the selected Recipie

        if rowsRecipeIngredient[k][0]==int(recipieId):

            #print(rowsRecipeIngredient[k][0],rowsRecipeIngredient[k][1],rowsRecipeIngredient[k][2])  #print out the Recipie ID, All the ingredients in the recipie , their quantiteis
            recipieIngredientIDList.append(int(rowsRecipeIngredient[k][1])) # fill a list all ingredients IDs
            recipieIngredientQtyList.append(rowsRecipeIngredient[k][2]) # fill a list all ingredients Quantities
            
            #Insert the IDs and the quantities of the ingredients in the Einkaufliste table
            #cursor.execute("INSERT INTO Einkaufliste (ItemId,Qty) VALUES (?,?)", (rowsRecipeIngredient[k][1],rowsRecipeIngredient[k][2]))
            #cnxn.commit()
    recipieIngredient = {recipieIngredientIDList: recipieIngredientQtyList for recipieIngredientIDList, recipieIngredientQtyList in zip(recipieIngredientIDList, recipieIngredientQtyList)}        
    ingredientName={IngredientIdList: IngredientNameList for IngredientIdList, IngredientNameList in zip(IngredientIdList, IngredientNameList)}
    ingredientUnit={IngredientIdList: IngredientUnitList for IngredientIdList, IngredientUnitList in zip(IngredientIdList, IngredientUnitList)}
    ingredientPrice={IngredientIdList: IngredientPriceList for IngredientIdList, IngredientPriceList in zip(IngredientIdList, IngredientPriceList)}
    
    ingredientQuelle={IngredientIdList: IngredientQuelleList for IngredientIdList, IngredientQuelleList in zip(IngredientIdList, IngredientQuelleList)}
    ingredientAbteilung={IngredientIdList: IngredientAbteilungList for IngredientIdList, IngredientAbteilungList in zip(IngredientIdList, IngredientAbteilungList)}

    #print("recipieIngredient",recipieIngredient)
    #print(ingredientName)
        
    
                            
    if EinkauflisteCount==0:
        #print("new")
        #inserting new ingriedents in the Einkaufsliste
        for m in range(0,len(recipieIngredientIDList)):
            cursor.execute("INSERT INTO Einkaufliste (ItemId,Qty) VALUES (?,?)", (recipieIngredientIDList[m],recipieIngredientQtyList[m]))
            cnxn.commit()
        print("==0")

    

    else:
        print("Else")
        result = list(set(recipieIngredientIDList) - set(EinaufsIdList))
        for m in range(0,len(result)):
            cursor.execute("INSERT INTO Einkaufliste (ItemId,Qty) VALUES (?,?)", (result[m],0))
            cnxn.commit()

        cursor.execute(query)
        Einkaufliste=cursor.fetchall()
        #queryCount = f"SELECT COUNT(*) FROM {table}"
        #cursor.execute(queryCount)
        #EinkauflisteCount = cursor.fetchone()[0]    

        
        for ID in Einkaufliste:
            print("ID",ID)
            #print(recipieIngredientIDList)
            if (int(ID[1]) in recipieIngredientIDList):
                
                ID[3]=float(ID[3])+float(recipieIngredient[int(ID[1])])

                
                sql = f"UPDATE {table} SET Qty='{ID[3]}' WHERE ID={ID[0]}"
                cursor.execute(sql)
                cnxn.commit()

        for ID01 in Einkaufliste:
            #print("ID01",ID01)
            #print(recipieIngredientIDList)
            
            
            
            
            
            #if (int(ID01[1]) ==IngredientNameList[int(ID01[1])]):
                
            inName=ingredientName[int(ID01[1])]
            inUnit=ingredientUnit[int(ID01[1])]
            inPrice=ingredientPrice[int(ID01[1])]
            inQuelle=ingredientQuelle[int(ID01[1])]
            inAbteilung=ingredientAbteilung[int(ID01[1])]

            print("Fill table",table,ID01[0],inName,inUnit,inPrice)
            #inName=result_list[int(ID01[1])][1]
            #print(inName,ID01[1])
            sql = f"UPDATE {table} SET Ingredient_Name='{inName}' WHERE ID={ID01[0]}"
            cursor.execute(sql)
            cnxn.commit()
            sql = f"UPDATE {table} SET Unit='{inUnit}' WHERE ID={ID01[0]}"
            cursor.execute(sql)
            cnxn.commit()
            sql = f"UPDATE {table} SET Price='{inPrice}' WHERE ID={ID01[0]}"
            cursor.execute(sql)
            cnxn.commit()

            sql = f"UPDATE {table} SET Laden='{inQuelle}' WHERE ID={ID01[0]}"
            cursor.execute(sql)
            cnxn.commit()

            sql = f"UPDATE {table} SET Abteilung='{inAbteilung}' WHERE ID={ID01[0]}"
            cursor.execute(sql)
            cnxn.commit()
            
            
                
                     




        

          

    
    return "Ingredients submitted successfully"


@app.route('/get-questions', methods=['GET', 'POST'])
def get_questions():
    #excerciseName=""
    #data= json.loads(request.data) 
    
    #excerciseName=data['Name']
    if request.method == 'POST':
        
        data= json.loads(request.data) 
    
        excerciseName=data['Name']
        table=excerciseName
        print(excerciseName)
        table=excerciseName
        # fetch a row from the database
        cursor_Gaps = cnxn_gaps.cursor()
        query= f"SELECT * FROM {table}"
        
        queryCount = f"SELECT COUNT(*) FROM {table}"

        cursor_Gaps.execute(queryCount)
        row_count = cursor_Gaps.fetchone()[0]
        #print(row_count)
    
        cursor_Gaps.execute(query)
        rows=cursor_Gaps.fetchall()

        print(rows)
        gapWordsList = []
        sentecelist = []
        photolist=[]
        
        # Use a for loop to fill the list
        for i in range(0, row_count):
            gapWordsList.append(rows[i][1])
            #print(rows[i][1])
            sentecelist.append(rows[i][2])
            print(rows[i][2])
            if rows[i][3] != None:
                photolist.append(rows[i][3])

        print(sentecelist)
        data = {"gapWord": gapWordsList,"sentence": sentecelist,"Photos": photolist}

        return jsonify(data)
    
    else:
        
        
        cursor_Gaps = cnxn_gaps.cursor()
        
        table_names = [table.table_name for table in cursor_Gaps.tables(tableType='TABLE')]


        data = {"tables": table_names}
        

        
        
        return jsonify(data)
    
@app.route('/get-questions02', methods=['GET', 'POST'])
def get_questions02():
    today = datetime.datetime.today()
    if request.method == 'POST':
        
        data= json.loads(request.data) 
    
        table=data['Name']
        score=data['Score']
        counter=data['Counter']

        #print(counter,score)
        
        # fetch a row from the database
        cursor_Gaps02 = cnxn_gaps02.cursor()
        query= f"SELECT * FROM {table}"
        
        queryCount = f"SELECT COUNT(*) FROM {table}"

        cursor_Gaps02.execute(queryCount)
        row_count = cursor_Gaps02.fetchone()[0]
        print("count",row_count)
    
        cursor_Gaps02.execute(query)
        rows=cursor_Gaps02.fetchall()

        print(rows)
        QuestionList = []
        AnswerList = []
        photolist=[]
        id=1
        
        
        if counter==row_count and score>=85:
            #print("score is",score)
            #Write score on the Database

            if rows[0][5] is None:
                EF = 2.5 + (0.1 - (5 - 3) * (0.08 + (5 - 3) * 0.02))
                print(EF)
                nextTime=today+datetime.timedelta(hours=24)

                sql = f"UPDATE {table} SET lastTime='{today}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()

                sql = f"UPDATE {table} SET nextTime='{nextTime}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()

                sql = f"UPDATE {table} SET Score='{score}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()

                
                

            else:
                dateLast = datetime.datetime.strptime(rows[0][5],"%Y-%m-%d %H:%M:%S.%f")
                EF = float(rows[0][5]) + (0.1 - (5 - 3) * (0.08 + (5 - 3) * 0.02))                                    
                print(EF)
                space=today-dateLast
                space_hours=int(space.total_seconds() / 3600)
                nextTime=today+datetime.timedelta(hours=EF*space_hours)

                sql = f"UPDATE {table} SET lastTime='{today}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()

                sql = f"UPDATE {table} SET nextTime='{nextTime}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()

                sql = f"UPDATE {table} SET Score='{score}' WHERE ID={id}"
                cursor_Gaps02.execute(sql)
                cnxn_gaps02.commit()


                print(today)
                print(space)
                
                print(nextTime)
            
        

            


        # Use a for loop to fill the list
        for i in range(0, row_count):
            QuestionList.append(rows[i][1])
            #print(rows[i][1])
            AnswerList.append(rows[i][2])
            #print(rows[i][2])
            if rows[i][3] != None:
                photolist.append(rows[i][3])


        

        # Text to be read aloud
        
        
        data = {"Question": QuestionList,"Answer": AnswerList,"Photos": photolist,"count":row_count}
        #os.remove("C:/Users/User/Test/output07.mp3")
        #gc.collect()  # Manually trigger garbage collection
        if counter<row_count:
            tts = gTTS(AnswerList[counter], lang='de', tld='de')
            print(AnswerList[counter])

            tts.save("C:/Users/User/Test/output07.mp3")   

        return jsonify(data)
    
    else:
        
        reviewList = []
        
        cursor_Gaps02 = cnxn_gaps02.cursor()
        
        table_names = [table.table_name for table in cursor_Gaps02.tables(tableType='TABLE')]
        print(table_names)
        for t in table_names:
            
            table=t
            # fetch a row from the database
            cursor_Gaps02 = cnxn_gaps02.cursor()
            query= f"SELECT * FROM {table}"
            
            cursor_Gaps02.execute(query)
            rows=cursor_Gaps02.fetchall()
            
            if rows[0][6] != None :
                
                nextTime=datetime.datetime.strptime(rows[0][6], "%Y-%m-%d %H:%M:%S.%f")
                if nextTime<today:#float(rows[0][4])<90: 
                    reviewList.append(t)
            else:
                reviewList.append(t)    
        
        print(reviewList)
        

        data = {"tables": table_names,"rTables": reviewList}
        
                
        return jsonify(data)


       
if __name__ == '__main__':
    app.run(debug=False)
    #app.run(host='127.0.0.1', port=5001)
