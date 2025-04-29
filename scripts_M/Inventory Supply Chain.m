let
    Source = Csv.Document(File.Contents("B:\Users\aymen\Desktop\bi\SAP MM PM\inventory_supply_chain_dataset (1) (1).csv"),[Delimiter=";", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"En-têtes promus" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Type modifié" = Table.TransformColumnTypes(#"En-têtes promus",{{"Material_ID", type text}, {"Unit_Price", type text}, {"Stock_Levels", Int64.Type}, {"Lead_Time", Int64.Type}, {"Reorder_Point", Int64.Type}, {"Safety_Stock", Int64.Type}, {"Arrival Date", type text}, {"Ordering_Costs", Int64.Type}, {"Holding_Costs", Int64.Type}, {"Seasonality", type text}, {"Historical_Sales_Data", Int64.Type}, {"Supplier_ID", type text}}),
    #"Valeur remplacée" = Table.ReplaceValue(#"Type modifié","","Unknown",Replacer.ReplaceValue,{"Material_ID"}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Valeur remplacée","","Unknown",Replacer.ReplaceValue,{"Unit_Price"}),
    #"Colonnes supprimées" = Table.RemoveColumns(#"Valeur remplacée1",{"Arrival Date"}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Colonnes supprimées","","SUPPLIER_20",Replacer.ReplaceValue,{"Supplier_ID"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2","Unknown","420",Replacer.ReplaceText,{"Unit_Price"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","420","420.66",Replacer.ReplaceText,{"Unit_Price"})
in
    #"Valeur remplacée4"