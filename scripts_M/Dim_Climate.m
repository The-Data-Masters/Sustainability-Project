let
    Source = Sql.Database("Asssouma", "SAP_DW"),
    dbo_Dim_Climate = Source{[Schema="dbo",Item="Dim_Climate"]}[Data]
in
    dbo_Dim_Climate