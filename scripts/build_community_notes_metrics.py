#!/usr/bin/env python3
"""Build de-identified aggregate metrics from Community Notes TSV exports."""

import argparse
import csv
import json
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


REASON_COLUMNS = {
    "misleadingFactualError": "Factual error",
    "misleadingManipulatedMedia": "Manipulated media",
    "misleadingOutdatedInformation": "Outdated information",
    "misleadingMissingImportantContext": "Missing important context",
    "misleadingUnverifiedClaimAsFact": "Unverified claim as fact",
    "misleadingSatire": "Satire",
    "misleadingOther": "Other misleading reason",
    "notMisleadingFactuallyCorrect": "Factually correct",
    "notMisleadingOutdatedButNotWhenWritten": "Outdated after publication",
    "notMisleadingClearlySatire": "Clearly satire",
    "notMisleadingPersonalOpinion": "Personal opinion",
    "notMisleadingOther": "Other non-misleading reason",
}

HELPFUL_RATING_COLUMNS = {
    "helpfulInformative": "Informative",
    "helpfulClear": "Clear",
    "helpfulEmpathetic": "Empathetic",
    "helpfulGoodSources": "Good sources",
    "helpfulUniqueContext": "Unique context",
    "helpfulAddressesClaim": "Addresses the claim",
    "helpfulImportantContext": "Adds important context",
    "helpfulUnbiasedLanguage": "Unbiased language",
    "helpfulOther": "Other helpful reason",
}

NOT_HELPFUL_RATING_COLUMNS = {
    "notHelpfulIncorrect": "Incorrect",
    "notHelpfulSourcesMissingOrUnreliable": "Sources missing or unreliable",
    "notHelpfulOpinionSpeculationOrBias": "Opinion, speculation, or bias",
    "notHelpfulMissingKeyPoints": "Missing key points",
    "notHelpfulOutdated": "Outdated",
    "notHelpfulHardToUnderstand": "Hard to understand",
    "notHelpfulArgumentativeOrBiased": "Argumentative or biased",
    "notHelpfulOffTopic": "Off topic",
    "notHelpfulSpamHarassmentOrAbuse": "Spam, harassment, or abuse",
    "notHelpfulIrrelevantSources": "Irrelevant sources",
    "notHelpfulOpinionSpeculation": "Opinion or speculation",
    "notHelpfulNoteNotNeeded": "Note not needed",
    "notHelpfulOther": "Other unhelpful reason",
}


def iso_date(milliseconds):
    if milliseconds is None:
        return None
    return datetime.fromtimestamp(milliseconds / 1000, tz=timezone.utc).date().isoformat()


def as_positive_timestamp(value):
    if not value or value == "-1":
        return None
    timestamp = int(value)
    if timestamp <= 1:
        return None
    return timestamp * 1000 if timestamp < 100_000_000_000 else timestamp


def scan_notes(paths):
    total = 0
    classifications = Counter()
    reasons = Counter()
    collaborative = 0
    source_flagged = 0
    min_millis = None
    max_millis = None

    for path in paths:
        with path.open(encoding="utf-8", errors="replace", newline="") as source:
            for row in csv.DictReader(source, delimiter="\t"):
                total += 1
                classifications[row.get("classification") or "UNSPECIFIED"] += 1
                collaborative += row.get("isCollaborativeNote") == "1"
                source_flagged += row.get("trustworthySources") == "1"

                for column, label in REASON_COLUMNS.items():
                    if row.get(column) == "1":
                        reasons[label] += 1

                created = int(row["createdAtMillis"])
                min_millis = created if min_millis is None or created < min_millis else min_millis
                max_millis = created if max_millis is None or created > max_millis else max_millis

    return {
        "totalNotes": total,
        "classificationCounts": dict(classifications),
        "reasonCounts": dict(reasons.most_common()),
        "collaborativeNotes": collaborative,
        "notesFlaggedWithTrustworthySources": source_flagged,
        "createdDateRange": {"start": iso_date(min_millis), "end": iso_date(max_millis)},
    }


