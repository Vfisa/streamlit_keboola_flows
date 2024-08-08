import streamlit as st
import requests

# Configuration bar with deployment URL selection
st.sidebar.header("Configuration")
token = st.sidebar.text_input("Token", type="password")

# Dictionary mapping user-friendly names to deployment URLs
deployment_urls = {
    "AWS-US-East": "https://connection.keboola.com/",
    "AWS-EU-Central": "https://connection.eu-central-1.keboola.com/",
    "Azure-EU-North": "https://connection.north-europe.azure.keboola.com/",
    "GCP-US-West": "https://connection.us-east4.gcp.keboola.com/",
    "GCP-EU-West": "https://connection.europe-west3.gcp.keboola.com/",
    "Custom": "Custom"
}

# Function to validate and adjust custom URL
def validate_custom_url(url):
    if url.startswith("http://"):
        url = "https://" + url[7:]
    elif not url.startswith("https://"):
        url = "https://" + url
    if not url.endswith("/"):
        url += "/"
    return url

# Dropdown for selecting a deployment
selected_option = st.sidebar.selectbox("Select Deployment", list(deployment_urls.keys()))

# If "Custom" is selected, allow the user to input a custom URL
if selected_option == "Custom":
    custom_url = st.sidebar.text_input("Specify Custom Deployment URL", "")
    if custom_url:
        custom_url = validate_custom_url(custom_url)
        deployment_url = custom_url
else:
    deployment_url = deployment_urls[selected_option]

if st.sidebar.button("Use this deployment"):
    st.session_state['deployment_url'] = deployment_url
    st.toast(f"Using Keboola URL: {deployment_url}", icon='🐙')

# Fetch selected deployment URL from session state
selected_deployment_url = st.session_state.get('deployment_url', '')

# Define headers for API requests using the token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

# Function to fetch flows data from Keboola API
def fetch_flows():
    response = requests.get(f'{selected_deployment_url}v2/storage/components/{{component_id}}/configs', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch flows data")
        return None

# Function to start a flow
def start_flow(flow_id):
    response = requests.post(f'{selected_deployment_url}v2/storage/jobs', json={"configId": flow_id}, headers=headers)
    if response.status_code == 202:
        st.success("Flow started successfully")
    else:
        st.error(f"Failed to start flow: {response.text}")

# Function to stop a flow
def stop_flow(flow_id):
    response = requests.delete(f'{selected_deployment_url}v2/storage/jobs/{flow_id}', headers=headers)
    if response.status_code == 200:
        st.success("Flow stopped successfully")
    else:
        st.error(f"Failed to stop flow: {response.text}")

# Main page with two tabs
tab1, tab2 = st.tabs(["Flows Overview", "Notification Management"])

with tab1:
    st.header("Flows Overview")
    
    # Fetch and display flows
    flows = fetch_flows()
    if flows:
        for flow in flows:
            st.subheader(flow['name'])
            st.text(f"Status: {flow['state']}")
            st.text(f"Last Run: {flow['lastRun']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f'Start {flow["name"]}'):
                    start_flow(flow['id'])
            with col2:
                if st.button(f'Stop {flow["name"]}'):
                    stop_flow(flow['id'])
    else:
        st.text("No flow information loaded.")

with tab2:
    st.header("Flow Notification Management")
    
    # Fetch and display notifications (placeholder code)
    notifications = [{"id": "1", "type": "Email", "status": "Active"}, {"id": "2", "type": "Slack", "status": "Inactive"}]  # Placeholder data
    for notification in notifications:
        st.subheader(notification['type'])
        st.text(f"Status: {notification['status']}")
        
        if st.button(f'Toggle Status for {notification["type"]}'):
            # Code to toggle notification status (replace with API call)
            st.write(f'Toggled {notification["type"]} status')
