import json
import subprocess

import streamlit as st

st.set_page_config(page_title="Hot Melting Iron Dashboard", layout="wide")

st.title("🔥 Hot Melting Iron: AWS & Forgejo Monitor")
st.markdown("Real-time monitoring of your continuous deployment environment.")


# Function to check AWS CloudFormation stack status
def get_aws_stack_status(stack_name="HotIronInfrastructure"):
    try:
        # Use AWS CLI to get stack status, returning JSON
        result = subprocess.run(
            [
                "aws",
                "cloudformation",
                "describe-stacks",
                "--stack-name",
                stack_name,
                "--output",
                "json",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "Stacks" in data and len(data["Stacks"]) > 0:
                return data["Stacks"][0]["StackStatus"]
            return "UNKNOWN"
        else:
            # Check if it's a credentials error vs stack not found
            if (
                "NoCredentialsError" in result.stderr
                or "Unable to locate credentials" in result.stderr
            ):
                return "AUTH_REQUIRED"
            elif "does not exist" in result.stderr:
                return "NOT_DEPLOYED"
            return f"ERROR: {result.stderr.strip()}"
    except Exception as e:
        return f"EXCEPTION: {str(e)}"


# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌩️ AWS Infrastructure Status")
    status = get_aws_stack_status()

    if status.endswith("_COMPLETE") and "ROLLBACK" not in status:
        st.success(f"**Status:** {status}")
        st.metric(label="Stack State", value="Healthy")
    elif "IN_PROGRESS" in status:
        st.info(f"**Status:** {status}")
        st.metric(label="Stack State", value="Updating...")
    elif status in ["AUTH_REQUIRED", "NOT_DEPLOYED"]:
        st.warning(f"**Status:** {status}")
        st.metric(label="Stack State", value="Pending/Unconfigured")
    else:
        st.error(f"**Status:** {status}")
        st.metric(label="Stack State", value="Action Required")

    if st.button("Refresh Status"):
        st.rerun()

with col2:
    st.subheader("🛠️ Local System Health")
    st.write(
        "Use this dashboard to monitor the status of your Git sync, local scripts, and the AWS Free Tier."
    )
    st.markdown("""
    **Next Steps for MQL5 Bridge:**
    1. Ensure `MeltSignalExporter.mq5` is placed in MT5 `Experts/` directory.
    2. Start the local bridge script (`mql5_bridge.py`).
    3. Create PRs using `tea pr create`.
    4. Auto-merge to `main` to trigger the GitHub Action.
    """)
