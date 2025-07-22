import arcpy

# Set the path to your File Geodatabase
gdb_path = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Public_Access_Recreation\Public_Access_Recreation.gdb"

# Fields to check and correct
fields_to_check = ["city", "citylsad"]
incorrect_text = "Unincoporated"
correct_text = "Unincorporated"

# Get a list of all feature classes in the geodatabase
arcpy.env.workspace = gdb_path
feature_classes = arcpy.ListFeatureClasses()

# Iterate over each feature class
for fc in feature_classes:
    print(f"Processing feature class: {fc}")
    
    # Check which fields exist in the feature class
    existing_fields = [f.name for f in arcpy.ListFields(fc)]
    fields_to_update = [field for field in fields_to_check if field in existing_fields]

    if not fields_to_update:
        print(f"Skipping {fc} (No matching fields)")
        continue

    # Use UpdateCursor to modify the fields in place
    with arcpy.da.UpdateCursor(fc, fields_to_update) as cursor:
        for row in cursor:
            modified = False
            new_row = list(row)  # Convert tuple to list for modification
            
            for i, field in enumerate(fields_to_update):
                if new_row[i] and incorrect_text in new_row[i]:  # Check for None and occurrence of text
                    new_row[i] = new_row[i].replace(incorrect_text, correct_text)
                    modified = True

            if modified:
                cursor.updateRow(new_row)  # Save changes to the database

    print(f"Completed updates for {fc}")

print("All updates completed successfully!")



