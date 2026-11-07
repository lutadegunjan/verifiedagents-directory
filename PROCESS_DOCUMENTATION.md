# VerifiedAgents Directory ? Process Documentation

## 1. Project Overview

### 1.1 Project Objective
The objective of this task was to collect insurance agent information from the VerifiedAgent directory, organize the extracted information into a structured dataset, prepare the Excel submission, and develop a publicly accessible Streamlit dashboard.

### 1.2 Source Website
- Website: https://verifiedagent.com
- Project: VerifiedAgents Directory
- Records processed: 4,000 agent profiles

### 1.3 Tools and Technologies
- Python
- Pandas
- Playwright
- Chrome browser and Chrome DevTools Protocol (CDP)
- Excel / OpenPyXL
- Streamlit
- Git and GitHub
- pgeocode for ZIP-code-based geographic enrichment

## 2. Part 1 ? Data Extraction and Submission

### 2.1 Data Fields
The final dataset contains the following 10 columns:

1. `s_no`
2. `profile_page_url`
3. `full_name`
4. `npn_number`
5. `location`
6. `phone_numbers`
7. `email_addresses`
8. `websites`
9. `appointed_companies`
10. `scraped_by`

### 2.2 Extraction Workflow
1. Inspected the source website and its agent profile pages.
2. Identified the profile information and relevant fields required for the task.
3. Collected and processed agent profile records in batches.
4. Used browser-based access for pages that were not reliably accessible through direct HTTP requests.
5. Extracted the available profile information and organized it into a structured CSV dataset.
6. Used intermediate progress files and checkpoints to retain extraction progress.
7. Combined and validated the collected records into the final 4,000-record dataset.
8. Assigned `Gunjan Lutade` in the `scraped_by` field.

### 2.3 Data Cleaning and Formatting
- Standardized the dataset into the required 10-column structure.
- Kept multiple values in a field separated by line breaks or delimiters where applicable.
- Retained unavailable information as blank rather than inserting unverified values.
- Checked profile URLs for missing values and duplicates.
- Ensured the final dataset contained 4,000 unique profile URLs.

### 2.4 Final Dataset
File: `data/verifiedagents_enriched_candidate_4000.csv`

Final dataset details:
- Total records: 4,000
- Total columns: 10
- Unique profile URLs: 4,000
- Missing profile URLs: 0
- Duplicate profile URLs: 0
- `scraped_by` attribution: Gunjan Lutade

### 2.5 Field Availability

| Field | Populated Records |
|---|---:|
| S No | 4,000 |
| Profile Page URL | 4,000 |
| Full Name | 4,000 |
| NPN Number | 4,000 |
| Location | 3,974 |
| Phone Numbers | 3,107 |
| Email Addresses | 3,112 |
| Websites | 0 |
| Appointed Companies | 2,791 |
| Scraped By | 4,000 |

## 3. Blocker Encountered and Resolution

### 3.1 Blocker: HTTP 403 and Cloudflare Protection
During the extraction process, direct HTTP requests to the source website returned HTTP 403 responses. Some pages displayed Cloudflare's "Just a moment" challenge, which prevented ordinary automated requests from reliably accessing profile content.

### 3.2 Impact
- Direct requests could not consistently retrieve profile information.
- Some requests returned challenge pages instead of the expected profile HTML.
- The extraction workflow needed to account for browser-based access and interrupted batches.

### 3.3 Investigation and Troubleshooting
1. Tested direct HTTP access to the website and identified the 403 responses.
2. Inspected the browser-rendered pages to understand the website's access behavior.
3. Checked whether the required profile information was available in the rendered page.
4. Tested browser-based access using Chrome and Playwright/CDP.
5. Identified challenge pages and treated them as access failures rather than valid profile data.
6. Avoided treating incomplete or challenge-page responses as successfully extracted records.

### 3.4 Resolution and Recovery Approach
- Used an interactive browser session to access pages where browser access was available.
- Used Playwright with the Chrome DevTools Protocol connection for browser-based extraction.
- Processed records in manageable batches rather than relying on one continuous extraction run.
- Retained intermediate progress files and checkpoints to reduce the risk of losing completed work.
- Resumed processing from saved progress where possible.
- Kept unavailable fields blank instead of generating or assuming values.

The website's access challenge was handled through browser-based inspection and recovery of accessible records. This documentation does not claim that Cloudflare protection was bypassed or disabled.

### 3.5 Website Field Investigation
The `websites` field remained empty in the final dataset.
- A sample of 50 profiles was checked for website information.
- A separate website-only re-extraction was performed on a subset of approximately 1,700 profiles.
- No website URLs were recovered in those checks.
- Website values were therefore retained as blank.

The checks were not a confirmed individual audit of every one of the 4,000 profiles.

## 4. Part 2 ? Excel Submission

### 4.1 Submission Workbook
Final workbook: `Submission File (Gunjan).xlsx`

Target worksheet: `Verifiedagents Directory`

### 4.2 Workbook Structure
- The worksheet title is in the first row.
- The column headers are in the second row.
- The 4,000 agent records begin in the third row.
- The worksheet contains 10 data columns.

### 4.3 Data Synchronization
The original worksheet contained the same 4,000 profile URLs as the enriched CSV, in the same order, but had fewer populated values in several fields.

