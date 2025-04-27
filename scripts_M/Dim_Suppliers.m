let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Suppliers = Source{[Schema="dbo",Item="Dim_Suppliers"]}[Data],
    #"Doublons supprimés" = Table.Distinct(dbo_Dim_Suppliers, {"Supplier_Name"}),
    #"Valeur remplacée" = Table.ReplaceValue(#"Doublons supprimés","2015","Aucune",Replacer.ReplaceText,{"Environmental_Certifications"}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Valeur remplacée","","ISO 14001",Replacer.ReplaceValue,{"Environmental_Certifications"}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Valeur remplacée1","2005","Agriculture Biologique",Replacer.ReplaceText,{"Environmental_Certifications"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2","20 052 015","Agriculture Biologique",Replacer.ReplaceText,{"Environmental_Certifications"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","FSSC 22000","ISO 14001",Replacer.ReplaceText,{"Environmental_Certifications"})
in
    #"Valeur remplacée4"