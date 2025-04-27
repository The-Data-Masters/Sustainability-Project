let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Reclamation = Source{[Schema="dbo",Item="Dim_Reclamation"]}[Data],
    #"Colonne conditionnelle ajoutée" = Table.AddColumn(dbo_Dim_Reclamation, "Personnalisé", each if [ID] = 1 then 1 else if [ID] = 2 then 1 else if [ID] = 3 then 1 else if [ID] = 4 then 2 else if [ID] = 5 then 2 else if [ID] = 6 then 2 else if [ID] = 7 then 2 else if [ID] = 8 then 2 else if [ID] = 9 then 3 else if [ID] = 10 then 2 else if [ID] = 11 then 2 else if [ID] = 12 then 2 else if [ID] = 13 then 2 else if [ID] = 14 then 2 else if [ID] = 15 then 2 else if [ID] = 16 then 1 else if [ID] = 17 then 2 else if [ID] = 18 then 2 else if [ID] = 19 then 2 else if [ID] = 20 then 3 else if [ID] = 21 then 2 else if [ID] = 22 then 2 else if [ID] = 23 then 2 else if [ID] = 24 then 2 else if [ID] = 25 then 2 else if [ID] = 26 then 2 else if [ID] = 27 then 2 else if [ID] = 28 then 2 else if [ID] = 29 then 2 else if [ID] = 30 then "" else null),
    #"Colonne conditionnelle ajoutée1" = Table.AddColumn(#"Colonne conditionnelle ajoutée", "Personnalisé 1", each if [ID] = 30 then 4 else if [ID] = 31 then 2 else if [ID] = 32 then 2 else if [ID] = 33 then 1 else if [ID] = 34 then 2 else null),
    #"Colonnes fusionnées" = Table.CombineColumns(Table.TransformColumnTypes(#"Colonne conditionnelle ajoutée1", {{"Personnalisé 1", type text}, {"Personnalisé", type text}}, "fr-FR"),{"Personnalisé 1", "Personnalisé"},Combiner.CombineTextByDelimiter("", QuoteStyle.None),"Fusionné"),
    #"Valeur remplacée" = Table.ReplaceValue(#"Colonnes fusionnées","","1",Replacer.ReplaceValue,{"Fusionné"}),
    #"Colonnes supprimées" = Table.RemoveColumns(#"Valeur remplacée",{"PRIOK"}),
    #"Colonnes renommées" = Table.RenameColumns(#"Colonnes supprimées",{{"Fusionné", "PRIOK"}}),
    #"Type modifié" = Table.TransformColumnTypes(#"Colonnes renommées",{{"PRIOK", Int64.Type}}),
    #"Duplication de la colonne" = Table.DuplicateColumn(#"Type modifié", "PRIOK", "PRIOK - Copier"),
    #"Type modifié1" = Table.TransformColumnTypes(#"Duplication de la colonne",{{"PRIOK - Copier", type text}}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Type modifié1","1","Critique",Replacer.ReplaceText,{"PRIOK - Copier"}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Valeur remplacée1","2","Élevée",Replacer.ReplaceText,{"PRIOK - Copier"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2","3","Moyenne",Replacer.ReplaceText,{"PRIOK - Copier"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","4","Faible",Replacer.ReplaceText,{"PRIOK - Copier"})
in
    #"Valeur remplacée4"