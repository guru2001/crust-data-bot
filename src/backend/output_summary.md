Summary of Document 1:
# Crustdata Discovery and Enrichment API Overview

## Introduction
Crustdata API offers programmatic access to firmographic and growth metrics data for global companies, drawing from over 16 datasets (LinkedIn, Glassdoor, Instagram, etc.). 

## Getting Started
- **Authorization**: Obtain an API key by contacting [abhilash@crustdata.com](mailto:abhilash@crustdata.com).

## API Endpoints

### Company Endpoints

#### Enrichment: Company Data API
- **Function**: Retrieve detailed information about companies via domain, name, or ID.
- **Authorization**: Requires `auth_token`.
- **Parameters**:
  - `company_domain`: List of up to 25 domains.
  - `company_name`: List of up to 25 company names (use quotes for names containing commas).
  - `company_linkedin_url`: List of LinkedIn URLs for the companies.
  - `company_id`: List of unique IDs for the companies.
  - `fields`: Specify fields for the response.
  - `enrich_realtime`: If set to True, allows for real-time enrichment of untracked companies.

#### Company Discovery: Screening API
- **Function**: Filter companies based on growth and firmographic criteria.
- **Parameters**:
  - `metrics`: Required to define which metrics are included in the results.
  - `filters`: Conditions that filter the results based on various criteria.
  - `offset`: Sets the starting point for the results.
  - `count`: Specifies number of results to return (max 100).

### Company Identification API
- **Function**: Identify a company using its name, website, or LinkedIn profile.

### Company Dataset API
- **Function**: Retrieve specific datasets related to companies like job listings and decision-makers.

### Search: LinkedIn Company Search API (real-time)
- **Function**: Search for company profiles using a LinkedIn Sales Navigator URL or custom criteria.
  
### LinkedIn Posts by Company API (real-time)
- **Function**: Retrieve recent LinkedIn posts for a specified company.

### People Endpoints

#### Enrichment: People Profile(s) API
- **Function**: Enrich individual profiles using LinkedIn URLs or business emails.
- **Parameters**:
  - `linkedin_profile_url`: Comma-separated list of LinkedIn URLs.
  - `business_email`: A single business email.
  - `enrich_realtime`: Allows for real-time search.
  - `fields`: Specify which fields to include in the response.

#### Search: LinkedIn People Search API (real-time)
- **Function**: Search for individuals based on a direct LinkedIn Sales Navigator search URL or custom search criteria.
  
### LinkedIn Posts by Person API (real-time)
- **Function**: Retrieve recent LinkedIn posts by a specified individual.

### API Usage Endpoints

#### Get Remaining Credits
- **Function**: Check the remaining credits for the API usage.

## Key Points
- **Credits**: Different endpoints consume varying credits.
  - Basic enrichment: 3 credits.
  - Real-time enrichment: 5 credits.
  - Screen company: 1 credit per company.
- **Real-time Enrichment**: Allows for enhancing data on the fly for companies not already present in the database.
- **Response Structures**: Use JSON format to receive data, with varying response formats depending on endpoint functionality.

For detailed examples and additional documentation, refer to the provided links in the original document.

Summary of Document 2:
# Crustdata Dataset API Detailed Summary

## Overview
Crustdata provides comprehensive APIs for accessing company-specific datasets, including job listings, funding milestones, employee information, and metrics from platforms like Glassdoor and G2. The API requires an authentication token for access.

## API Endpoints

### 1. Job Listings
- **Unique Identifier:** `company_id` (numeric).
- **Request Variants:**
  - Direct job listing queries by specified `company_id`.
  - Real-time fetching (`sync_from_source`) for one company.
  - Background tasks for up to 10 companies.
  
- **Request Body Parameters:**
  - `filters`: Required filter conditions.
  - `offset`: Starting point of results (default is 0).
  - `limit`: Number of results (max 100).
  - Other optional parameters for sorting, aggregations, functions, groups, and background task triggers.

- **Sample Request (cURL):**
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/job_listings/Table/ \
      --header 'Authorization: Token $token' \
      --data '{
        "filters": {
            "op": "and",
            "conditions": [
                {"column": "company_id", "type": "in", "value": [7576, 680992]},
                {"column": "date_updated", "type": ">", "value": "2024-02-01"}
            ]
        },
        "offset": 0,
        "limit": 100
      }'
    ```

### 2. Funding Milestones
- Retrieve funding milestones for specified `company_id`.

- **Sample Request:**
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/funding_milestone_timeseries/ \
      --header 'Authorization: Token $auth_token' \
      --data '{"filters":{"op": "or", "conditions": [{"column": "company_id", "type": "in", "value": [637158, 674265]}]},"offset":0,"count":1000}'
    ```

