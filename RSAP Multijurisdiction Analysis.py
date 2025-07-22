import arcpy
# Analysis to update city geo graphic boundary data with multijurisdictional opportunities with cities based on spatial relationship with OLUs 
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_Analysis_CALFire_2022"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_SFEI_2024"  # Intermediate feature class
third_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_CALFire_2022_ShorelineOnly"    # Third feature class for final selection
multijurisdiction_field = "multijurisdiction"  # New or existing field for the results
attribute_to_concat = "city"  # Field in third_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, multijurisdiction_field):
    print(f"Adding field '{multijurisdiction_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, multijurisdiction_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Total number of features in source_fc for progress tracking
source_feature_count = int(arcpy.GetCount_management(source_fc)[0])

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", multijurisdiction_field]) as update_cursor:
    current_feature = 0
    for source_row in update_cursor:
        current_feature += 1
        print(f"Processing feature {current_feature} of {source_feature_count}...")

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

        # Step 2: Use the selected features in target_fc to select features in third_fc
        arcpy.MakeFeatureLayer_management(third_fc, "third_layer")
        arcpy.SelectLayerByLocation_management(
            "third_layer",
            "INTERSECT",
            "target_layer"
        )
        print(f"  Selected features from {third_fc} using the target selection.")

        # Step 3: Concatenate attributes from the selected features in third_fc
        jurisdictions = []
        with arcpy.da.SearchCursor("third_layer", [attribute_to_concat]) as third_cursor:
            for selected_row in third_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 4: Update the source_fc feature with concatenated data
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)

        # Feedback to the user
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up selections
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("third_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")


import arcpy

# Analysis to update county geo graphic boundary data with multijurisdictional opportunities with cities based on spatial relationship with OLUs 
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Counties_US_Census_2019"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_SFEI_2024"  # Intermediate feature class
third_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_CALFire_2022_ShorelineOnly"    # Third feature class for final selection
multijurisdiction_field = "multijurisdiction"  # New or existing field for the results
attribute_to_concat = "city"  # Field in third_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, multijurisdiction_field):
    print(f"Adding field '{multijurisdiction_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, multijurisdiction_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Total number of features in source_fc for progress tracking
source_feature_count = int(arcpy.GetCount_management(source_fc)[0])

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", multijurisdiction_field]) as update_cursor:
    current_feature = 0
    for source_row in update_cursor:
        current_feature += 1
        print(f"Processing feature {current_feature} of {source_feature_count}...")

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

        # Step 2: Use the selected features in target_fc to select features in third_fc
        arcpy.MakeFeatureLayer_management(third_fc, "third_layer")
        arcpy.SelectLayerByLocation_management(
            "third_layer",
            "INTERSECT",
            "target_layer"
        )
        print(f"  Selected features from {third_fc} using the target selection.")

        # Step 3: Concatenate attributes from the selected features in third_fc
        jurisdictions = []
        with arcpy.da.SearchCursor("third_layer", [attribute_to_concat]) as third_cursor:
            for selected_row in third_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 4: Update the source_fc feature with concatenated data
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)

        # Feedback to the user
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up selections
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("third_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")


import arcpy
# Analysis to update OLU geo graphic boundary data with multijurisdictional opportunities with cities based on spatial relationship with OLUs 
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_SFEI_2024"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_SFEI_2024"  # Intermediate feature class
third_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_CALFire_2022_ShorelineOnly"    # Third feature class for final selection
multijurisdiction_field = "multijurisdiction"  # New or existing field for the results
attribute_to_concat = "city"  # Field in third_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, multijurisdiction_field):
    print(f"Adding field '{multijurisdiction_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, multijurisdiction_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Total number of features in source_fc for progress tracking
source_feature_count = int(arcpy.GetCount_management(source_fc)[0])

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", multijurisdiction_field]) as update_cursor:
    current_feature = 0
    for source_row in update_cursor:
        current_feature += 1
        print(f"Processing feature {current_feature} of {source_feature_count}...")

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

        # Step 2: Use the selected features in target_fc to select features in third_fc
        arcpy.MakeFeatureLayer_management(third_fc, "third_layer")
        arcpy.SelectLayerByLocation_management(
            "third_layer",
            "INTERSECT",
            "target_layer"
        )
        print(f"  Selected features from {third_fc} using the target selection.")

        # Step 3: Concatenate attributes from the selected features in third_fc
        jurisdictions = []
        with arcpy.da.SearchCursor("third_layer", [attribute_to_concat]) as third_cursor:
            for selected_row in third_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 4: Update the source_fc feature with concatenated data
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)

        # Feedback to the user
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up selections
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management("third_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")


import arcpy
#Intermediate analysis to estimate the number of cities with multipl OLUs
# Parameters: update these paths and field names for your data
source_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\0b_ProcessedInputs\Geographic_Boundaries_1.gdb\Cities_CDP_Analysis_CALFire_2022"  # Feature class to iterate over
target_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\0b_ProcessedInputs\Geographic_Boundaries_1.gdb\Operational_Landscape_Units_SFEI_2024"  # Intermediate feature class
third_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\0b_ProcessedInputs\Geographic_Boundaries_1.gdb\Operational_Landscape_Units_SFEI_2024"    # Third feature class for final selection
multijurisdiction_field = "multijurisdiction"  # New or existing field for the results
attribute_to_concat = "OLU_name"  # Field in third_fc to concatenate

# Add the output field if it doesn't exist
if not arcpy.ListFields(source_fc, multijurisdiction_field):
    print(f"Adding field '{multijurisdiction_field}' to {source_fc}.")
    arcpy.AddField_management(source_fc, multijurisdiction_field, "TEXT", field_length=2000)

print("Starting the processing...")

# Total number of features in source_fc for progress tracking
source_feature_count = int(arcpy.GetCount_management(source_fc)[0])

# Iterate through features in source_fc
with arcpy.da.UpdateCursor(source_fc, ["OID@", "SHAPE@", multijurisdiction_field]) as update_cursor:
    current_feature = 0
    for source_row in update_cursor:
        current_feature += 1
        print(f"Processing feature {current_feature} of {source_feature_count}...")

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

        # Step 3: Concatenate attributes from the selected features in third_fc
        jurisdictions = []
        with arcpy.da.SearchCursor("target_layer", [attribute_to_concat]) as third_cursor:
            for selected_row in third_cursor:
                jurisdictions.append(selected_row[0])

        concatenated_jurisdictions = ", ".join(jurisdictions)

        # Step 4: Update the source_fc feature with concatenated data
        source_row[2] = concatenated_jurisdictions
        update_cursor.updateRow(source_row)

        # Feedback to the user
        print(f"  Updated source feature OID {oid} with jurisdictions: {concatenated_jurisdictions}")

        # Clean up selections
        arcpy.SelectLayerByAttribute_management("target_layer", "CLEAR_SELECTION")

print("Processing complete. Check the multijurisdiction field for results.")



