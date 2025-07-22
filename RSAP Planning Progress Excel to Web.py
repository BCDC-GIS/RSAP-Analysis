import arcpy
import os

# --- Config ---
workspace = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Governance_Flood_Management\RSAP_Planning_Progress_BCDC" #download new excel file into this directory
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

# Paths
xls_path = os.path.join(workspace, "Subregional_Plan_Tracking_053025.xlsx")  # Manually downloaded file, update with new file name
csv_path = os.path.join(workspace, "planning_table.csv")
gdb_path = os.path.join(workspace, "Subregional_Plan_Tracking_BCDC.gdb")

planning_table = os.path.join(gdb_path, "planning_table")
city_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_CALFire_2022"
county_fc = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Boundaries\Geographic_Boundaries.gdb\Counties_US_Census_2019"

city_fc_field = "NAME"
county_fc_field = "NAME"
city_table_field = "Atlas_City"
county_table_field = "Atlas_Coun"

city_spatial = os.path.join(gdb_path, "city_spatial")
county_spatial = os.path.join(gdb_path, "county_spatial")

final_output_fc = os.path.join(gdb_path, f"RSAP_Planning_Status")

# --- STEP 0: Convert Excel sheet to CSV ---
sheet_name = "EXTERNAL-Plan Status"
arcpy.ExcelToTable_conversion(xls_path, csv_path, sheet_name)
print("📄 Converted Excel sheet to CSV.")

# --- STEP 1: Convert CSV to Table in GDB ---
arcpy.TableToTable_conversion(csv_path, gdb_path, "planning_table")
print("📑 CSV converted to GDB table.")

# --- STEP 1.5: Simplify spatial inputs to only NAME and geometry ---
def simplify_fc(input_fc, name_field, output_name, gdb_path):
    output_fc = os.path.join(gdb_path, output_name)

    # Clean up if it already exists
    if arcpy.Exists(output_fc):
        arcpy.Delete_management(output_fc)

    # Get geometry info
    desc = arcpy.Describe(input_fc)
    spatial_ref = desc.spatialReference
    geometry_type = desc.shapeType.upper()

    # Create the simplified feature class in GDB
    arcpy.CreateFeatureclass_management(
        out_path=gdb_path,
        out_name=output_name,
        geometry_type=geometry_type,
        spatial_reference=spatial_ref,
        has_m="DISABLED",
        has_z="DISABLED"
    )

    # Get the type of the name field
    fields = arcpy.ListFields(input_fc)
    name_field_type = None
    for f in fields:
        if f.name == name_field:
            name_field_type = f.type
            break
    if not name_field_type:
        raise ValueError(f"Field {name_field} not found in {input_fc}")

    # Add the name field
    if name_field_type.upper() in ["TEXT", "STRING"]:
        arcpy.AddField_management(output_fc, name_field, "TEXT", field_length=255)
    else:
        arcpy.AddField_management(output_fc, name_field, name_field_type)

    # Copy geometry + name field values
    with arcpy.da.SearchCursor(input_fc, ["SHAPE@", name_field]) as search_cursor, \
         arcpy.da.InsertCursor(output_fc, ["SHAPE@", name_field]) as insert_cursor:
        for row in search_cursor:
            insert_cursor.insertRow(row)

    return output_fc

# Simplify city and county FCs
city_fc_simple = simplify_fc(city_fc, city_fc_field, "city_simple", gdb_path)
county_fc_simple = simplify_fc(county_fc, county_fc_field, "county_simple", gdb_path)
print("✨ Simplified city and county feature classes written to GDB.")

# --- STEP 2: Add Geometry from City Boundaries to Planning Table ---
arcpy.MakeFeatureLayer_management(city_fc_simple, "city_fc_layer")
arcpy.AddJoin_management("city_fc_layer", city_fc_field, planning_table, city_table_field, "KEEP_COMMON")
arcpy.FeatureClassToFeatureClass_conversion("city_fc_layer", gdb_path, "city_spatial")
arcpy.RemoveJoin_management("city_fc_layer")
print("✅ Joined city geometry to planning table.")

