import arcpy
import os

arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.overwriteOutput = True
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26910)

import datetime

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

# ==== USER INPUTS - Update paths and field names as needed ====

parcels = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\Housing_Jobs_redux\Housing_Development_Land_Use.gdb\Housing_Jobs_Simple"

# Boundary layers
cities = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Boundaries\Geographic_Boundaries.gdb\Cities_CDP_Analysis_CALFire_2022"
city_id_field = "citylsad"

counties = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Boundaries\Geographic_Boundaries.gdb\Counties_Analysis_US_Census_2019"
county_id_field = "countylsad"

olus = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Datasets\1_InputData\Boundaries\Geographic_Boundaries.gdb\Operational_Landscape_Units_Analysis_SPUR_SFEI_2019"
olu_id_field = "olu"

taz = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\Housing_Jobs_redux\Geographic_Boundaries.gdb\transportation_analysis_zones_1454_MTC_2023"
taz_id_field = "taz1454"  # 🔁 Update this to match the actual field name in the TAZ layer

# Output GDB location and name
output_gdb_folder = r"E:\Shared drives\BCDC Regional Shoreline Adaptation Planning\Workspace\Housing_Jobs_redux"
output_gdb_name = "Housing_Jobs.gdb"

# Parcel field names
jobs_field = "Job_Spaces_2010"
res_units_field = "Residential_Units_2010"
future_jobs_field = "Job_Spaces_2050"
future_units_field = "Residential_Units_2050"

# SLR binary exposure fields (1 = exposed, blank = not exposed)
slr_fields = ["slr_0p8ft", "slr_3p1ft", "slr_4p9ft", "slr_6p6ft"]

# ==== Workspace setup ====
output_gdb = os.path.join(output_gdb_folder, output_gdb_name)
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(output_gdb_folder, output_gdb_name)

arcpy.env.workspace = output_gdb
arcpy.env.overwriteOutput = True

