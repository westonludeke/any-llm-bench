"""any-llm Bench - A side-by-side model comparator demo."""

import streamlit as st
import os
from dotenv import load_dotenv
from anybench.providers import enabled_models, has_any_provider, get_default_models
from anybench.tasks import get_available_tasks, get_task_description
from anybench.bench import run_comparison
from anybench.report import export_report

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="any-llm Bench",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = None


def main():
    """Main application interface."""
    
    st.title("🤖 any-llm Bench")
    st.caption("Compare LLM outputs side-by-side using any-llm")
    
    # Check if any providers are enabled
    has_providers = has_any_provider()
    available_models = enabled_models()
    
    # Show provider status
    if not has_providers:
        st.warning("⚠️ No API keys detected. Enable Mock Mode to try the demo.")
        st.info("💡 Add API keys to your `.env` file to use real models. See `env.example` for reference.")
        mock_mode = True
    else:
        st.success(f"✅ {len(available_models)} models available from enabled providers")
        mock_mode = False
    
    # Sidebar controls
    with st.sidebar:
        st.header("Configuration")
        
        # Model selection
        if has_providers:
            default_models = get_default_models()
            
            model1 = st.selectbox(
                "Model 1",
                available_models,
                index=0 if available_models else 0,
                help="First model to compare"
            )
            
            model2 = st.selectbox(
                "Model 2", 
                available_models,
                index=1 if len(available_models) > 1 else 0,
                help="Second model to compare"
            )
        else:
            model1 = st.selectbox("Model 1 (Mock)", ["mock:gpt-4o-mini", "mock:claude-3-haiku"])
            model2 = st.selectbox("Model 2 (Mock)", ["mock:claude-3-haiku", "mock:gpt-4o-mini"])
        
        # Task selection
        tasks = get_available_tasks()
        task = st.selectbox(
            "Task",
            tasks,
            help="Type of task to perform"
        )
        st.caption(get_task_description(task))
        
        # Mock mode toggle (only show if no providers)
        if not has_providers:
            mock_mode = st.checkbox("Enable Mock Mode", value=True, help="Use simulated responses for demo")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Input")
        
        # Initialize prompt in session state if not exists
        if "current_prompt" not in st.session_state:
            st.session_state.current_prompt = ""
        
        # Prompt input
        if task == "summarize":
            prompt = st.text_area(
                "Text to summarize",
                value=st.session_state.current_prompt,
                placeholder="Paste the text you want to summarize here...",
                height=200,
                key="prompt_input"
            )
        elif task == "extract_fields":
            prompt = st.text_area(
                "Text to extract fields from",
                value=st.session_state.current_prompt,
                placeholder="Paste text containing vendor, total, and date information...",
                height=200,
                key="prompt_input"
            )
        else:
            prompt = st.text_area(
                "Prompt",
                value=st.session_state.current_prompt,
                placeholder="Enter your prompt here...",
                height=200,
                key="prompt_input"
            )
        
        # Update session state with current prompt
        st.session_state.current_prompt = prompt
        
        # Run comparison button
        if st.button("🚀 Run Comparison", type="primary", disabled=not prompt.strip()):
            if not prompt.strip():
                st.error("Please enter a prompt")
            else:
                with st.spinner("Running comparison..."):
                    try:
                        st.session_state.results = run_comparison(
                            model1, model2, task, prompt, mock_mode
                        )
                        st.success("Comparison completed!")
                    except Exception as e:
                        st.error(f"Error running comparison: {str(e)}")
    
    with col2:
        st.header("Quick Actions")
        
        # Sample prompts
        st.subheader("Sample Prompts")
        
        if task == "summarize":
            sample_text = """The quarterly earnings report shows strong growth across all business segments. Revenue increased by 15% compared to the previous quarter, driven primarily by increased demand in the technology sector. The company's cloud services division saw the most significant growth, with a 25% increase in subscriptions. Operating expenses remained stable, resulting in improved profit margins. The management team is optimistic about continued growth in the next quarter and has announced plans to expand into new markets."""
            
        elif task == "extract_fields":
            sample_text = """Invoice #12345 from Acme Corp dated January 15, 2024 shows a total amount of $1,250.00 for consulting services rendered during December 2023. The invoice includes detailed line items for project management, technical analysis, and implementation support."""
            
        else:
            sample_text = "This is a sample prompt for testing purposes."
        
        if st.button("📝 Use Sample"):
            st.session_state.current_prompt = sample_text
            st.rerun()
    
    # Display results
    if st.session_state.results:
        st.header("Results")
        
        results = st.session_state.results
        result1 = results["model1"]
        result2 = results["model2"]
        
        # Metrics table
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"📊 {result1['model']}")
            
            # Status indicator
            if result1["ok"]:
                st.success("✅ Success")
            else:
                st.error(f"❌ Error: {result1.get('error', 'Unknown error')}")
            
            # Metrics
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Latency", f"{result1['latency_ms']} ms")
                if result1["tokens_in"]:
                    st.metric("Tokens In", result1["tokens_in"])
            with metrics_col2:
                if result1["tokens_out"]:
                    st.metric("Tokens Out", result1["tokens_out"])
                if result1["cost"]:
                    st.metric("Cost", result1["cost"])
            
            # Output
            with st.expander("View Output", expanded=True):
                st.text(result1["output"])
        
        with col2:
            st.subheader(f"📊 {result2['model']}")
            
            # Status indicator
            if result2["ok"]:
                st.success("✅ Success")
            else:
                st.error(f"❌ Error: {result2.get('error', 'Unknown error')}")
            
            # Metrics
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("Latency", f"{result2['latency_ms']} ms")
                if result2["tokens_in"]:
                    st.metric("Tokens In", result2["tokens_in"])
            with metrics_col2:
                if result2["tokens_out"]:
                    st.metric("Tokens Out", result2["tokens_out"])
                if result2["cost"]:
                    st.metric("Cost", result2["cost"])
            
            # Output
            with st.expander("View Output", expanded=True):
                st.text(result2["output"])
        
        # Export button
        st.header("Export")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("📄 Export Markdown"):
                try:
                    files = export_report(results)
                    st.success(f"✅ Report saved to `{files['markdown']}`")
                except Exception as e:
                    st.error(f"Error exporting report: {str(e)}")
        
        with col2:
            if st.button("📋 Export JSON"):
                try:
                    files = export_report(results)
                    st.success(f"✅ Report saved to `{files['json']}`")
                except Exception as e:
                    st.error(f"Error exporting report: {str(e)}")
        
        with col3:
            st.caption("Reports are saved in the `runs/` directory with timestamps")


if __name__ == "__main__":
    main()
