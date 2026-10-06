import streamlit as st
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Schema for Structured Event Intelligence (Historical Price Removed) ---
class EventItem(BaseModel):
    event_title: str = Field(description="Name of the event")
    city: str = Field(description="Location city")
    category: str = Field(description="Category e.g., Sports, Music, Family, Festival, Technology")
    target_age: str = Field(description="Target age group suitability")
    current_cost: float = Field(description="Current ticket price or 0 for free")
    deal_offers: str = Field(description="Available deals, promo codes, or free admission notes")
    why_its_best: str = Field(description="Why this ranks in the top 20% ROI events")
    personal_benefit: str = Field(description="How attending benefits the individual or family")
    price_worth_verdict: str = Field(description="Verdict: 🔥 Absolute Worth It, 🟡 Fair Value, ❌ Overpriced")
    roi_score: float = Field(description="Calculated value score out of 100")
    source_link: str = Field(description="Direct URL to ticket or event page")

# --- Streamlit Configuration ---
st.set_page_config(
    page_title="AI Event Recommendation & Intelligence Aggregator",
    page_icon="🎟️",
    layout="wide"
)

st.title("🎟️ Agentic Event Recommendation & Intelligence Aggregator")
st.markdown("Discover the top 20% high-ROI events tailored to your age, city, and interests in one central hub. View deal offers, personal benefits, and direct booking links.")

# --- Sidebar Search & Dynamic Criteria ---
st.sidebar.header("Event Search & Filtering Criteria")
user_city = st.sidebar.selectbox("Select City / Region", ["Santa Clara, CA", "San Francisco, CA", "San Jose, CA", "Half Moon Bay, CA"])
user_age_group = st.sidebar.selectbox("Age Group Suitability", ["All Ages / Family", "Adults (21+)", "Teens & Young Adults"])

selected_interests = st.sidebar.multiselect(
    "Interests & Categories",
    ["Sports", "Music & Concerts", "Festivals & Fairs", "Family & Community", "Technology & Science"],
    default=["Sports", "Music & Concerts", "Family & Community", "Festivals & Fairs"]
)

max_ticket_budget = st.sidebar.slider("Maximum Ticket Budget ($ USD)", min_value=0, max_value=500, value=150, step=10)

sort_by = st.sidebar.selectbox(
    "Sort Recommendations By",
    ["Highest ROI / Best Value Score", "Lowest Ticket Price"]
)

