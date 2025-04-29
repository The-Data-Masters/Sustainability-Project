let
    Source = Csv.Document(File.Contents("B:\Users\aymen\Desktop\bi\SAP MM PM\facture.csv"),[Delimiter=";", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"En-têtes promus" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Valeur remplacée" = Table.ReplaceValue(#"En-têtes promus",".",",",Replacer.ReplaceText,{"Total"}),
    #"Type modifié" = Table.TransformColumnTypes(#"Valeur remplacée",{{"Total", Int64.Type}, {"Date", type date}}),
    #"Erreurs remplacées" = Table.ReplaceErrorValues(#"Type modifié", {{"Date", #date(2024, 12, 11)}}),
    #"Colonnes renommées" = Table.RenameColumns(#"Erreurs remplacées",{{"Numéro", "ID"}}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Colonnes renommées","326502","1",Replacer.ReplaceText,{"ID"}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Valeur remplacée1","117262","7",Replacer.ReplaceText,{"ID"}),
    #"Valeur remplacée3" = Table.ReplaceValue(#"Valeur remplacée2","Email","",Replacer.ReplaceText,{"Fournisseur"}),
    #"Valeur remplacée4" = Table.ReplaceValue(#"Valeur remplacée3","","info@racinesvertessarl.com",Replacer.ReplaceValue,{"Email"}),
    #"Colonnes supprimées" = Table.RemoveColumns(#"Valeur remplacée4",{"Client"}),
    #"Valeur remplacée5" = Table.ReplaceValue(#"Colonnes supprimées","","Agro Nature",Replacer.ReplaceValue,{"Fournisseur"}),
    #"Valeur remplacée6" = Table.ReplaceValue(#"Valeur remplacée5","D","Distributeurs SustainTech",Replacer.ReplaceText,{"Fournisseur"}),
    #"Type modifié1" = Table.TransformColumnTypes(#"Valeur remplacée6",{{"ID", type number}})
in
    #"Type modifié1"