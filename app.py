import streamlit as st
import requests
import os
import re
import json

# Hardcoded API key
API_KEY = st.secrets["AI21_API_KEY"]

def call_ai21_api(prompt):
    url = 'https://api.ai21.com/studio/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": "jamba-1.5-large",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048,
        "temperature": 0.4,
        "top_p": 1
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling AI21 API: {e}")
        return None

def clean_text(text):
    text = re.sub(r'[®©™]', '', text)
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return clean_text(content)

def generate_prompt_template(selected_files, question):
    prompt_template = "#################################\n"
    for i, file in enumerate(selected_files, 1):
        file_path = os.path.join('./data', file)
        file_content = read_file(file_path)
        plan_name = os.path.splitext(file)[0]
        
        prompt_template += f"PLAN: {plan_name}\n"
        prompt_template += f"PLANDETAILS: {file_content}\n"
        prompt_template += "#################################\n\n"
    
    if question:
        prompt_template += "#################################\nCOMPARE THE ABOVE HEALTHCARE PLANS AND ANSWER THIS QUESTION:\n"
        prompt_template += clean_text(question)
    
    return prompt_template

def escape_markdown(text):
    chars_to_escape = ['$', '*', '_', '[', ']', '(', ')', '#', '+', '-', '.', '!']
    for char in chars_to_escape:
        text = text.replace(char, '\\' + char)
    return text

def main():
    st.title("AI21 JambaCare | Healthcare Plan Comparison Assistant :health_worker::snake:")

    st.write("""
    Welcome to the [AI21](https://www.ai21.com/) JambaCare App! This tool empowers you to quickly compare healthcare plans. 
             
    With the help of the [Jamba-1.5-Large model](https://www.ai21.com/jamba), you can pose specific questions to guide your decision-making process. Whether your focus is on out-of-pocket costs, prescription coverage, or options for families, this app facilitates the comparison of up to two plans simultaneously!

    By utilizing Jamba 1.5 from AI21, you benefit from its ability to handle long context inputs of up to 256k tokens. This capability is particularly advantageous when comparing extensive healthcare plans, ensuring you receive thorough and comprehensive insights tailored to your needs.

    For more information about specific plans, you can access the [coverage policy documents here](https://www.bluecrossma.org/myblue/learn-and-save/plans-and-benefits/coverage-policy-documents). Each one of these plans is hundreds of pages long and dense with detail. Jamba 1.5 helps you quickly navigate and compare the key details.
""")
    
    st.info("""The app currently compares healthcare plans, but you can easily modify it to compare any type of documents - resumes, 
    legal contracts, research papers, or any other text-based documents. Feel free to use this code as a starting point 
    and adapt it to your specific use case!""")
    
    # Initialize session state for the question
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""
    
    # File selection
    data_folder = './data'
    txt_files = [f for f in os.listdir(data_folder) if f.endswith('.txt')]
    selected_files = st.multiselect("Select up to 2 healthcare plans to compare", txt_files, max_selections=2)
    
    # Pre-populated questions dropdown
    pre_populated_questions = [
        "Select a pre-populated question...",
        "What are the differences between these plans?",
        "Which plan offers the best coverage for dental services?",
        "How do the costs compare between these plans?",
        "What are the deductibles for each plan?",
        "What are the copayments for primary care visits between these plans?",
        "What are the prescription drug benefits of these plans?"
    ]
    
    selected_question = st.selectbox(
        "Choose a common question or type your own below:",
        pre_populated_questions
    )
    
    # Update the text area if a pre-populated question is selected
    if selected_question != "Select a pre-populated question...":
        st.session_state.current_question = selected_question
    
    # Question input text area
    question = st.text_area(
        "What would you like to know about these plans?",
        value=st.session_state.current_question,
        help="Ask any question about the selected healthcare plans"
    )

    if st.button("Compare Plans"):
        if not selected_files:
            st.warning("Please select at least one healthcare plan.")
        elif not question:
            st.warning("Please enter a question about the plans.")
        else:
            with st.spinner("Analyzing plans..."):
                # Generate prompt behind the scenes
                prompt = generate_prompt_template(selected_files, question)
                
                # Get AI response
                response = call_ai21_api(prompt)
                
                if response:
                    try:
                        if 'choices' in response and len(response['choices']) > 0:
                            choice = response['choices'][0]
                            if 'message' in choice:
                                message = choice['message']['content']
                            elif 'messages' in choice:
                                message = choice['messages']
                            elif 'mesages' in choice:
                                message = choice['mesages']
                            else:
                                message = str(choice)
                        else:
                            message = str(response)
                        
                        st.write("### Analysis:")
                        escaped_message = escape_markdown(message)
                        st.write(escaped_message)
                        
                        # Add debug expander with full API response
                        with st.expander("View API Response"):
                            st.json(response)
                            
                    except KeyError as e:
                        st.error(f"An error occurred while analyzing the plans: {e}")
                        # Show the raw response in case of error for debugging
                        with st.expander("View API Response"):
                            st.json(response)

    st.markdown("---")
    st.write("Note: This app uses the Jamba-1.5-Large model to analyze insurance plans. The app  makes a single call to Jamba with concatenated plan details for efficient comparison.")


    # Add resources section at the bottom
    with st.expander("📚 Resources for Builders"):
        st.markdown("""
        Want to build something similar? Check out these helpful resources:
        
        - [AI21 Labs Industry Samples](https://github.com/AI21Labs/AI21-Industry-Samples) - Collection of example applications and use cases
        - [Jamba 1.5 API Documentation](https://docs.ai21.com/reference/jamba-15-api-ref) - Complete API reference for the Jamba model
        
        Feel free to fork, modify, and build upon this example for your own applications!
        """)
if __name__ == "__main__":
    main()