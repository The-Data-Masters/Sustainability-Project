let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Equipements = Source{[Schema="dbo",Item="Dim_Equipements"]}[Data],
    #"Valeur remplacée" = Table.ReplaceValue(dbo_Dim_Equipements,".",",",Replacer.ReplaceText,{"CO2_Emissions_kg"}),
    #"Type modifié" = Table.TransformColumnTypes(#"Valeur remplacée",{{"CO2_Emissions_kg", type number}}),
    #"Erreurs remplacées" = Table.ReplaceErrorValues(#"Type modifié", {{"CO2_Emissions_kg", 0}}),
    #"Type modifié1" = Table.TransformColumnTypes(#"Erreurs remplacées",{{"Estimated_Lifetime_Years", type number}}),
    #"Erreurs remplacées1" = Table.ReplaceErrorValues(#"Type modifié1", {{"Estimated_Lifetime_Years", 0}}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Erreurs remplacées1",".",",",Replacer.ReplaceText,{"Energy_Consumption_kWh"}),
    #"Type modifié2" = Table.TransformColumnTypes(#"Valeur remplacée1",{{"Energy_Consumption_kWh", type number}}),
    #"Erreurs remplacées2" = Table.ReplaceErrorValues(#"Type modifié2", {{"Energy_Consumption_kWh", 0}}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Erreurs remplacées2","Système de Pu","Système de Pasteurisation",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2","Machine de m","Machine de Mélange Automatique",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","Machine dm","Machine de Mélange Automatique",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée5" = Table.ReplaceValue(#"Valeur remplacée4","Machine d'Inspv","Machine d'Inspection Visuelle",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée6" = Table.ReplaceValue(#"Valeur remplacée5","Pasteurisc","Pasteurisateur Lait",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée7" = Table.ReplaceValue(#"Valeur remplacée6","Pasteursi","Pasteurisateur Lait",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée8" = Table.ReplaceValue(#"Valeur remplacée7","Pasteurism","Pasteurisateur Lait",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée9" = Table.ReplaceValue(#"Valeur remplacée8","Robot de Pan","Robot de Palettisation",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée10" = Table.ReplaceValue(#"Valeur remplacée9","Robot de Par","Robot de Palettisation",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée11" = Table.ReplaceValue(#"Valeur remplacée10","Robot de Paz","Robot de Palettisation",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée12" = Table.ReplaceValue(#"Valeur remplacée11","Système de Pb","Système de Pasteurisation",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée13" = Table.ReplaceValue(#"Valeur remplacée12","Ligne de Prodl","Ligne de Production Yaourt",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée14" = Table.ReplaceValue(#"Valeur remplacée13","Machine df","Machine de Mélange Automatique",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée15" = Table.ReplaceValue(#"Valeur remplacée14","Pasteurisi","Pasteurisateur Lait",Replacer.ReplaceText,{"Equipment_Name"}),
    #"Valeur remplacée16" = Table.ReplaceValue(#"Valeur remplacée15","Système de Refrom","Système de Refroidissement Rapide",Replacer.ReplaceText,{"Equipment_Name"})
in
    #"Valeur remplacée16"