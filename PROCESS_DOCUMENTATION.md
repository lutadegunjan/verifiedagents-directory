# VerifiedAgents Directory ? Process Documentation

## 1. Project Overview

The objective of this project is to collect and structure publicly accessible insurance-agent profile information from VerifiedAgents, prepare a consolidated submission dataset, and develop an interactive Streamlit dashboard for searching, filtering, and reviewing agent records.

## 2. Data Collection and Extraction

- Collected 4,000 profile URLs.
- Removed duplicate profile URLs.
- Extracted NPN identifiers from numeric profile URL segments.
- Populated agent names and available profile information.
- Processed records in batches and consolidated the extracted information into a structured CSV.
- Used `Gunjan Lutade` as the `scraped_by` value.

Automated HTTP requests returned HTTP 403 responses and displayed a Cloudflare security-verification page. Browser-based access was used for permitted profile extraction. No attempt was made to bypass the security challenge.

## 3. Final Dataset

**File:** `verifiedagents_enriched_candidate_4000.csv`

**Location:** `data/verifiedagents_enriched_candidate_4000.csv`

The consolidated dataset contains 4,000 records and the following 10 columns:

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

### Field Population

| Field | Populated Records |
|---|---:|
| Serial number | 4,000 |
| Profile URL | 4,000 |
| Full name | 4,000 |
| NPN number | 4,000 |
| Location | 3,974 |
| Phone numbers | 3,107 |
| Email addresses | 3,112 |
| Websites | 0 |
| Appointed companies | 2,791 |
| Scraped by | 4,000 |

### Data Validation

- Total records: 4,000
- Unique profile URLs: 4,000
- Missing profile URLs: 0
- Duplicate profile URLs: 0
- Missing information was retained as blank rather than filled with guessed values.
- Multiple values within a field are retained in the consolidated dataset.

Names were initially derived from profile URL slugs, and NPN identifiers were taken from numeric URL segments. These fields should be treated as URL-derived unless independently verified against corresponding profile information.

## 4. Data Limitations

The dataset contains 4,000 collected profiles. This count does not establish that every profile in the entire publicly accessible directory has been collected.

No website URLs were populated in the final dataset. Website values were left blank rather than inferred or fabricated.

Some profiles do not provide location, phone, email, or appointed-company information. These fields remain blank where information was unavailable.

## 5. Excel Submission Workbook

**File:** `Submission File (Gunjan).xlsx`

The workbook contains a `Verifiedagents Directory` sheet with 4,000 data records and the required 10-column structure. Existing workbook tabs were preserved.

## 6. Interactive Dashboard

**Application:** VerifiedAgents Directory

**Dashboard code:** `dashboard/dashboard.py`

**Data source:** `data/verifiedagents_enriched_candidate_4000.csv`

The dashboard is developed using Streamlit and Pandas.

### Dashboard Features

- Global search across agent records.
- Individual filters for available dataset fields.
- Dynamic profile and filtered-record counts.
- Geographic coverage metrics.
- Phone, email, website, and appointed-company coverage metrics.
- Interactive filtered-record table.
- CSV download of filtered results.

### Dashboard Metrics

The dashboard displays:

- Total profiles: 4,000
- Filtered profiles
- Profiles with NPN
- Location coverage
- Phone-number coverage
- Email-address coverage
- Website coverage
- Appointed-company coverage
- Unique states
- Unique cities (city-state pairs)
- Unique ZIP codes

Geographic coverage metrics use ZIP-code lookup data, with source-verified exceptions applied where necessary. ZIP-derived city names represent lookup-based geographic coverage and may not correspond to every municipality served by a ZIP code.

## 7. Deployment

The dashboard is deployed using Streamlit Community Cloud.

**Public Dashboard:**

https://verifiedagents-directory-enbcknsw3nwrkpovbzxgxr.streamlit.app/

The deployed application was checked to confirm that the 4,000-profile dataset and geographic coverage metrics are displayed.

## 8. Remaining Considerations

- Confirm whether the 4,000 collected profiles represent the complete publicly accessible directory.
- Verify URL-derived names and NPN identifiers against corresponding profile information where possible.
- Populate website information only when available from a permitted and verifiable source.
- The current dashboard reads the consolidated CSV file. Confirm that this source remains aligned with the final Excel submission workbook if the submission requirement specifies that the workbook must be the dashboard's sole data source.
