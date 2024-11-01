# AI21 JambaCare App

## Overview
The AI21 JambaCare App is a Streamlit application designed to help users compare healthcare plans using the Jamba-1.5-Large model from AI21. With this tool, you can easily analyze and compare various plans based on specific questions regarding coverage, costs, and other critical details.

## Features
- **Compare Healthcare Plans**: Select up to two healthcare plans and ask specific questions to get detailed comparisons.
- **Pre-Populated Questions**: Choose from a list of common questions or input your own to guide the analysis.
- **Customizable**: While this app focuses on healthcare plan comparisons, you can adapt it to compare any type of documents, such as resumes, legal contracts, or research papers.

## Live Demo
You can try the app online at: [AI21 JambaCare App](https://jambacare-qgomybb58qbvah3q3whys9.streamlit.app/)

## Setup for Local Use
To run the app locally:
1. Clone this repository.
2. Install the required packages:
   ```bash
   pip install streamlit requests
   ```
3. Replace the `streamlit secrets` API key with your actual AI21 API key, which you can sign up for [here](https://studio.ai21.com/login).
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Customization
Feel free to modify the code to suit your specific use case! You can change the data inputs, the types of questions, or even the underlying model settings to fit different document comparison needs.

## Resources
- [AI21 Labs Industry Samples](https://github.com/AI21Labs/AI21-Industry-Samples)
- [Jamba 1.5 API Documentation](https://docs.ai21.com/reference/jamba-15-api-ref)

Explore, customize, and build your own document comparison tools using this framework!
