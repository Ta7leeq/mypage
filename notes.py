if EinkauflisteCount!=0:
        
        
        print("missing ingredients",result) 

        #looping inside the list of ingredients IDs (which are in the selected recipie)
        for m in range(0,len(recipieIngredientIDList)):
            #looping insdie the Einkaufsliste table
            for l in range(0,EinkauflisteCount): 
                
                
                #printing item m in the list of ingredients Ids beside the item item l in the Einkaufsliste table column Ingredient ID to compare
                #print(recipieIngredientIDList[m],Einkaufliste[l][1])
                # compare item in the ingredients of the recipie with every item in the Einkaufsliste to check if it already exists in the list
                if recipieIngredientIDList[m]==float(Einkaufliste[l][1]):  
                    
                    print("Adding to existing")
                    #inserting new ingriedents in the Einkaufsliste
                    print("Einkaufliste[l][2]",Einkaufliste[l][3])
                    print("recipieIngredientIDList[m]",recipieIngredientIDList[m])

                    
                    Einkaufliste[l][2]=float(Einkaufliste[l][3])+ recipieIngredientQtyList[m]
                    #Einkaufliste[l][2]="0"
                    
                    target_id=Einkaufliste[l][0]
                    print("target_id",target_id)

                    sql = f"UPDATE {table} SET Qty='{Einkaufliste[l][2]}' WHERE ID={target_id}"
                    cursor.execute(sql)
                    cnxn.commit()
                else:
                    #This ingredient has not been add yet to the Einkaufsliste
                    #print(recipieIngredientIDList[m],Einkaufliste[l][1])
                    #print("to be added",recipieIngredientIDList[m])    
                    print()    
