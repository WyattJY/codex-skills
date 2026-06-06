# Visual Manifest Template

Use one row per inserted, changed, rebuilt, or rejected paper-derived visual. Keep absolute paths when practical.

| paper | source_pdf | source_page | source_id | visual_type | expected_objects | panel_map | crop_provenance | generated_provenance | clean_asset | report_page | source_inspected | render_inspected | claim_supported | content_role | reader_takeaway | source_fact_vs_inference | content_explained | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |  | `source_inspected=view_image path= page= observation=` | `render_inspected=view_image path= report_page= dpi= observation=` |  |  |  |  |  | `pass|recrop|rebuild-native|omit|partial-with-limitation` |

Required evidence examples:

- `source_inspected=view_image path=H:\...\paper_p12_240dpi.png page=12 observation=table body clean, final row visible`
- `render_inspected=view_image path=H:\...\inspect\page-031.png report_page=31 dpi=240 observation=labels readable, caption separated`
- `verdict=pass`

For generated/rebuilt visuals, fill `generated_provenance` with script path, input data/source table, parameters/seed, output format, and source comparison.
