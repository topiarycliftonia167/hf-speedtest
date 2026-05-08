"""Resolve which CDN PoP a URL is being served from.

Sends a HEAD request and inspects:
  - x-hf-cdn-pop  (hf-cdn: aws-/dev-/gcp- prefixed region ids)
  - x-amz-cf-pop  (CloudFront: 3-letter IATA airport code)

Returns a "City, Country" label or "Unknown" when neither header is present.
"""

import httpx

from .iata import MAJOR_AIRPORT_IATAS

# AWS/GCP region → "City, Country" labels. Used to resolve hf-cdn pop_id values
# emitted via the x-hf-cdn-pop header.
AWS_REGION_LABELS: dict[str, str] = {
    "us-east-1": "Ashburn, USA",
    "us-east-2": "Columbus, USA",
    "us-west-1": "San Jose, USA",
    "us-west-2": "Boardman, USA",
    "af-south-1": "Cape Town, South Africa",
    "ap-east-1": "Hong Kong, China",
    "ap-south-1": "Mumbai, India",
    "ap-south-2": "Hyderabad, India",
    "ap-southeast-1": "Singapore, Singapore",
    "ap-southeast-2": "Sydney, Australia",
    "ap-southeast-3": "Jakarta, Indonesia",
    "ap-southeast-4": "Melbourne, Australia",
    "ap-southeast-5": "Kuala Lumpur, Malaysia",
    "ap-southeast-7": "Bangkok, Thailand",
    "ap-northeast-1": "Tokyo, Japan",
    "ap-northeast-2": "Seoul, South Korea",
    "ap-northeast-3": "Osaka, Japan",
    "ca-central-1": "Montreal, Canada",
    "ca-west-1": "Calgary, Canada",
    "eu-central-1": "Frankfurt, Germany",
    "eu-central-2": "Zurich, Switzerland",
    "eu-west-1": "Dublin, Ireland",
    "eu-west-2": "London, UK",
    "eu-west-3": "Paris, France",
    "eu-north-1": "Stockholm, Sweden",
    "eu-south-1": "Milan, Italy",
    "eu-south-2": "Zaragoza, Spain",
    "me-south-1": "Manama, Bahrain",
    "me-central-1": "Dubai, UAE",
    "mx-central-1": "Mexico City, Mexico",
    "il-central-1": "Tel Aviv, Israel",
    "sa-east-1": "São Paulo, Brazil",
}

GCP_REGION_LABELS: dict[str, str] = {
    "us-central1": "Council Bluffs, USA",
    "us-east1": "Moncks Corner, USA",
    "us-east4": "Ashburn, USA",
    "us-east5": "Columbus, USA",
    "us-west1": "The Dalles, USA",
    "us-west2": "Los Angeles, USA",
    "us-west3": "Salt Lake City, USA",
    "us-west4": "Las Vegas, USA",
    "us-south1": "Dallas, USA",
    "northamerica-northeast1": "Montreal, Canada",
    "northamerica-northeast2": "Toronto, Canada",
    "southamerica-east1": "São Paulo, Brazil",
    "southamerica-west1": "Santiago, Chile",
    "europe-central2": "Warsaw, Poland",
    "europe-north1": "Hamina, Finland",
    "europe-southwest1": "Madrid, Spain",
    "europe-west1": "St. Ghislain, Belgium",
    "europe-west2": "London, UK",
    "europe-west3": "Frankfurt, Germany",
    "europe-west4": "Eemshaven, Netherlands",
    "europe-west6": "Zurich, Switzerland",
    "europe-west8": "Milan, Italy",
    "europe-west9": "Paris, France",
    "europe-west10": "Berlin, Germany",
    "europe-west12": "Turin, Italy",
    "asia-east1": "Changhua County, Taiwan",
    "asia-east2": "Hong Kong, China",
    "asia-northeast1": "Tokyo, Japan",
    "asia-northeast2": "Osaka, Japan",
    "asia-northeast3": "Seoul, South Korea",
    "asia-south1": "Mumbai, India",
    "asia-south2": "Delhi, India",
    "asia-southeast1": "Singapore, Singapore",
    "asia-southeast2": "Jakarta, Indonesia",
    "australia-southeast1": "Sydney, Australia",
    "australia-southeast2": "Melbourne, Australia",
    "me-central1": "Doha, Qatar",
    "me-central2": "Dammam, Saudi Arabia",
    "me-west1": "Tel Aviv, Israel",
    "africa-south1": "Johannesburg, South Africa",
}


def resolve_hf_cdn_pop(pop_id: str) -> str:
    """Resolve an x-hf-cdn-pop value to a "City, Country" label.

    Conventions:
      aws-<region>  → AWS prod
      dev-<region>  → AWS or GCP dev (suffixed " (dev)")
      gcp-<region>  → GCP prod
    Falls back to the raw pop_id when the region is unknown.
    """
    if pop_id.startswith("aws-"):
        return AWS_REGION_LABELS.get(pop_id[4:], pop_id)
    if pop_id.startswith("dev-"):
        region = pop_id[4:]
        label = AWS_REGION_LABELS.get(region) or GCP_REGION_LABELS.get(region)
        return f"{label} (dev)" if label else pop_id
    if pop_id.startswith("gcp-"):
        return GCP_REGION_LABELS.get(pop_id[4:], pop_id)
    return pop_id


async def get_server_location(url: str) -> str:
    """Resolve which CDN PoP `url` is being served from. Returns "Unknown" on miss."""
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.head(url)

    hf_pop = response.headers.get("x-hf-cdn-pop")
    if hf_pop is not None:
        return resolve_hf_cdn_pop(hf_pop)

    cf_pop = response.headers.get("x-amz-cf-pop")
    if cf_pop is not None:
        iata = cf_pop.upper()[:3]
        if iata in MAJOR_AIRPORT_IATAS:
            city, country = MAJOR_AIRPORT_IATAS[iata]
            return f"{city}, {country}"

    return "Unknown"
