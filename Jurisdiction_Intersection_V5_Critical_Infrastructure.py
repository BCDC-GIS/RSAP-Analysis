import os
import arcpy

# ***** JURISDICTION + HAZARD INTERSECTION *****

arcpy.env.parallelProcessingFactor = "80%"
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26910)

# GDB for intermediate products
work_gdb = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Workspace.gdb"

# GDB for final output datasets
output_gdb = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Critical_Infrastructure\Critical_Infrastructure.gdb"

# City, county, OLU vector data with only the name fields as attributes
city,county,olu = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Boundaries\Updated_Boundaries_121624\Geographic_Boundaries.gdb\CityPlace_v3",r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Boundaries\Updated_Boundaries_121624\Geographic_Boundaries.gdb\Counties_v2",r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Boundaries\Updated_Boundaries_121624\Geographic_Boundaries.gdb\OLUs_v4"

# RSAP analysis boundary
rsap_boundary = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Boundaries\RSAP_Boundaries.gdb\RSAP_PlanningArea_ocean"

# Structure data inputs as such:
# "Dataset_Name_No_Spaces" : "File_path_no_spaces"
input_datasets = {
    #"Cell_Towers":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Cell_towers_HIFLD_2022.gdb\Cellular_Towers",
    #"Substations":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Substations_Final_CEC_SFBay_clip",
    #"Power_plants":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Critical_Infrastructure_California_Power_Plants_CEC_SFBay_clip",
    #"Water_Related_Industry_PUA":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\BayPlan_PUA_BCDC_2023.gdb\BayPlan_PUA",
    #"Fire_Stations":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Critical_Infrastructure_Fire_Stations_SFBay_clip",
    #"Police_Stations":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Critical_Infrastructure_Local_Law_Enforcement_SFBay_clip",
    #"Natural_Gas_Stations":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Critical_Infrastructure_Natural_Gas_Station_CEC_SFBay_clip",
    #"Healthcare_Facilities":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Critical_Infrastructure_OSHPD_Healthcare_Facilities_SFBay_clip",
    #"Oil_Refineries":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Critical_infrastructure_source.gdb\Oil_Refineries_BCDC_2024",
    "Granted_Lands":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Granted_Lands_SLC_2023.gdb\Granted_Lands"
    #"Emergency_Operations_Centers":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\Local_Emergency_Operations_Centers_CalOES_2024.gdb\Local_EOC",
    #"Publicly_Owned_Wastewater_Treatment_Works":r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Critical_Infrastructure\POTW_Wet_Weather_Facilities_BACWA_2024.gdb\Wastewater_Treatment_BACWA_2024"
}

# Path to the SRP datasets - key needs to match the input_datasets precisely
srp_datasets = {
    #"Emergency_Operations_Centers": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\StrategicRegionalPriorities\Critical_Infrastructure\SRP_Critical_Infrastructure.gdb\Emergency_Operating_Centers",
    #"Healthcare_Facilities": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\StrategicRegionalPriorities\Critical_Infrastructure\SRP_Critical_Infrastructure.gdb\Healthcare",
    #"Power_plants": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\StrategicRegionalPriorities\Critical_Infrastructure\SRP_Critical_Infrastructure.gdb\Power_plants",
    #"Publicly_Owned_Wastewater_Treatment_Works": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\StrategicRegionalPriorities\Critical_Infrastructure\SRP_Critical_Infrastructure.gdb\Wastewater",
    #"Water_Related_Industry_PUA": r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\StrategicRegionalPriorities\Critical_Infrastructure\SRP_Critical_Infrastructure.gdb\Water_Related_Industry"
}

# These field names need to match between the SRP and original dataset
srp_id_fields = {
    #"Emergency_Operations_Centers" : "ID",
    #"Healthcare_Facilities": "oshpd_id",
    #"Power_plants": "CECPlantID",
    #"Publicly_Owned_Wastewater_Treatment_Works": "Facility_Name",
    #"Water_Related_Industry_PUA": "PUA_Number"
}

# Path to coastal hazards with bridge polygons removed
slr_6p6ft= r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Coastal_Flood_Hazards\Coastal_Hazards_NoBridges_v2.gdb\NoBridge_RSAP_6p6ft_SLR_Bay_CombinedHazards"
slr_4p9ft= r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Coastal_Flood_Hazards\Coastal_Hazards_NoBridges_v2.gdb\NoBridge_RSAP_4p9ft_SLR_Bay_CombinedHazards"
slr_3p1ft= r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Coastal_Flood_Hazards\Coastal_Hazards_NoBridges_v2.gdb\NoBridge_RSAP_3p1ft_SLR_Bay_CombinedHazards"
slr_0p8ft= r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\0_SourceData\Coastal_Flood_Hazards\Coastal_Hazards_NoBridges_v2.gdb\NoBridge_RSAP_0p8ft_SLR_Bay_CombinedHazards"

