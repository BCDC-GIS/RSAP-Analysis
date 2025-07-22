import os
import arcpy

# ***** JURISDICTION INTERSECTION ONLY *****

arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26910)

# GDB for intermediate products
work_gdb = r"G:\2_EDIT\RSAP\Datasets_For_Upload\Work.gdb"

# GDB for final output datasets
output_gdb = r"G:\2_EDIT\RSAP\Datasets_For_Upload\RSAP_Datasets_For_Upload.gdb"

# City, county, OLU vector data with only the name fields as attributes
city,county,olu = r"G:\2_EDIT\RSAP\RSAP_ArcPro_Project\Updated_Boundaries.gdb\CityPlace_v3",r"G:\2_EDIT\RSAP\RSAP_ArcPro_Project\Updated_Boundaries.gdb\Counties_v2",r"G:\2_EDIT\RSAP\RSAP_ArcPro_Project\Updated_Boundaries.gdb\OLUs_V4"

# RSAP analysis boundary
rsap_boundary = r"G:\2_EDIT\RSAP\RSAP_ArcPro_Project\RSAP_ArcPro_Project.gdb\PlanningArea"

# Structure data inputs as such:
# "Dataset_Name_No_Spaces" : "File_path_no_spaces"
input_datasets = {
    "Bay_Trail": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Public_Access_Recreation\SF_BayTrail_MTC_2024.gdb\bay_trail",
#     "Active_Transportation":r"C:\Users\reganm\Downloads\drive-download-20241217T170105Z-001\Active_Transportation_MTC_2022.shp",
#     "BPAD":r"C:\Users\reganm\Downloads\drive-download-20241217T170105Z-001\BPAD_CLN_2018\CLN2_BPAD_release_Flat.shp",
#     "Waterfront_Park_PUA":r"C:\Users\reganm\Downloads\drive-download-20241217T170105Z-001\Waterfront_Park_PUA.gdb\Waterfront_Park_PUA",
#     "Water_Trail_SCC":r"C:\Users\reganm\Downloads\drive-download-20241217T170105Z-001\WaterTrail_SCC_2021.gdb\Water_Trail_SCC_2021"
}

