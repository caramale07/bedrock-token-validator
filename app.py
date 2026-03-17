import streamlit as st
import requests
import json

st.set_page_config(page_title="Bedrock Token Validator", layout="centered")
st.title("Bedrock Token Validator")
st.caption("Test your Bedrock API key and model access with a single request.")

with st.form("bedrock_form"):
    api_key = st.text_input("Bedrock API Key", type="password")
    region = st.text_input("AWS Region", value="us-east-1")
    model_id = st.text_input(
        "Model ID / Inference Profile ARN",
        value="us.anthropic.claude-sonnet-4-6",
    )
    prompt = st.text_area("Prompt", value="Say hello in one sentence.")
    submitted = st.form_submit_button("Send Request")

if submitted:
    if not api_key or not model_id:
        st.error("API Key and Model ID are required.")
    else:
        try:
            url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{requests.utils.quote(model_id, safe='')}/invoke"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            body = {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 256,
                "anthropic_version": "bedrock-2023-05-31",
            }

            with st.spinner("Calling Bedrock..."):
                response = requests.post(
                    url, headers=headers, json=body, timeout=60
                )

            if response.ok:
                result = response.json()
                st.success("Request succeeded — API key and model ID are valid.")
                st.subheader("Response")
                if "content" in result:
                    for block in result["content"]:
                        if block.get("type") == "text":
                            st.write(block["text"])
                else:
                    st.json(result)
            else:
                st.error(f"HTTP {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to Bedrock in region '{region}'. Check the region.")
        except Exception as e:
            st.error(f"Error: {type(e).__name__}: {e}")
