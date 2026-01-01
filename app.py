import streamlit as st

# Import the planner from the tools.agent package
from tools.agent import plan_trip_with_agent

st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")

st.title("✈️ Agentic AI Travel Planner")

with st.sidebar:
    st.header("Trip details")
    origin = st.text_input("Origin city", "Mumbai")
    destination = st.text_input("Destination city", "Goa")
    days = st.number_input("Number of days", min_value=1, max_value=30, value=3)
    budget = st.number_input("Total budget (INR)", min_value=1000, value=20000, step=1000)
    trip_type = st.selectbox(
        "Trip type",
        ["Leisure", "Adventure", "Family", "Romantic", "Business"],
    )
    preferences = st.text_area(
        "Preferences (food, activities, pace, etc.)",
        "Beach, local food, moderate pace",
    )

st.markdown(
    "Ask for a trip plan or modify an existing one. "
    "The planner will use flights, hotels, places and weather to build an itinerary."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Describe your trip request...")

if user_prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Combine sidebar details with chat input
    full_request = (
        f"{user_prompt}\n\n"
        f"Trip details:\n"
        f"- Origin: {origin}\n"
        f"- Destination: {destination}\n"
        f"- Days: {days}\n"
        f"- Total budget: {budget} INR\n"
        f"- Trip type: {trip_type}\n"
        f"- Preferences: {preferences}\n"
    )

    with st.chat_message("assistant"):
        with st.spinner("Planning your trip..."):
            itinerary = plan_trip_with_agent(
                user_request=full_request,
                origin=origin,
                destination=destination,
                days=int(days),
                total_budget=int(budget),
                trip_type=trip_type,
            )
            st.markdown(itinerary)

    st.session_state.messages.append({"role": "assistant", "content": itinerary})