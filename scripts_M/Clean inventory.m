let
    Source = Csv.Document(File.Contents("B:\Users\aymen\Downloads\Clean_Inventory (1).csv"),[Delimiter=";", Columns=12, Encoding=1252, QuoteStyle=QuoteStyle.None]),
    #"En-têtes promus" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Type modifié" = Table.TransformColumnTypes(#"En-têtes promus",{{"Material_ID", type text}, {"Unit_Price", type text}, {"Stock_Levels", type text}, {"Lead_Time", type text}, {"Reorder_Point", type text}, {"Safety_Stock", type text}, {"Arrival Date", type date}, {"Ordering_Costs", type text}, {"Holding_Costs", type text}, {"Seasonality", type text}, {"Historical_Sales_Data", type text}, {"Supplier_ID", type text}})
in
    #"Type modifié"