
import arcpy
arcpy.env.overwriteOutput = True
#analysis to add city names to CBO directory data for cbos whose stewardship area overlaps jurisdictional boundaries. 
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\CBO_Directory_Map_BCDC_2024.gdb\Community_Based_Organization_Directory_Map_011525"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_CALFire_2022_ShorelineOnly"  # Feature class for the selection
city_field = "city"  # New or existing field for the results
attribute_to_concat = "city"  # Field in target_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, city_field):
    print(f"Adding field '{city_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, city_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", city_field]) as update_cursor:
    for source_row in update_cursor:
        oid = source_row[0]
        source_geometry = source_row[1]

        # Step 1: Select features in target_fc that intersect the source feature
        arcpy.MakeFeatureLayer_management(target_fc, "target_layer")
        arcpy.SelectLayerByLocation_management(
            "target_layer",
            "INTERSECT",
            source_geometry
        )
        print(f"  Selected features from {target_fc} that intersect source feature OID {oid}.")

        # Step 2: Fetch and concatenate attributes
        jurisdictions = []
        with arcpy.da.SearchCursor("target_layer", [attribute_to_concat]) as target_cursor:
            for selected_row in target_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 3: Update the source feature with the concatenated string
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up the selection
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")


import arcpy
arcpy.env.overwriteOutput = True
#analysis to add county names to CBO directory data for cbos whose stewardship area overlaps jurisdictional boundaries.
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\CBO_Directory_Map_BCDC_2024.gdb\Community_Based_Organization_Directory_Map_011525"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Counties_US_Census_2019"  # Feature class for the selection
county_field = "county"  # New or existing field for the results
attribute_to_concat = "NAME"  # Field in target_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, county_field):
    print(f"Adding field '{county_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, county_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", county_field]) as update_cursor:
    for source_row in update_cursor:
        oid = source_row[0]
        source_geometry = source_row[1]

        # Step 1: Select features in target_fc that intersect the source feature
        arcpy.MakeFeatureLayer_management(target_fc, "target_layer")
        arcpy.SelectLayerByLocation_management(
            "target_layer",
            "INTERSECT",
            source_geometry
        )
        print(f"  Selected features from {target_fc} that intersect source feature OID {oid}.")

        # Step 2: Fetch and concatenate attributes
        jurisdictions = []
        with arcpy.da.SearchCursor("target_layer", [attribute_to_concat]) as target_cursor:
            for selected_row in target_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 3: Update the source feature with the concatenated string
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up the selection
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")


import arcpy
arcpy.env.overwriteOutput = True
#analysis to add OLU names to CBO directory data for cbos whose stewardship area overlaps jurisdictional boundaries.
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\CBO_Directory_Map_BCDC_2024.gdb\Community_Based_Organization_Directory_Map_011525"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_SFEI_2024"  # Feature class for the selection
olu_field = "olu"  # New or existing field for the results
attribute_to_concat = "OLU_Name"  # Field in target_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, olu_field):
    print(f"Adding field '{olu_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, olu_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", olu_field]) as update_cursor:
    for source_row in update_cursor:
        oid = source_row[0]
        source_geometry = source_row[1]

        # Step 1: Select features in target_fc that intersect the source feature
        arcpy.MakeFeatureLayer_management(target_fc, "target_layer")
        arcpy.SelectLayerByLocation_management(
            "target_layer",
            "INTERSECT",
            source_geometry
        )
        print(f"  Selected features from {target_fc} that intersect source feature OID {oid}.")

        # Step 2: Fetch and concatenate attributes
        jurisdictions = []
        with arcpy.da.SearchCursor("target_layer", [attribute_to_concat]) as target_cursor:
            for selected_row in target_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 3: Update the source feature with the concatenated string
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up the selection
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")