def scan_status_history(path):
    total = 0
    statuses = Counter()
    decision_models = Counter()
    hours_to_first_status = []
    min_millis = None
    max_millis = None

    with path.open(encoding="utf-8", errors="replace", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            total += 1
            statuses[row.get("currentStatus") or "UNSPECIFIED"] += 1
            decision_models[row.get("currentDecidedBy") or "UNSPECIFIED"] += 1

            created = int(row["createdAtMillis"])
            first_status = as_positive_timestamp(row.get("timestampMillisOfFirstNonNMRStatus"))
            if first_status and first_status >= created:
                hours_to_first_status.append((first_status - created) / 3_600_000)

            min_millis = created if min_millis is None or created < min_millis else min_millis
            max_millis = created if max_millis is None or created > max_millis else max_millis

    return {
        "totalStatusRecords": total,
        "currentStatusCounts": dict(statuses),
        "decisionModelCounts": dict(decision_models.most_common()),
        "medianHoursToFirstNonPendingStatus": round(statistics.median(hours_to_first_status), 1)
        if hours_to_first_status
        else None,
        "recordsWithNonPendingLatency": len(hours_to_first_status),
        "createdDateRange": {"start": iso_date(min_millis), "end": iso_date(max_millis)},
    }


def scan_bat_signals(path):
    total = 0
    eligible = Counter()
    with_source_links = 0
    with_suggestions = 0

    eligibility_columns = {
        "noteRequestFeedEligibleAtMillis": "noteRequestFeed",
        "apiSmallFeedEligibleAtMillis": "smallApiFeed",
        "apiLargeFeedEligibleAtMillis": "largeApiFeed",
        "apiXlFeedEligibleAtMillis": "xlApiFeed",
    }

    with path.open(encoding="utf-8", errors="replace", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            total += 1
            for column, label in eligibility_columns.items():
                eligible[label] += as_positive_timestamp(row.get(column)) is not None
            with_source_links += bool((row.get("sourceLinks") or "").strip())
            with_suggestions += (row.get("suggestions") or "").strip() not in ("", "[]")

    return {
        "totalSignalRecords": total,
        "eligibilityCounts": dict(eligible),
        "recordsWithSourceLinks": with_source_links,
        "recordsWithSuggestions": with_suggestions,
    }


def scan_ratings(path):
    total = 0
    helpfulness = Counter()
    helpful_reasons = Counter()
    not_helpful_reasons = Counter()
    source_buckets = Counter()
    versions = Counter()
    min_millis = None
    max_millis = None

    with path.open(encoding="utf-8", errors="replace", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            total += 1
            helpfulness[row.get("helpfulnessLevel") or "UNSPECIFIED"] += 1
            source_buckets[row.get("ratingSourceBucketed") or "UNSPECIFIED"] += 1
            versions[row.get("version") or "UNSPECIFIED"] += 1

            for column, label in HELPFUL_RATING_COLUMNS.items():
                if row.get(column) == "1":
                    helpful_reasons[label] += 1
            for column, label in NOT_HELPFUL_RATING_COLUMNS.items():
                if row.get(column) == "1":
                    not_helpful_reasons[label] += 1

            created = int(row["createdAtMillis"])
            min_millis = created if min_millis is None or created < min_millis else min_millis
            max_millis = created if max_millis is None or created > max_millis else max_millis

    return {
        "totalRatings": total,
        "helpfulnessCounts": dict(helpfulness),
        "helpfulReasonCounts": dict(helpful_reasons.most_common()),
        "notHelpfulReasonCounts": dict(not_helpful_reasons.most_common()),
        "ratingSourceCounts": dict(source_buckets.most_common()),
        "versionCounts": dict(versions.most_common()),
        "createdDateRange": {"start": iso_date(min_millis), "end": iso_date(max_millis)},
    }


def scan_enrollment(path):
    total = 0
    states = Counter()
    populations = Counter()
    groups = Counter()
    earned_out_counts = Counter()
    ratings_needed = Counter()
    min_millis = None
    max_millis = None

    with path.open(encoding="utf-8", errors="replace", newline="") as source:
        for row in csv.DictReader(source, delimiter="\t"):
            total += 1
            states[row.get("enrollmentState") or "UNSPECIFIED"] += 1
            populations[row.get("modelingPopulation") or "UNSPECIFIED"] += 1
            groups[row.get("modelingGroup") or "UNSPECIFIED"] += 1
            earned_out_counts[row.get("numberOfTimesEarnedOut") or "UNSPECIFIED"] += 1
            ratings_needed[row.get("successfulRatingNeededToEarnIn") or "UNSPECIFIED"] += 1

            changed = as_positive_timestamp(row.get("timestampOfLastStateChange"))
            if changed:
                min_millis = changed if min_millis is None or changed < min_millis else min_millis
                max_millis = changed if max_millis is None or changed > max_millis else max_millis

    return {
        "totalParticipants": total,
        "enrollmentStateCounts": dict(states.most_common()),
        "modelingPopulationCounts": dict(populations.most_common()),
        "modelingGroupCounts": dict(groups.most_common()),
        "timesEarnedOutCounts": dict(earned_out_counts.most_common()),
        "successfulRatingsNeededCounts": dict(ratings_needed.most_common()),
        "lastStateChangeDateRange": {"start": iso_date(min_millis), "end": iso_date(max_millis)},
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--notes", nargs="+", required=True, type=Path)
    parser.add_argument("--status-history", required=True, type=Path)
    parser.add_argument("--bat-signals", required=True, type=Path)
    parser.add_argument("--ratings", type=Path)
    parser.add_argument("--user-enrollment", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    result = {
        "dataset": "Community Notes public data export",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "privacy": "Aggregate metrics only; participant IDs and note text are excluded.",
        "interpretation": "Statuses describe note-rating outcomes, not whether the underlying post is true or false.",
        "notes": scan_notes(args.notes),
        "statusHistory": scan_status_history(args.status_history),
        "batSignals": scan_bat_signals(args.bat_signals),
    }
    if args.ratings:
        result["ratings"] = scan_ratings(args.ratings)
    if args.user_enrollment:
        result["userEnrollment"] = scan_enrollment(args.user_enrollment)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
