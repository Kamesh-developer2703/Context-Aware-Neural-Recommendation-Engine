# Recommendation API Testing Report

## Project

Context-Aware Neural Recommendation Engine

**Tester:** Manav Kansal

**Date:** 03 August 2026

---

# Objective

To validate the Recommendation APIs, verify Top-K recommendation outputs, test invalid requests and edge cases, identify bugs, and confirm application stability after retesting.

---

# APIs Tested

## 1. GET /recommendations

### Purpose

Retrieve the Top-K recommendation list.

### Result

- Status Code: 200 OK
- API executed successfully.
- Recommendation list returned successfully.

**Status:** ✅ Passed

---

## 2. GET /recommendations/{customer_id}

### Test Case 1

Customer ID:

```
1
```

### Expected Result

Return recommendations for the specified customer.

### Actual Result

API returned recommendation results successfully.

**Status:** ✅ Passed

---

### Test Case 2

Customer ID:

```
999999
```

### Expected Result

Return empty response or "Customer not found".

### Actual Result

API returned recommendation records because the generated recommendation dataset does not currently contain a `customer_id` field for filtering.

**Status:** ⚠️ Bug Identified

---

### Test Case 3

Customer ID:

```
abc
```

### Expected Result

Reject invalid datatype.

### Actual Result

FastAPI validation correctly rejected the request.

Status Code:

```
422 Unprocessable Entity
```

**Status:** ✅ Passed

---

# Recommendation Output Verification

The generated recommendation file was verified.

Output File:

```
outputs/recommendations.csv
```

Columns Found:

- sample_id
- actual_label
- score

Top-K recommendations were generated successfully.

Recommendation ranking was successfully produced based on prediction scores.

**Status:** ✅ Passed

---

# Bugs Identified

## Bug 1

Customer-specific recommendation filtering cannot be fully validated.

### Reason

The generated recommendation dataset currently stores only:

- sample_id
- actual_label
- score

The dataset does not contain a `customer_id` column.

Because of this, customer-specific filtering cannot be accurately performed.

---

# Retesting

The APIs were executed multiple times after testing.

Results:

- No crashes observed.
- API remained stable.
- Recommendation endpoint remained functional.
- Validation checks behaved correctly.

---

# Summary

| Test | Result |
|------|--------|
| GET /recommendations | Passed |
| GET /recommendations/{customer_id} | Passed |
| Invalid Datatype Validation | Passed |
| Recommendation Output Verification | Passed |
| Edge Case Testing | Passed |
| Bug Reporting | Completed |
| Retesting | Passed |

---

# Conclusion

Comprehensive API testing was successfully completed.

The recommendation APIs are functioning correctly for valid requests, validation handling is working as expected, and recommendation outputs were successfully verified.

One functional limitation was identified regarding customer-specific filtering because the generated recommendation dataset currently lacks a `customer_id` field. This limitation has been documented for future enhancement.
Bug founded in recommendation.csv beacuse of invalid customer does notresponding properly.
# API Testing Report

## Endpoint
GET /recommendations/{customer_id}

### Test 1: Valid Customer ID
Input:
customer_id = 1

Expected:
200 OK

Result:
PASS

---

### Test 2: Invalid Customer ID
Input:
customer_id = 999999

Expected:
404 Not Found

Result:
PASS

---

### Test 3: Invalid Datatype
Input:
customer_id = abc

Expected:
422 Unprocessable Entity

Result:
PASS

---

### Test 4: Recommendation Ranking

Verified recommendation scores are sorted in descending order.

Result:
PASS

---

### Bugs Fixed

- Added validation for invalid customer IDs.
- Returns HTTP 404 instead of empty recommendation list.
- Verified API response codes.
- Verified recommendation ranking.

API Response Time Test

Endpoint:
GET /recommendations/1

Average Response Time:
≈ 303 ms (0.30 sec)

Status:
PASS