# === Utility function to generate everything for a given zone type ===
def process_zone(zone_name, zone_fc, zone_id_field, suffix):
    log(f"🔹 Starting processing for {zone_name}...")
    print(f"\n🔹 Processing {zone_name}...")

    # 1. Spatial Join
    joined_parcels = f"Parcels_With_{suffix}"
    log(f"1. Spatial Join: Joining parcels with {zone_name} boundaries...")
    arcpy.analysis.SpatialJoin(
        target_features=parcels,
        join_features=zone_fc,
        out_feature_class=joined_parcels,
        join_operation="JOIN_ONE_TO_ONE",
        join_type="KEEP_COMMON",
        match_option="HAVE_THEIR_CENTER_IN"
    )
        # Detect actual zone field in joined parcels
    joined_fields = [f.name for f in arcpy.ListFields(joined_parcels)]
    log(f"Fields in joined_parcels: {joined_fields}")

    actual_zone_field = None
    for f in joined_fields:
        if zone_id_field.lower() in f.lower():
            actual_zone_field = f
            log(f"✅ Using zone field '{actual_zone_field}' for statistics.")
            break

    if not actual_zone_field:
        raise ValueError(f"❌ Could not find a matching zone ID field like '{zone_id_field}' in joined_parcels.")


    # 2. Add exposure calculation fields
    log("2. Adding and calculating exposure fields...")
    exposure_fields = []
    all_calc_exprs = []

    for i, slr in enumerate(slr_fields, start=1):
        jf = f"jobs_slr{i}"
        uf = f"units_slr{i}"
        fjf = f"future_jobs_slr{i}"
        fuf = f"future_units_slr{i}"

        exposure_fields += [jf, uf, fjf, fuf]

        # Add fields
        for fld in [jf, uf, fjf, fuf]:
            arcpy.management.AddField(joined_parcels, fld, "DOUBLE")

        # Prepare CalculateFields expressions
        all_calc_exprs += [
            [jf, f"(!{jobs_field}! if !{slr}! == '1' else 0)"],
            [uf, f"(!{res_units_field}! if !{slr}! == '1' else 0)"],
            [fjf, f"(!{future_jobs_field}! if !{slr}! == '1' else 0)"],
            [fuf, f"(!{future_units_field}! if !{slr}! == '1' else 0)"]
        ]

    arcpy.management.CalculateFields(joined_parcels, "PYTHON3", all_calc_exprs)
    log("✔ Exposure fields calculated.")

    # 3. Summary Table
    summary_table = f"{zone_name}_Exposure_Summary"
    summary_fields = [
        [jobs_field, "SUM"], [res_units_field, "SUM"],
        [future_jobs_field, "SUM"], [future_units_field, "SUM"]
    ] + [[f, "SUM"] for f in exposure_fields]

    
    log("3. Summarizing exposure data by zone...")
    fields = [f.name for f in arcpy.ListFields(joined_parcels)]
    log(f"Fields in joined_parcels: {fields}")
    arcpy.analysis.Statistics(joined_parcels, summary_table, summary_fields, actual_zone_field)
    log(f"✔ Summary table created: {summary_table}")

    # 4. Rename fields for clarity
    log("4. Renaming summary fields...")
    rename_map = {
        f"SUM_{jobs_field}": "total_jobs",
        f"SUM_{res_units_field}": "total_units",
        f"SUM_{future_jobs_field}": "total_future_jobs",
        f"SUM_{future_units_field}": "total_future_units"
    }
    for i in range(1, len(slr_fields) + 1):
        rename_map[f"SUM_jobs_slr{i}"] = f"jobs_slr{i}"
        rename_map[f"SUM_units_slr{i}"] = f"units_slr{i}"
        rename_map[f"SUM_future_jobs_slr{i}"] = f"future_jobs_slr{i}"
        rename_map[f"SUM_future_units_slr{i}"] = f"future_units_slr{i}"

    # Get list of fields in summary table
    summary_fields_existing = [f.name for f in arcpy.ListFields(summary_table)]

    # Safely rename only fields that exist
    for old, new in rename_map.items():
        if old in summary_fields_existing:
            try:
                arcpy.management.AlterField(summary_table, old, new)
                log(f"Renamed field {old} ➜ {new}")
            except Exception as e:
                log(f"⚠ Failed to rename field {old} ➜ {new}: {e}")
        else:
            log(f"⚠ Field {old} not found in summary table — skipping rename.")

    log("✔ Field renaming complete.")

    # 5. Create spatial layer with joined summary
    spatial_fc = f"{zone_name}s_Exposure_Summary"
    log("5. Joining summary back to zone layer for spatial output...")
    arcpy.management.CopyFeatures(zone_fc, spatial_fc)
    # Check if the expected join field exists in both tables
    summary_fields = [f.name for f in arcpy.ListFields(summary_table)]
    spatial_fields = [f.name for f in arcpy.ListFields(spatial_fc)]

    actual_join_field = None
    for field in summary_fields:
        if field.upper() == zone_id_field.upper() and field in spatial_fields:
            actual_join_field = field
            break

    if not actual_join_field:
        # Try a fallback: look for any field with a similar name
        matches = [f for f in spatial_fields if zone_id_field.lower() in f.lower()]
        if matches:
            actual_join_field = matches[0]
            log(f"⚠ Using best-match join field: {actual_join_field}")
        else:
            raise ValueError(f"❌ Zone ID field '{zone_id_field}' not found in spatial layer or summary table.")

    # Join the summary table to the spatial features
    arcpy.management.JoinField(spatial_fc, actual_zone_field, summary_table, actual_zone_field)
    log(f"✅ {zone_name} summary complete: {spatial_fc}")

# === Process all 3 zone types ===
#process_zone("City", cities, city_id_field, "City")
#process_zone("County", counties, county_id_field, "County")
#process_zone("OLU", olus, olu_id_field, "OLU")
process_zone("TAZ", taz, taz_id_field, "TAZ")

# === Done ===
print("\n🎉 All zone summaries complete!")
print(f"📁 Output saved in: {output_gdb}")

fields = [f.name for f in arcpy.ListFields(olus)]
print(fields)


