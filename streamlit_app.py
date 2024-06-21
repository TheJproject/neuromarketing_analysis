import streamlit as st
import requests

# Set the page configuration
st.set_page_config(page_title="Neuromarketing Analysis Demo", page_icon=":sparkles:", layout="centered", initial_sidebar_state="auto")

# Apply custom CSS for smaller image display
st.markdown(
    """
    <style>
        .upload-section {
            display: flex;
            align-items: center;
        }
        .upload-section > div {
            margin-right: 20px;
        }
        .small-image {
            width: 150px;
            height: auto;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to format JSON response
def format_json(response):
    color_map = {
        "ad_description": "#4CAF50",
        "ad_purpose": "#2196F3",
        "saliency_description": "#FF5722",
        "cognitive_description": "#FF9800"
    }
    
    html_content = "<div style='padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>"
    for key, value in response.items():
        color = color_map.get(key, "#000000")
        html_content += f"<h3 style='color: {color};'>{key.replace('_', ' ').title()}</h3>"
        html_content += f"<p>{value}</p>"
    html_content += "</div>"
    return html_content

# Set the title and description
st.title('Neuromarketing Analysis Demo')
st.markdown("""
Visualize customer attention instantly & optimize your ads before launch.
Improve campaign effectiveness and fine-tune ads based on industry, platform, and more.
""")

# File uploaders
col1, col2 = st.columns(2)
with col1:
    uploaded_image = st.file_uploader("Choose an image...", type="jpg")
    if uploaded_image is not None:
        st.image(uploaded_image, caption='Uploaded Image.', use_column_width=True)
with col2:
    uploaded_heatmap = st.file_uploader("Choose a heatmap...", type="jpg")
    if uploaded_heatmap is not None:
        st.image(uploaded_heatmap, caption='Uploaded Heatmap.', use_column_width=True)

# Analysis button
if st.button("Analyze"):
    if uploaded_image is not None and uploaded_heatmap is not None:
        with st.spinner('Uploading image and heatmap...'):
            files = {
                "image": uploaded_image.getvalue(),
                "heatmap": uploaded_heatmap.getvalue()
            }

        with st.spinner('Calling API to analyze image...'):
            try:
                response = requests.post("http://localhost:8000/analyze", files=files)
                response.raise_for_status()
                result = response.json()
                st.success('Analysis complete!')

                # Displaying the formatted JSON response
                st.markdown("## Analysis Results")
                html_content = format_json(result)
                st.markdown(html_content, unsafe_allow_html=True)
            except requests.exceptions.RequestException as e:
                st.error(f"Error in processing the image: {e}")
                st.write(e)
    else:
        st.error("Please upload both an image and a heatmap.")
