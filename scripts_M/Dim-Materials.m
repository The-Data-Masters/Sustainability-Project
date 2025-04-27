let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Materials = Source{[Schema="dbo",Item="Dim_Materials"]}[Data],
    #"Type modifié" = Table.TransformColumnTypes(dbo_Dim_Materials,{{"Carbon_Footprint_per_Unit_kgCO2e", type number}}),
    #"Erreurs remplacées" = Table.ReplaceErrorValues(#"Type modifié", {{"Carbon_Footprint_per_Unit_kgCO2e", 0}}),
    #"Valeur remplacée" = Table.ReplaceValue(#"Erreurs remplacées",".",",",Replacer.ReplaceText,{"Total_Stock_Value"}),
    #"Type modifié1" = Table.TransformColumnTypes(#"Valeur remplacée",{{"Total_Stock_Value", type number}}),
    #"Erreurs remplacées1" = Table.ReplaceErrorValues(#"Type modifié1", {{"Total_Stock_Value", 0}}),
    #"Type modifié2" = Table.TransformColumnTypes(#"Erreurs remplacées1",{{"Transport_Distance", type number}}),
    #"Erreurs remplacées2" = Table.ReplaceErrorValues(#"Type modifié2", {{"Transport_Distance", 0}}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Erreurs remplacées2",".",",",Replacer.ReplaceText,{"Unit_Price"}),
    #"Type modifié3" = Table.TransformColumnTypes(#"Valeur remplacée1",{{"Unit_Price", type number}}),
    #"Erreurs remplacées3" = Table.ReplaceErrorValues(#"Type modifié3", {{"Unit_Price", 0}}),
    #"Type modifié4" = Table.TransformColumnTypes(#"Erreurs remplacées3",{{"Safety_Stock", type number}, {"Stock_Levels", type number}, {"Holding_Costs", type number}, {"Ordering_Costs", type number}}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Type modifié4","Unknown","Ferments lactiques",Replacer.ReplaceText,{"Material_Name"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2",null,0,Replacer.ReplaceValue,{"Carbon_Footprint_per_Unit_kgCO2e"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","","0",Replacer.ReplaceValue,{"Stock_Initial"}),
    #"Valeur remplacée5" = Table.ReplaceValue(#"Valeur remplacée4","a","",Replacer.ReplaceText,{"Stock_Initial"}),
    #"Valeur remplacée6" = Table.ReplaceValue(#"Valeur remplacée5","m","",Replacer.ReplaceText,{"Stock_Initial"}),
    #"Type modifié5" = Table.TransformColumnTypes(#"Valeur remplacée6",{{"Stock_Initial", type number}}),
    #"Erreurs remplacées4" = Table.ReplaceErrorValues(#"Type modifié5", {{"Stock_Initial", 120}}),
    #"Valeur remplacée7" = Table.ReplaceValue(#"Erreurs remplacées4",null,0,Replacer.ReplaceValue,{"Total_Stock_Value"})
in
    #"Valeur remplacée7"