for key in input_datasets:
    
    # ----Create field mappings----
    out_fms = arcpy.FieldMappings()
    
    # Measurement field mapping
    desc = arcpy.Describe(input_datasets[key])
    geomType = desc.shapeType
    msr_name = None
    if geomType=='Polygon':
        msr_name = 'area_acres'
    elif geomType=='Polyline':
        msr_name = 'length_mi'
    if msr_name:
        fm_measurement = arcpy.FieldMap()
        out_measurement = arcpy.Field()
        out_measurement.name = msr_name
        out_measurement.aliasName = msr_name
        out_measurement.type = "DOUBLE"  # Using DOUBLE for measurements
        fm_measurement.outputField = out_measurement
        out_fms.addFieldMap(fm_measurement)

    # City field mapping
    fm_city = arcpy.FieldMap()
    out_city = arcpy.Field()
    out_city.name = "city"
    out_city.aliasName = "city"
    out_city.type = "TEXT"
    out_city.length = 100  # Adjust length as needed
    fm_city.outputField = out_city
    out_fms.addFieldMap(fm_city)

    fm_city2 = arcpy.FieldMap()
    out_city2 = arcpy.Field()
    out_city2.name = "citylsad"
    out_city2.aliasName = "citylsad"
    out_city2.type = "TEXT"
    out_city2.length = 100
    fm_city2.outputField = out_city2
    out_fms.addFieldMap(fm_city2)

    # County field mapping
    fm_county = arcpy.FieldMap()
    out_county = arcpy.Field()
    out_county.name = "county"
    out_county.aliasName = "county"
    out_county.type = "TEXT"
    out_county.length = 100
    fm_county.outputField = out_county
    out_fms.addFieldMap(fm_county)

    fm_county2 = arcpy.FieldMap()
    out_county2 = arcpy.Field()
    out_county2.name = "countylsad"
    out_county2.aliasName = "countylsad"
    out_county2.type = "TEXT"
    out_county2.length = 100
    fm_county2.outputField = out_county2
    out_fms.addFieldMap(fm_county)

    # OLU field mapping
    fm_olu = arcpy.FieldMap()
    out_olu = arcpy.Field()
    out_olu.name = "olu"
    out_olu.aliasName = "olu"
    out_olu.type = "TEXT"
    out_olu.length = 100
    fm_olu.outputField = out_olu
    out_fms.addFieldMap(fm_olu)
    
    in_path = input_datasets[key]
    print(key)
    
    # ----- JURISDICTION INTERECTIONS -----
    print("Intersecting with OLUs...")
    olu_intersect = os.path.join(work_gdb,key + "_olu")
    if not arcpy.Exists(olu_intersect):
        arcpy.analysis.PairwiseIntersect([in_path,olu], olu_intersect, "NO_FID", "", "INPUT")
    
    print("Intersecting with counties...")
    county_intersect = os.path.join(work_gdb,key+"_county")
    if not arcpy.Exists(county_intersect):
        arcpy.analysis.PairwiseIntersect([olu_intersect,county], county_intersect, "NO_FID", "", "INPUT")
    
    print("Intersecting with cities...")
    city_intersect = os.path.join(work_gdb,key+"_city")
    if not arcpy.Exists(city_intersect):
        arcpy.analysis.PairwiseIntersect([county_intersect,city], city_intersect, "NO_FID", "", "INPUT")
    
    if msr_name:
        print("Adding measurement field...")
        print(msr_name)
        arcpy.management.AddField(city_intersect, msr_name, "DOUBLE")
        if "length" in msr_name:
            calc_sr = arcpy.SpatialReference(102005)
            arcpy.management.CalculateGeometryAttributes(city_intersect, [[msr_name,"LENGTH"]], "MILES_US","", calc_sr)
        elif "area" in msr_name:
            calc_sr = arcpy.SpatialReference(102003)
            arcpy.management.CalculateGeometryAttributes(city_intersect, [[msr_name,"AREA"]], "", "ACRES", calc_sr)
    
    # Measurement field mapping if applicable
    print("Finishing field mappings...")
    if msr_name:
        fm_measurement.addInputField(city_intersect, msr_name)

    # Administrative boundary field mappings
    input_fields = [f.baseName for f in arcpy.ListFields(input_datasets[key])]
    if "city_1" in input_fields:
        fm_city.addInputField(city_intersect, "city_1")
    else:
        fm_city.addInputField(city_intersect,"city")
        
    fm_city2.addInputField(city_intersect, "citylsad")
    if "county_1" in input_fields:
        fm_county.addInputField(city_intersect, "county_1")
    else:
        fm_county.addInputField(city_intersect,"county")
    fm_county2.addInputField(city_intersect, "countylsad")
    fm_olu.addInputField(city_intersect, "olu")

    for field in arcpy.ListFields(input_datasets[key]):
        if "OBJECTID" not in field.name and "Shape" not in field.name and "SHAPE" not in field.name and "FID" not in field.name:
            temp_fm = arcpy.FieldMap()
            out_fm = arcpy.Field()
            out_fm.name = field.name
            out_fm.type = field.type
            out_fm.aliasName = field.aliasName
            temp_fm.outputField = out_fm
            temp_fm.addInputField(city_intersect, field.baseName)
            out_fms.addFieldMap(temp_fm)

    out_data = os.path.join(output_gdb,key)
    arcpy.conversion.ExportFeatures(city_intersect, out_data, "", "", out_fms)

    # Delete intermediate products
    arcpy.management.Delete(county_intersect)
    arcpy.management.Delete(olu_intersect)
    arcpy.management.Delete(city_intersect)


