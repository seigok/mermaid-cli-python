# Regression Test Scenarios

This document maps current functionality to automated regression tests.

## How To Run

```bash
python -m pytest
```

## Scenario Matrix

| Feature | Scenario | Test(s) |
| --- | --- | --- |
| CLI rendering | Render a single `.mmd` to SVG/PNG/PDF via CLI | `TestMermaidCLICLI.test_cli_render_svg`, `TestMermaidCLICLI.test_cli_render_png`, `TestMermaidCLICLI.test_cli_render_pdf` |
| CLI markdown processing | Convert Markdown with multiple Mermaid blocks to images and update `.md` | `TestMermaidCLICLI.test_cli_render_markdown` |
| CLI themes | Apply theme via `-t/--theme` | `TestMermaidCLICLI.test_cli_with_theme` |
| CLI background color | Apply background via `-b/--background-color` | `TestMermaidCLICLI.test_cli_with_background_color` |
| CLI dimensions | Custom width/height via `-w/-H` | `TestMermaidCLICLI.test_cli_with_custom_dimensions` |
| CLI scale factor | Device scale via `-s/--scale` | `TestMermaidCLICLIOptions.test_cli_with_scale_option` |
| CLI PDF fit | PDF fit via `-f/--pdf-fit` | `TestMermaidCLICLIOptions.test_cli_with_pdf_fit_option` |
| CLI SVG ID | SVG element id via `-I/--svg-id` | `TestMermaidCLICLIOptions.test_cli_with_svg_id_option` |
| CLI CSS file | Apply CSS via `-C/--css-file` | `TestMermaidCLICLIOptions.test_cli_with_css_and_config_files` |
| CLI Mermaid config | Apply config via `-c/--config-file` | `TestMermaidCLICLIOptions.test_cli_with_css_and_config_files` |
| CLI icon packs | Pass icon packs via `--icon-packs` | `TestMermaidCLICLIOptions.test_cli_with_icon_packs` |
| CLI Playwright config | Pass browser options via `-p/--playwright-config-file` | `TestMermaidCLICLIOptions.test_cli_with_playwright_config_file` |
| CLI version | `--version` output | `TestMermaidCLICLI.test_cli_version` |
| API render formats | Render SVG/PNG/PDF outputs | `TestMermaidCLIAPI.test_api_render_mermaid_all_formats` |
| API diagram types | Render flowchart/sequence/gantt/pie/state/ER/class/user-journey | `TestMermaidCLIAPI.test_api_render_mermaid_flowchart`, `TestMermaidCLIAPI.test_api_render_mermaid_sequence_diagram`, `TestMermaidCLIAPI.test_api_render_mermaid_gantt_chart`, `TestMermaidCLIAPI.test_api_render_mermaid_pie_chart`, `TestMermaidCLIAPI.test_api_render_mermaid_state_diagram`, `TestMermaidCLIAPI.test_api_render_mermaid_er_diagram`, `TestMermaidCLIAPI.test_api_render_mermaid_class_diagram`, `TestMermaidCLIAPI.test_api_render_mermaid_user_journey` |
| API render file | Render single file in all formats | `TestMermaidCLIAPI.test_api_render_mermaid_file_all_formats` |
| API markdown file | Render Markdown with multiple Mermaid blocks | `TestMermaidCLIAPI.test_api_render_mermaid_file_markdown` |
| API sync wrapper | `render_mermaid_file_sync` | `TestMermaidCLIAPI.test_api_render_mermaid_file_sync_all_formats` |
| API custom config | Mermaid config overrides | `TestMermaidCLI.test_render_mermaid_with_custom_config` |
| API custom CSS | Apply CSS string | `TestMermaidCLI.test_render_mermaid_with_custom_css` |
| API background color | Apply background color | `TestMermaidCLI.test_render_mermaid_with_custom_background` |
| API SVG ID | Custom SVG id | `TestMermaidCLI.test_render_mermaid_with_svg_id` |
| API icon packs | Pass icon packs into page context | `TestMermaidCLI.test_render_mermaid_with_icon_packs` |
| API PDF fit | Fit PDF to diagram bounds | `TestMermaidCLI.test_render_mermaid_pdf_fit_uses_dimensions` |
| API Playwright config | Pass `headless`, `executable_path`, `args` | `TestMermaidCLI.test_playwright_config_parameter` |
| Input helpers | Read from stdin and create markdown image | `TestMermaidCLI.test_get_input_data_from_stdin`, `TestMermaidCLI.test_create_markdown_image` |
| Real-world fixtures | Render all sample `.mmd` and config/CSS files | `TestMermaidCLIWithTestPositive.test_render_all_mmd_files`, `TestMermaidCLIWithTestPositive.test_render_with_config_files`, `TestMermaidCLIWithTestPositive.test_render_with_css` |
