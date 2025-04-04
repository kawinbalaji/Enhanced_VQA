import streamlit as st


# Define function to display icons
def icon(icon_name, width=100):
    st.image(f"https://streamlit.io/components/icons/{icon_name}.png", width=width)


# Main Streamlit app
def main():
    st.title("Button Icons Example")

    st.write("Button with Icon:")
    icon("radio-button-on")
    st.button("Button with Icon")

    st.write("Different Icon Size:")
    icon("thumbs-up", width=50)
    st.button("Smaller Icon")

    icon("thumbs-down", width=150)
    st.button("Larger Icon")


if __name__ == "__main__":
    main()
