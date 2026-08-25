# KSA SaaS Features & Government Portal Gating for Frappe

A multi-tenant feature-gating and Saudi government HR compliance integration app for Frappe/ERPNext (Muqeem, Mudad WPS, GOSI).

## Features
- **SaaS Feature Gate Decorator:** Protects backend endpoints based on active tenant subscriptions, expiry dates, and API call quotas.
- **Dynamic UI Gating:** Passes subscription status through `frappe.boot` to show/hide action buttons dynamically.
- **Saudi HR Connectors:** Ready-to-extend service layer for Elm Muqeem, Mudad WPS, and GOSI.

## Installation
```bash
bench get-app [https://github.com/](https://github.com/)<YOUR_USERNAME>/ksa_saas_features
bench --site <site_name> install-app ksa_saas_features
bench --site <site_name> migrate
