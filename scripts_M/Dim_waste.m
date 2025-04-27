let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Waste = Source{[Schema="dbo",Item="Dim_Waste"]}[Data]
in
    dbo_Dim_Waste