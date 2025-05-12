from fastmcp import FastMCP
from typing import Annotated, Optional
from pydantic import Field

mcp = FastMCP(
    name="Test Ads Campaign MCP",
    instructions="A test MCP server for ads campaign management. All data is mock/test only."
)


@mcp.tool()
def setup_campaign(
    customer_id: Annotated[str, Field(description="Google Ads customer ID, e.g. '123-456-7890'")],
    campaign_name: Annotated[str, Field(description="Name for the new campaign")],
    daily_budget: Annotated[float, Field(description="Daily budget in account currency")],
    start_date: Annotated[str, Field(description="Campaign start date, YYYY-MM-DD")],
    end_date: Annotated[Optional[str], Field(
        description="Campaign end date, YYYY-MM-DD (optional)")] = None,
) -> dict:
    """
    Launch a new (mock) campaign for the given customer.
    Returns a mock campaign object with an ID and status.
    """
    return {
        "campaign_id": "999999",
        "customer_id": customer_id,
        "name": campaign_name,
        "status": "ENABLED",
        "daily_budget": daily_budget,
        "start_date": start_date,
        "end_date": end_date,
    }


@mcp.tool()
def get_campaign_performance(
    customer_id: Annotated[str, Field(description="Google Ads customer ID")],
    campaign_id: Annotated[str, Field(description="Campaign ID")],
    date_range: Annotated[str, Field(description="Date range, e.g. 'LAST_30_DAYS' or '2024-01-01:2024-01-31'")],
) -> dict:
    """
    Retrieve mock performance metrics for a campaign.
    Returns clicks, impressions, cost, conversions, etc.
    """
    return {
        "campaign_id": campaign_id,
        "customer_id": customer_id,
        "date_range": date_range,
        "metrics": {
            "impressions": 12345,
            "clicks": 678,
            "cost_micros": 123456789,
            "conversions": 12,
            "ctr": 0.0549,
            "average_cpc_micros": 182123,
        }
    }


@mcp.tool()
def modify_campaign(
    customer_id: Annotated[str, Field(description="Google Ads customer ID")],
    campaign_id: Annotated[str, Field(description="Campaign ID")],
    new_status: Annotated[Optional[str], Field(
        description="New status, e.g. 'PAUSED', 'ENABLED'")] = None,
    new_budget: Annotated[Optional[float], Field(
        description="New daily budget (optional)")] = None,
) -> dict:
    """
    Update campaign settings (status, budget) for a mock campaign.
    Returns the updated campaign object.
    """
    updated = {
        "campaign_id": campaign_id,
        "customer_id": customer_id,
        "status": new_status or "UNCHANGED",
        "daily_budget": new_budget or "UNCHANGED",
    }
    return updated


def main():
    mcp.run()


if __name__ == "__main__":
    main()