To correct this:
1. Compared the profile URLs in the CSV and Excel worksheet.
2. Confirmed that all 4,000 URLs matched in the same order.
3. Created a timestamped backup of the workbook.
4. Updated the 4,000 data rows in the `Verifiedagents Directory` worksheet using the enriched CSV.
5. Preserved the workbook's other worksheets.
6. Re-read the updated workbook and compared its data against the CSV.

### 4.4 Synchronization Verification
The final comparison confirmed that all 10 columns in the Excel worksheet matched the CSV dataset.

The following populated-value counts were also verified:

- Locations: 3,974
- Phone numbers: 3,107
- Email addresses: 3,112
- Websites: 0
- Appointed companies: 2,791

## 5. Part 3 ? Streamlit Dashboard Development

### 5.1 Dashboard Objective
Developed an interactive directory dashboard to allow users to search, filter, and inspect the collected insurance agent records.

### 5.2 Technologies
- Streamlit
- Pandas
- OpenPyXL
- pgeocode

### 5.3 Dashboard Features
1. Global search across the available fields.
2. Individual column filters for all 10 fields.
3. Total and filtered profile counts.
4. NPN availability count.
5. Data availability metrics for location, phone, email, website, and appointed company fields.
6. Geographic coverage metrics.
7. Agent record display.

### 5.4 Dashboard Data Source
The dashboard reads directly from:

`Submission File (Gunjan).xlsx`

Worksheet:

`Verifiedagents Directory`

The Excel worksheet uses the second row as its header row. The dashboard reads the workbook directly rather than relying on a separate CSV as its deployed data source.

### 5.5 Dashboard Metrics Verified
| Metric | Verified Value |
|---|---:|
| Total Profiles | 4,000 |
| Filtered Profiles (initial view) | 4,000 |
| Profiles with NPN | 4,000 |
| Locations | 3,974 |
| Phone Numbers | 3,107 |
| Email Addresses | 3,112 |
| Websites | 0 |
| Appointed Companies | 2,791 |
| Unique States | 48 |
| Unique Cities (City-State) | 1,645 |
| Unique ZIP Codes | 2,563 |

Geographic coverage figures use ZIP-code-based geographic enrichment. City and state figures should be interpreted in the context of ZIP-code mapping.

## 6. Part 4 ? Testing and Validation

### 6.1 Dataset Validation
- Confirmed 4,000 records in the final dataset.
- Confirmed 4,000 unique profile URLs.
- Confirmed no missing profile URLs.
- Confirmed no duplicate profile URLs.
- Checked the 10 required columns.
- Compared the CSV and Excel worksheet values.
- Confirmed that all 10 columns matched after synchronization.

### 6.2 Dashboard Testing
- Confirmed that the dashboard loaded the Excel workbook.
- Verified the initial total profile count.
- Checked data availability metrics against the final dataset.
- Verified geographic coverage figures.
- Confirmed that the global search and individual column filters were displayed.
- Confirmed that the dashboard displayed all 4,000 records in the initial view.

### 6.3 Deployment Verification
The deployed dashboard was opened after the GitHub update. The displayed metrics were checked against the locally verified workbook.

## 7. Part 5 ? GitHub and Deployment

### 7.1 GitHub Repository
Repository:
https://github.com/lutadegunjan/verifiedagents-directory

### 7.2 Main Project Files
- `Submission File (Gunjan).xlsx`
- `dashboard/dashboard.py`
- `requirements.txt`
- `PROCESS_DOCUMENTATION.md`
- `data/verifiedagents_enriched_candidate_4000.csv`

### 7.3 Deployment
Platform: Streamlit Community Cloud

Public dashboard:
https://verifiedagents-directory-enbcknsw3nwrkpovbzxgxr.streamlit.app/

The final workbook and dashboard changes were committed and pushed to the `main` branch. The deployed dashboard was subsequently checked.

## 8. Limitations and Observations

1. The final dataset contains 4,000 unique profiles. The total size of the website's complete directory was not independently established; therefore, the 4,000 records should not be described as a confirmed complete extraction of the entire website.
2. The website field has no populated values in the final dataset. Sample and subset checks did not recover website URLs.
3. Some profile fields were not populated or available in the accessible source data. These values were retained as blank.
4. Names and NPN values should be interpreted according to the extraction method and source-page information; they were not independently verified against a separate authoritative registry.
5. Geographic coverage metrics are based on ZIP-code mapping and should not be interpreted as a complete list of every municipality served.

## 9. Final Deliverables

1. Final Excel submission workbook: `Submission File (Gunjan).xlsx`
2. Structured dataset: `data/verifiedagents_enriched_candidate_4000.csv`
3. Streamlit dashboard source: `dashboard/dashboard.py`
4. Dependency file: `requirements.txt`
5. Process documentation: `PROCESS_DOCUMENTATION.md`
6. GitHub repository: https://github.com/lutadegunjan/verifiedagents-directory
7. Public dashboard: https://verifiedagents-directory-enbcknsw3nwrkpovbzxgxr.streamlit.app/

## 10. Final Project Status

- 4,000 agent records processed.
- 10 required dataset columns maintained.
- Excel worksheet synchronized with the enriched CSV.
- All 10 columns verified as identical between the CSV and Excel worksheet.
- Dashboard configured to read directly from the final Excel workbook.
- Search and individual filters available.
- Dashboard metrics checked against the final dataset.
- Updated workbook and dashboard changes pushed to GitHub.
- Public Streamlit dashboard checked after deployment.