### 3. Decision Makers
- Get decision makers for a specified `company_id`.
- Filter by titles including "CEO," "CFO," "CTO," and other senior positions.

- **Sample Request:**
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/decision_makers/ \
      --header 'Authorization: Token $auth_token' \
      --data '{"filters":{"op": "or","conditions":[{"column": "company_id", "type": "in", "value": [632328]}]},"offset":0,"count":100}'
    ```

### 4. LinkedIn Employee Headcount
- Get timeseries of employee headcount and follower count via `company_id` or `linkedin_id`.

### 5. Employee Headcount by Function
- Retrieve headcount by function for a given company.
  
- **Sample Request:**
    ```bash
    curl --request POST \
      --url https://api.crustdata.com/data_lab/linkedin_headcount_by_facet/Table/ \
      --header 'Authorization: Token $token' \
      --data '{
        "filters": {
          "op": "and", 
          "conditions": [{"column": "company_id", "type": "in", "value": [680992]}]
        }
      }'
    ```

### 6. Glassdoor Profile Metrics
- Retrieve ratings, number of reviews, and CEO approval ratings from Glassdoor using company information.

### 7. G2 Profile Metrics
- Get product ratings and reviews for companies using their website domain.

### 8. Web Traffic
- Access historical web traffic data for a company's website.
  
- **Sample Request:**
    ```bash
    curl --request POST \
      --url 'https://api.crustdata.com/data_lab/webtraffic/' \
      --header 'Authorization: Token $token' \
      --data '{"filters":{"op":"or","conditions":[{"column":"company_website","type":"(.)","value":"wefitanyfurniture.com"}]},"offset":0,"count":100}'
    ```

### 9. Investor Portfolio
- Retrieve investment portfolio details for specified investors by UUID or name.

- **Sample Request:**
    ```bash
    curl 'https://api.crustdata.com/data_lab/investor_portfolio?investor_uuid=<uuid>' \
      --header 'Authorization: Token $auth_token'
    ```

## Conclusion
Crustdata provides a detailed and structured API for accessing various datasets concerning companies and their operational metrics. Proper usage of filters, request parameters, and authentication is necessary to utilize the API effectively.

Summary of Document 3:
# Company Overview
## Firmographics
- **Key Attributes**: Company name, headquarters country, employee headcount by location, last funding round details, website and valuation information, industry classifications, and investor information.

## Founder Background
- **Details**: Names, LinkedIn profiles, locations, educational backgrounds, previous companies, and titles of company founders and decision-makers.

## Revenue
- **Estimates**: Lower and upper bounds of estimated revenue in USD.

## Employee Headcount
- **Metrics**: Total employee count, distribution across roles (engineering, sales, etc.), geographical headcount, and percentage changes over time.

## Employee Skills
- **Insights**: Comprehensive list of employee skills, proficiency distribution, and counts.

## Employee Ratings
- **Feedback Ratings**: Overall and category-based ratings from Glassdoor, including culture, diversity, work-life balance, and management approval.

## Product Reviews
- **Performance**: Number and average rating of reviews on G2.

## Web Traffic
- **Analytics**: Monthly visitor counts, traffic sources breakdown.

## Job Listings
- **Growth Insights**: Job openings by function with quarterly and six-month growth percentages, total listings, and their changes.

## Ads
- **Advertising Metrics**: Total ads served and active campaigns.

## SEO and Search Ranking
- **Visibility Metrics**: Organic and paid clicks, average ranks on Google, and ad campaign budgets.

## Google Search Impressions
- **Engagement**: Monthly and yearly impression counts with growth metrics.

## Twitter Engagement
- **Metrics**: Follower counts and engagement growth statistics.

## Social Media Posts
- **Content Tracking**: Company posts on LinkedIn and Twitter, including likes, shares, and comments.

## News Articles
- **Coverage**: Titles, links, publishers, and publication dates of articles featuring the company.

## Form D Filings
- **Regulatory Information**: Details on offerings, filing dates, and amounts.

# People Overview
## Profile and Background
- **Attributes**: LinkedIn profile URLs, personal details (name, title, contact info), connection counts, skills, and educational histories.