# --- STEP 3: Add Geometry from County Boundaries to Planning Table ---
arcpy.MakeFeatureLayer_management(county_fc_simple, "county_fc_layer")
arcpy.AddJoin_management("county_fc_layer", county_fc_field, planning_table, county_table_field, "KEEP_COMMON")
arcpy.FeatureClassToFeatureClass_conversion("county_fc_layer", gdb_path, "county_spatial")
arcpy.RemoveJoin_management("county_fc_layer")
print("✅ Joined county geometry to planning table.")

# --- STEP 4: Delete records without geometry ---
for fc in [city_spatial, county_spatial]:
    arcpy.MakeFeatureLayer_management(fc, "temp_layer")
    arcpy.SelectLayerByAttribute_management("temp_layer", "NEW_SELECTION", "Shape IS NULL")
    count = int(arcpy.GetCount_management("temp_layer")[0])
    if count > 0:
        arcpy.DeleteFeatures_management("temp_layer")
        print(f"🧹 Deleted {count} features without geometry in {fc}.")
    arcpy.Delete_management("temp_layer")

# --- STEP 5: Append County into City ---
arcpy.Append_management(inputs=county_spatial, target=city_spatial, schema_type="NO_TEST")
print("✅ Appended county spatial features into city.")

# --- STEP 6: Copy to Final Output ---
arcpy.CopyFeatures_management(city_spatial, final_output_fc)
print(f"✅ Final output ready: {final_output_fc}")

# --- STEP 7: Keep only necessary fields and rename (alias) them ---
# List of fields to keep and their aliases
fields_to_keep = {
    "County": "County",
    "Jurisdicti": "Jurisdiction",
    "City_or_Co": "City or County",
    "Subregiona": "Subregional Plan Status",
    "Date_BCDC": "Date BCDC Notice Posted",
    "Link_to_BC": "Link to BCDC Notice",
    "Plan_Websi": "Plan Website (if applicable)",
    "Single_or": "Single or Muli-Jurisdiction Plan",
    "Participat": "Participating Jurisdictions"
    
    # Shape field must be included if keeping geometry
}

# System fields you can't delete
protected_fields = ["OBJECTID_1", "Shape", "Shape_Length", "Shape_Area"]

# Get all current fields
all_fields = [f.name for f in arcpy.ListFields(final_output_fc)]

# Compute fields to delete (exclude protected and keep list)
fields_to_delete = [f for f in all_fields if f not in fields_to_keep and f not in protected_fields]

# Delete unnecessary fields
if fields_to_delete:
    arcpy.DeleteField_management(final_output_fc, fields_to_delete)
    print(f"🧹 Deleted unnecessary fields: {fields_to_delete}")
else:
    print("✅ No unnecessary fields to delete.")

# Set field aliases for kept fields
for field, alias in fields_to_keep.items():
    try:
        arcpy.AlterField_management(final_output_fc, field, new_field_alias=alias)
        print(f"✏️ Set alias for {field} → {alias}")
    except Exception as e:
        print(f"⚠️ Could not set alias for {field}: {e}")
        


import arcpy
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# Sign into AGOL
gis = GIS("home")  # or GIS("https://www.arcgis.com", "username", "password")

# Path to the layer on disk (e.g., shapefile or FGDB feature class)
local_path = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Governance_Flood_Management\RSAP_Planning_Progress_BCDC\Subregional_Plan_Tracking_BCDC.gdb\RSAP_Planning_Status"

# ID of the hosted feature layer on AGOL
item_id = "1bbf708f78044b4ca6c310d36fcd64fe"

# Get the item
item = gis.content.get(item_id)

# Overwrite using the data
item_manager = FeatureLayerCollection.fromitem(item)
item_manager.manager.overwrite(local_path)


print(item.title, item.type)

item


