let
    Source = Table.FromRecords({
        [City="Sfax", Latitude="34.7333", Longitude="10.7667"],
        [City="Gabes", Latitude="33.8833", Longitude="10.1167"],
        [City="Tunis", Latitude="36.8065", Longitude="10.1815"],  // Nouvelle ligne
        [City="Nabeul", Latitude="36.4513", Longitude="10.7361"]  // Nouvelle ligne ajoutée
    }),
    #"Valeur remplacée" = Table.ReplaceValue(Source, "10.7667#(lf)10.7667#(lf)", "10.7667", Replacer.ReplaceText, {"Longitude"}),
    #"Valeur remplacée1" = Table.ReplaceValue(#"Valeur remplacée",".",",",Replacer.ReplaceText,{"Longitude"}),
    #"Type modifié" = Table.TransformColumnTypes(#"Valeur remplacée1",{{"Longitude", type number}}),
    #"Valeur remplacée2" = Table.ReplaceValue(#"Type modifié",".",",",Replacer.ReplaceText,{"Latitude"}),
    #"Type modifié1" = Table.TransformColumnTypes(#"Valeur remplacée2",{{"Latitude", type number}})
in
    #"Type modifié1"