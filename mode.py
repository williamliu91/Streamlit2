import streamlit as st
import os

# Path to the Streamlit config file
config_file_path = ".streamlit/config.toml"

# Function to read the current theme from the config file
def get_current_theme():
    try:
        with open(config_file_path, "r") as config_file:
            content = config_file.read()
            if 'base = "dark"' in content:
                return "Dark"
            else:
                return "Light"
    except FileNotFoundError:
        return "Light"  # Default to light mode if config file is not found

# Function to set the theme by writing to the config.toml file
def set_theme(theme_choice):
    with open(config_file_path, "w") as config_file:
        if theme_choice == 'Dark':
            config_file.write("""
            [theme]
            base = "dark"
            primaryColor = "#FF4B4B"
            backgroundColor = "#0E1117"
            secondaryBackgroundColor = "#262730"
            textColor = "#FFFFFF"
            """)
        else:
            config_file.write("""
            [theme]
            base = "light"
            primaryColor = "#FF4B4B"
            backgroundColor = "#FFFFFF"
            secondaryBackgroundColor = "#F0F2F6"
            textColor = "#000000"
            """)
    # Refresh the app to apply the new theme
    st.experimental_rerun()

# Read the current theme from the config file on startup
current_theme = get_current_theme()

# Create a checkbox for selecting dark mode or light mode
dark_mode_enabled = st.checkbox("Enable Dark Mode", value=(current_theme == "Dark"))

# Apply the selected theme and reload the app if the theme has changed
if dark_mode_enabled and current_theme != "Dark":
    set_theme("Dark")  # Set to dark mode and refresh
elif not dark_mode_enabled and current_theme != "Light":
    set_theme("Light")  # Set to light mode and refresh

# Add a refresh button for manual refresh
if st.button("Refresh Page"):
    st.experimental_rerun()  # Refresh the page when clicked

# Display the current theme
st.write(f"Current theme is: {current_theme}")

# Sidebar content
with st.sidebar:
    st.write("This is the sidebar content.")
=======
import streamlit as st
import os

# Path to the Streamlit config file
config_file_path = ".streamlit/config.toml"

# Function to read the current theme from the config file
def get_current_theme():
    try:
        with open(config_file_path, "r") as config_file:
            content = config_file.read()
            if 'base = "dark"' in content:
                return "Dark"
            else:
                return "Light"
    except FileNotFoundError:
        return "Light"  # Default to light mode if config file is not found

# Function to set the theme by writing to the config.toml file
def set_theme(theme_choice):
    with open(config_file_path, "w") as config_file:
        if theme_choice == 'Dark':
            config_file.write("""
            [theme]
            base = "dark"
            primaryColor = "#FF4B4B"
            backgroundColor = "#0E1117"
            secondaryBackgroundColor = "#262730"
            textColor = "#FFFFFF"
            """)
        else:
            config_file.write("""
            [theme]
            base = "light"
            primaryColor = "#FF4B4B"
            backgroundColor = "#FFFFFF"
            secondaryBackgroundColor = "#F0F2F6"
            textColor = "#000000"
            """)
    # Refresh the app to apply the new theme
    st.experimental_rerun()

# Read the current theme from the config file on startup
current_theme = get_current_theme()

# Create a checkbox for selecting dark mode or light mode
dark_mode_enabled = st.checkbox("Enable Dark Mode", value=(current_theme == "Dark"))

# Apply the selected theme and reload the app if the theme has changed
if dark_mode_enabled and current_theme != "Dark":
    set_theme("Dark")  # Set to dark mode and refresh
elif not dark_mode_enabled and current_theme != "Light":
    set_theme("Light")  # Set to light mode and refresh

# Add a refresh button for manual refresh
if st.button("Refresh Page"):
    st.experimental_rerun()  # Refresh the page when clicked

# Display the current theme
st.write(f"Current theme is: {current_theme}")

# Sidebar content
with st.sidebar:
    st.write("This is the sidebar content.")
>>>>>>> d7503ef00784db64417744e9e243d3feb4a79f94
