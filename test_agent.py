import streamlit as st
import logging
import traceback
from agno.agent import Agent
from agno.models.google import Gemini
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_agent_output(text):
    # Extract fields using new delimiters in agent's response
    rec = re.search(r"Rec:([^|]+)", text)
    rat = re.search(r"Why:([^|]+)", text)
    factors = re.search(r"Factors:([^|]+)", text)
    outlook = re.search(r"Outlook:([^|]+)", text)
    prices = re.search(r"Targets:([^|]+)", text)
    return (
        rec.group(1).strip() if rec else "Undefined recommendation",
        rat.group(1).strip() if rat else "No explanation provided",
        factors.group(1).strip() if factors else "No factors detailed",
        outlook.group(1).strip() if outlook else "No outlook available",
        prices.group(1).strip() if prices else "No price targets provided",
    )

def main():
    st.title("Test Agent Functionality")
    
    # Simple input
    api_key = st.text_input("Google API Key 🔑", type="password")
    
    if not api_key:
        st.info("Enter your Google API key to test the agent.")
        return
    
    # Basic test data
    symbol = "BTC"
    price = 83000
    mood = "Neutral"
    buzz = "Moderate"
    volume = 1000000000
    cap = 1000000000000
    
    # Simple prompt
    prompt = (f"Analyze {symbol} now at ${price}.\n"
              f"Market mood is: {mood} and social buzz: {buzz}.\n"
              f"Volume: ${volume:,.0f}, Cap: ${cap:,.0f}.\n\n"
              "Provide your analysis in a single response with these parts separated by | symbol in order:\n"
              "Rec: [Buy/Hold/Sell] | Why: [Explain your reasoning] | Factors: [List key factors] | "
              "Outlook: [Provide 1-week outlook] | Targets: [Supply price targets]\n"
              "Ensure none of the fields are empty and keep your answer around 150 words.")
    
    if st.button("Run Test"):
        try:
            # Initialize Agent
            st.info("Initializing agent...")
            agent = Agent(
                model=Gemini(id="gemini-2.0-flash", api_key=api_key),  # Try a different model version
                tools=[], show_tool_calls=True, markdown=True
            )
            
            st.info("Running agent query...")
            ai_response = agent.run(prompt)
            
            if ai_response is None:
                st.error("Agent returned None response.")
                return
                
            output_text = ai_response.content if hasattr(ai_response, 'content') else None
            
            if output_text is None:
                st.error("Agent returned empty content.")
                return
            
            st.success("Agent query successful!")
            st.subheader("Raw Response")
            st.text(output_text)
            
            # Parse the response
            rec, rationale, factors, outlook, targets = extract_agent_output(output_text)
            
            st.subheader("Parsed Results")
            st.write(f"**Recommendation:** {rec}")
            st.write(f"**Rationale:** {rationale}")
            st.write(f"**Factors:** {factors}")
            st.write(f"**Outlook:** {outlook}")
            st.write(f"**Targets:** {targets}")
            
        except Exception as e:
            st.error(f"Test failed: {str(e)}")
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()
