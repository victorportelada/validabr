import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Literal

import streamlit as st
from dotenv import load_dotenv

# Load `.env` file automatically so user doesn't have to inject variables in their terminal
load_dotenv()

# Config
st.set_page_config(page_title="pybrdoc Tracker", page_icon="🇧🇷", layout="wide")
PROJECT_ROOT = Path(__file__).parent.parent


def run_tests() -> str:
    """Runs pytest and captures output to parse basic metrics"""
    result = subprocess.run(
        ["uv", "run", "pytest", "--cov=src", "--cov-report=term"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    return result.stdout


def parse_roadmap() -> tuple[list[str], list[str]]:
    """Parses README.md for the Roadmap checklist"""
    readme_path = PROJECT_ROOT / "README.md"
    if not readme_path.exists():
        return [], []

    with open(readme_path, encoding="utf-8") as f:
        content = f.read()

    completed = re.findall(r"- \[x\] \*\*(.*?)\*\*", content)
    pending = re.findall(r"- \[ \] \*\*(.*?)\*\*", content)

    return completed, pending


st.title("🇧🇷 pybrdoc | Development Dashboard")
st.markdown("Live view of project progress, test status, coverage, and CI pipeline.")

with st.spinner("Running test suite & parsing project data..."):
    test_output = run_tests()
    completed, pending = parse_roadmap()

# Extract Coverage & Passing Tests
total_components = len(completed) + len(pending)
completion_pct = int((len(completed) / total_components) * 100) if total_components > 0 else 0

cov_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", test_output)
coverage_pct = cov_match.group(1) if cov_match else "0"

test_match = re.search(r"(\d+) passed", test_output)
tests_passed = test_match.group(1) if test_match else "0"


# Fetch GitHub CI Pipeline Status
def fetch_ci_status() -> tuple[str, Literal["normal", "inverse", "off"]]:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return "⚠️ Private Repo (Set GITHUB_TOKEN)", "off"
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/victorportelada/pybrdoc/actions/runs?per_page=1",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if not data.get("workflow_runs"):
                return "No runs found", "off"
            run = data["workflow_runs"][0]
            if run["status"] == "in_progress":
                return "🔄 Running", "normal"
            if run["conclusion"] == "success":
                return "✅ Passed", "normal"
            return f"❌ {run['conclusion'].title()}", "inverse"
    except Exception:
        return "❌ Auth/Network Error", "inverse"


ci_label, ci_delta = fetch_ci_status()

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Progress", f"{completion_pct}%", f"{len(completed)} / {total_components} Components")
col2.metric("Test Coverage", f"{coverage_pct}%", "Line Coverage")
col3.metric("Passing Tests", tests_passed, "Unit Tests")
col4.metric(
    "Remote Pipeline",
    ci_label,
    delta_color="off" if ci_delta == "off" else ("normal" if ci_delta == "normal" else "inverse"),
)


st.divider()

# Layout
left, right = st.columns([1, 1])

with left:
    st.subheader("🚀 Roadmap")
    if completed:
        st.success("Completed Modules")
        for item in completed:
            st.markdown(f"✅ {item}")

    if pending:
        st.warning("Pending Modules")
        for item in pending:
            st.markdown(f"⏳ {item}")

with right:
    st.subheader("🧪 Latest Local Output")
    with st.expander("Show Pytest Log", expanded=True):
        st.code(test_output, language="text")

st.info("Set `GITHUB_TOKEN=your_token` in a `.env` file to see live CI data.")
