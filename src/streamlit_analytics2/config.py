import os
from pathlib import Path
import streamlit as st
import toml
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    "analytics": {
        "enabled": False,
        "tracking_id": "",
    },
    "storage": {
        "storage_type": "Json"
    }
}

def ensure_streamlit_dir():
    """Ensure .streamlit directory exists"""
    Path(".streamlit").mkdir(exist_ok=True)

def load_analytics_config():
    """Load analytics configuration with fallback to defaults"""
    path = os.path.join(os.getcwd(), ".streamlit/analytics.toml")
    logger.info(f"Loading configuration from: {path}")
    
    try:
        if not os.path.exists(path):
            logger.warning("Configuration file not found. Creating with defaults.")
            ensure_streamlit_dir()
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()

        with open(path, "r") as file:
            config = toml.load(file)
            
        # Check if file is empty or missing required sections
        if not config or "analytics" not in config:
            logger.warning("Invalid configuration found. Resetting to defaults.")
            save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG.copy()
            
        return config
        
    except Exception as e:
        logger.error(f"Error loading configuration: {str(e)}")
        st.error("Error loading configuration. Using defaults.")
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file"""
    path = os.path.join(os.getcwd(), ".streamlit/analytics.toml")
    try:
        ensure_streamlit_dir()
        with open(path, "w") as file:
            toml.dump(config, file)
        new_config = config
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving configuration: {str(e)}")
        st.error("Failed to save configuration")
        raise

def show_config():
    """Display and manage configuration"""
    st.title("Analytics Configuration")
    
    # Load current config
    config = load_analytics_config()
    
    # Configuration inputs
    enabled = st.checkbox("Enable Analytics", value=config["analytics"]["enabled"])
    tracking_id = st.text_input("Tracking ID", value=config["analytics"]["tracking_id"])
    storage_type = st.radio(
        "Storage type", 
        ["Json", "CSV"], 
        horizontal=True, 
        index=0 if config["storage"]["storage_type"] == "Json" else 1
    )
    
    # Create new config from inputs
    new_config = {
        "analytics": {
            "enabled": enabled,
            "tracking_id": tracking_id,
        },
        "storage": {
            "storage_type": storage_type
        }
    }
    
    st.subheader("Current Configuration")
    st.json(new_config)

    col1, col2 = st.columns(2)

    with col1:
        # Save button
        if st.button("Save Configuration", type="primary"):
            try:
                save_config(new_config)
                st.success("Configuration saved!")
            except Exception:
                st.error("Failed to save configuration. Please check logs.")

    
    with col2:
        # Reset to defaults button
        if st.button("↻ Reset to Defaults"):
            save_config(DEFAULT_CONFIG)
            st.success("Configuration reset to defaults!")
            new_config = DEFAULT_CONFIG
            st.rerun()
        