def checkForSRPs(input_dataset,SRP_dataset, SRP_ID):
    
    with arcpy.da.SearchCursor(SRP_dataset,[SRP_ID]) as cursor:
        
        for row in cursor:
            
            current_id = row[0]
            
            with arcpy.da.UpdateCursor(input_dataset,[SRP_ID,'srp']) as cursor2:
                
                for row2 in cursor2:
                    
                    if current_id == row2[0]:
                        row2[1] = 1
                        cursor2.updateRow(row2)

for key in input_datasets:
    
    # ----Create field mappings----
    out_fms = arcpy.FieldMappings()

    # 0.8ft field mapping
    fm_0p8ft = arcpy.FieldMap()
    out_0p8ft = arcpy.Field()  
    out_0p8ft.name = "slr_0p8ft"
    out_0p8ft.aliasName = "slr_0p8ft"
    out_0p8ft.type = "TEXT" 
    fm_0p8ft.outputField = out_0p8ft
    out_fms.addFieldMap(fm_0p8ft)

    # 3.1ft field mapping
    fm_3p1ft = arcpy.FieldMap()
    out_3p1ft = arcpy.Field()
    out_3p1ft.name = "slr_3p1ft"
    out_3p1ft.aliasName = "slr_3p1ft"
    out_3p1ft.type = "TEXT"
    fm_3p1ft.outputField = out_3p1ft
    out_fms.addFieldMap(fm_3p1ft)

    # 4.9ft field mapping
    fm_4p9ft = arcpy.FieldMap()
    out_4p9ft = arcpy.Field()
    out_4p9ft.name = "slr_4p9ft"
    out_4p9ft.aliasName = "slr_4p9ft"
    out_4p9ft.type = "TEXT"
    fm_4p9ft.outputField = out_4p9ft
    out_fms.addFieldMap(fm_4p9ft)

    # 6.6ft field mapping
    fm_6p6ft = arcpy.FieldMap()
    out_6p6ft = arcpy.Field()
    out_6p6ft.name = "slr_6p6ft"
    out_6p6ft.aliasName = "slr_6p6ft"
    out_6p6ft.type = "TEXT"
    fm_6p6ft.outputField = out_6p6ft
    out_fms.addFieldMap(fm_6p6ft)

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
    
    # ----- SLR INTERSECTIONS -----
    print("Intersecting with 0 p 8 ft")
    out_0p8ft = os.path.join(work_gdb,key+"_0p8ft")
    erase_0p8ft = os.path.join(work_gdb,key+"_0p8erase")
    intersect_0p8ft = os.path.join(work_gdb,key+"_0p8intrsct")
    if not arcpy.Exists(out_0p8ft):
        arcpy.analysis.PairwiseIntersect([city_intersect,slr_0p8ft], intersect_0p8ft, "NO_FID", "", "INPUT")
        arcpy.analysis.PairwiseErase(city_intersect, intersect_0p8ft, erase_0p8ft)
        arcpy.management.Merge([erase_0p8ft,intersect_0p8ft], out_0p8ft)
    
    # For 3.1ft scenario
    out_3p1ft = os.path.join(work_gdb,key+"_3p1ft")
    erase_3p1ft = os.path.join(work_gdb,key+"_3p1erase")
    intersect_3p1ft = os.path.join(work_gdb,key+"_3p1intrsct")
    if not arcpy.Exists(out_3p1ft):
        arcpy.analysis.PairwiseIntersect([out_0p8ft,slr_3p1ft], intersect_3p1ft, "NO_FID", "", "INPUT")
        arcpy.analysis.PairwiseErase(out_0p8ft, intersect_3p1ft, erase_3p1ft)
        arcpy.management.Merge([erase_3p1ft,intersect_3p1ft], out_3p1ft)

    # For 4.9ft scenario
    out_4p9ft = os.path.join(work_gdb,key+"_4p9ft")
    erase_4p9ft = os.path.join(work_gdb,key+"_4p9erase")
    intersect_4p9ft = os.path.join(work_gdb,key+"_4p9intrsct")
    if not arcpy.Exists(out_4p9ft):
        arcpy.analysis.PairwiseIntersect([out_3p1ft,slr_4p9ft], intersect_4p9ft, "NO_FID", "", "INPUT")
        arcpy.analysis.PairwiseErase(out_3p1ft, intersect_4p9ft, erase_4p9ft)
        arcpy.management.Merge([erase_4p9ft,intersect_4p9ft], out_4p9ft)
    
    print("Intersecting with 6 p 6 ft")
    out_6p6ft = os.path.join(work_gdb,key+"_6p6ft")
    erase_6p6ft = os.path.join(work_gdb,key+"_6p6erase")
    intersect_6p6ft = os.path.join(work_gdb,key+"_6p6intrsct")
    if not arcpy.Exists(out_6p6ft):
        arcpy.analysis.PairwiseIntersect([out_4p9ft,slr_6p6ft], intersect_6p6ft, "NO_FID", "", "INPUT")
        arcpy.analysis.PairwiseErase(out_4p9ft, intersect_6p6ft, erase_6p6ft)
        arcpy.management.Merge([erase_6p6ft,intersect_6p6ft], out_6p6ft)
    
    if msr_name:
        print("Adding measurement field...")
        print(msr_name)
        arcpy.management.AddField(out_6p6ft, msr_name, "DOUBLE")
        if "length" in msr_name:
            calc_sr = arcpy.SpatialReference(102005)
            arcpy.management.CalculateGeometryAttributes(out_6p6ft, [[msr_name,"LENGTH"]], "MILES_US","", calc_sr)
        elif "area" in msr_name:
            calc_sr = arcpy.SpatialReference(102003)
            arcpy.management.CalculateGeometryAttributes(out_6p6ft, [[msr_name,"AREA"]], "", "ACRES", calc_sr)
            
    # ----- SRP CHECKS -----
    if key in srp_datasets:
        print("Checking for SRPs...")
        arcpy.management.AddField(out_6p6ft, "srp", "SHORT")
        fm_srp = arcpy.FieldMap()
        out_srp = arcpy.Field()
        out_srp.name = "srp"
        out_srp.aliasName = "srp"
        out_srp.type = "SHORT"
        fm_srp.outputField = out_srp
        out_fms.addFieldMap(fm_srp)
        checkForSRPs(out_6p6ft,srp_datasets[key], srp_id_fields[key])
        fm_srp.addInputField(out_6p6ft,"srp")
        
    
    print("Clipping to RSAP analysis area...")
    # SLR field mappings
    fm_0p8ft.addInputField(out_6p6ft, "slr_0p8ft")
    fm_3p1ft.addInputField(out_6p6ft, "slr_3p1ft") 
    fm_4p9ft.addInputField(out_6p6ft, "slr_4p9ft")
    fm_6p6ft.addInputField(out_6p6ft, "slr_6p6ft")
    

    # Measurement field mapping if applicable
    print("Finishing field mappings...")
    if msr_name:
        fm_measurement.addInputField(out_6p6ft, msr_name)

    # Administrative boundary field mappings
    input_fields = [f.baseName for f in arcpy.ListFields(input_datasets[key])]
    if "city_1" in input_fields:
        fm_city.addInputField(out_6p6ft, "city_1")
    else:
        fm_city.addInputField(out_6p6ft,"city")
        
    fm_city2.addInputField(out_6p6ft, "citylsad")
    if "county_1" in input_fields:
        fm_county.addInputField(out_6p6ft, "county_1")
    else:
        fm_county.addInputField(out_6p6ft,"county")
    fm_county2.addInputField(out_6p6ft, "countylsad")
    fm_olu.addInputField(out_6p6ft, "olu")
    i=0
    for field in arcpy.ListFields(input_datasets[key]):
        if "OBJECTID" not in field.name and "Shape" not in field.name and "SHAPE" not in field.name and "FID" not in field.name and "GlobalID" not in field.name:
            temp_fm = arcpy.FieldMap()
            out_fm = arcpy.Field()
            out_fm.name = field.name
            out_fm.type = field.type
            out_fm.aliasName = field.aliasName
            temp_fm.outputField = out_fm
            temp_fm.addInputField(out_6p6ft, field.baseName)
            out_fms.addFieldMap(temp_fm)
            i+=1
            
    out_data = os.path.join(output_gdb,key)
    arcpy.conversion.ExportFeatures(out_6p6ft, out_data, "", "", out_fms)
                                
    # Delete intermediate products
    arcpy.management.Delete(county_intersect)
    arcpy.management.Delete(olu_intersect)
    arcpy.management.Delete(city_intersect)
    arcpy.management.Delete(out_0p8ft)
    arcpy.management.Delete(out_3p1ft)
    arcpy.management.Delete(out_4p9ft)

    # Delete erase/intersect intermediates for 0.8ft scenario
    arcpy.management.Delete(erase_0p8ft)
    arcpy.management.Delete(intersect_0p8ft)

    # Delete erase/intersect intermediates for 3.1ft scenario
    arcpy.management.Delete(erase_3p1ft)
    arcpy.management.Delete(intersect_3p1ft)

    # Delete erase/intersect intermediates for 4.9ft scenario
    arcpy.management.Delete(erase_4p9ft)
    arcpy.management.Delete(intersect_4p9ft)

    # Delete erase/intersect intermediates for 6.6ft scenario
    arcpy.management.Delete(erase_6p6ft)
    arcpy.management.Delete(intersect_6p6ft)



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