if st.button("Run Event Intelligence Aggregator", type="primary"):
    with st.spinner(f"Agents aggregating top-rated events for {user_city} under ${max_ticket_budget}..."):
        
        # Mock database of top-tier aggregated events validated via Pydantic v2
        mock_events = [
            EventItem(
                event_title="Bruno Mars: The Romantic Tour (Levi's Stadium)",
                city="Santa Clara, CA",
                category="Music & Concerts",
                target_age="All Ages / Family",
                current_cost=125.00,
                deal_offers="SeatGeek promo codes available for upper-tier seating.",
                why_its_best="Stadium-scale global concert draw with elite live production.",
                personal_benefit="Creates unforgettable family memories and provides high-energy emotional rejuvenation.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=92.5,
                source_link="https://seatgeek.com"
            ),
            EventItem(
                event_title="Bay Area Science Festival (UCSF Mission Bay)",
                city="San Francisco, CA",
                category="Technology & Science",
                target_age="All Ages / Family",
                current_cost=0.00,
                deal_offers="Free admission with online RSVP.",
                why_its_best="Massive one-day celebration of science with interactive learning for all ages.",
                personal_benefit="Inspires curiosity in children and exposes attendees to cutting-edge tech and scientific breakthroughs.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=98.0,
                source_link="https://sf.funcheap.com"
            ),
            EventItem(
                event_title="54th Annual Half Moon Bay Art & Pumpkin Festival",
                city="Half Moon Bay, CA",
                category="Festivals & Fairs",
                target_age="All Ages / Family",
                current_cost=0.00,
                deal_offers="Free street admission; parking passes available online.",
                why_its_best="Iconic California fall festival celebrating giant gourds, artisan crafts, and local food.",
                personal_benefit="Terrific weekend outdoor bonding experience with exceptional seasonal food and community atmosphere.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=95.0,
                source_link="https://hmbpumpkinfest.com"
            ),
            EventItem(
                event_title="San Francisco Fleet Week: Blue Angels Air Show",
                city="San Francisco, CA",
                category="Festivals & Fairs",
                target_age="All Ages / Family",
                current_cost=0.00,
                deal_offers="Free waterfront viewing along Marina Green.",
                why_its_best="World-class aviation exhibition drawing millions with breathtaking aerial stunts.",
                personal_benefit="Thrilling spectacle that sparks wonder and provides an exhilarating weekend outing.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=96.5,
                source_link="https://sf.funcheap.com"
            ),
            EventItem(
                event_title="Children's SpooktaClara Halloween Party (Central Park)",
                city="Santa Clara, CA",
                category="Family & Community",
                target_age="All Ages / Family",
                current_cost=0.00,
                deal_offers="Free community event hosted by Discover Santa Clara.",
                why_its_best="Safe, daytime trick-or-treating and family activities in a signature local park.",
                personal_benefit="Engages young children in community holiday celebrations in a secure, friendly environment.",
                price_worth_verdict="🔥 Absolute Worth It",
                roi_score=90.0,
                source_link="https://www.discoversantaclara.org"
            )
        ]
        
        # Convert models using Pydantic v2 model_dump()
        df = pd.DataFrame([event.model_dump() for event in mock_events])
        
        # Filter based on user criteria
        filtered_df = df[
            (df["current_cost"] <= max_ticket_budget) &
            (df["category"].isin(selected_interests))
        ]
        
        if sort_by == "Highest ROI / Best Value Score":
            filtered_df = filtered_df.sort_values(by="roi_score", ascending=False)
        elif sort_by == "Lowest Ticket Price":
            filtered_df = filtered_df.sort_values(by="current_cost", ascending=True)
            
        st.success(f"Aggregated {len(filtered_df)} top-tier recommended events matching your criteria!")
        
        # --- Top Summary Metrics ---
        col1, col2, col3 = st.columns(3)
        if not filtered_df.empty:
            free_events_count = len(filtered_df[filtered_df["current_cost"] == 0])
            avg_cost = filtered_df["current_cost"].mean()
            col1.metric("Top Recommended Events", len(filtered_df))
            col2.metric("Free Admission Events", free_events_count)
            col3.metric("Average Ticket Cost", f"${avg_cost:.2f}")
        
        # --- Main Tabular Display ---
        st.subheader("📊 Top 20% High-ROI Event Intelligence Table")
        
        if not filtered_df.empty:
            display_df = filtered_df[[
                "event_title", "city", "category", "current_cost", 
                "deal_offers", "price_worth_verdict", "roi_score"
            ]].copy()
            
            display_df.columns = [
                "Event Title", "City", "Category", "Cost ($)", 
                "Deals & Offers", "Worth It Verdict", "ROI Score"
            ]
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("### 🔍 Detailed Breakdown, Personal Benefits & Suggested Next Steps")
            for _, row in filtered_df.iterrows():
                with st.expander(f"📍 {row['event_title']} ({row['city']}) — Cost: ${row['current_cost']} [{row['price_worth_verdict']}]"):
                    c_left, c_right = st.columns([2, 1])
                    with c_left:
                        st.markdown(f"* **Category & Target:** {row['category']} | Suitable for: `{row['target_age']}`")
                        st.markdown(f"* **Why It's a Top Recommendation:** {row['why_its_best']}")
                        st.markdown(f"* **Personal Benefit:** {row['personal_benefit']}")
                        st.markdown(f"* **Deals & Offers Available:** {row['deal_offers']}")
                        st.markdown(f"* **Suggested Next Steps:** Review schedule, secure free RSVPs or advance tickets early, and add event reminder to family calendar.")
                    with c_right:
                        st.link_button("🔗 Secure Tickets / Source Link", row["source_link"])
        else:
            st.warning("No events matched your exact category and budget filters. Try expanding your interest selections or increasing your maximum ticket budget.")
else:
    st.info("Configure your search criteria in the sidebar and click **Run Event Intelligence Aggregator** to view recommended events.")
