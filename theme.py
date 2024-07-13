import streamlit as st
from streamlit_js_eval import streamlit_js_eval

# Custom CSS for different themes
theme_css = {
    "light": """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
        color: #000000;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    </style>
    """,
    "dark": """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #111111;
        color: #FFFFFF;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
        background-color: #111111;
    }
    </style>
    """,
    "blue": """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #007BFF;
        color: #FFFFFF;
    }
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stSidebar"] {
        background-color: #0056b3;
    }
    </style>
    """
}

def main():
    # Get the current theme from URL parameters
    current_theme = st.query_params.get("theme", "light")

    # Create a dropdown for theme selection
    selected_theme = st.selectbox(
        "Choose a theme:",
        list(theme_css.keys()),
        index=list(theme_css.keys()).index(current_theme)
    )

    # Check if the theme has changed
    if selected_theme != current_theme:
        # Update the URL parameter
        st.query_params["theme"] = selected_theme
        # Use streamlit-js-eval to refresh the page
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

    # Apply the selected theme CSS
    st.markdown(theme_css[selected_theme], unsafe_allow_html=True)

    # Add some content to the app
    st.title("Theme Changer App")
    st.write("This is a simple Streamlit app that allows you to change the theme.")
    st.write(f"Current theme: {selected_theme}")

if __name__ == "__main__":
    main()
