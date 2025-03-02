import streamlit as st
import plotly.graph_objects as go
import numpy as np

# Constants for scaled-down distances and sizes (in AU and Earth radii)
PLANET_DATA = {
    "Sun": {"radius": 0.1, "distance": 0, "color": "yellow", "orbital_speed": 0},
    "Mercury": {"radius": 0.003, "distance": 0.39, "color": "gray", "orbital_speed": 47.87},
    "Venus": {"radius": 0.007, "distance": 0.72, "color": "orange", "orbital_speed": 35.02},
    "Earth": {"radius": 0.0075, "distance": 1.0, "color": "blue", "orbital_speed": 29.78},
    "Mars": {"radius": 0.004, "distance": 1.52, "color": "red", "orbital_speed": 24.077},
    "Jupiter": {"radius": 0.08, "distance": 5.20, "color": "brown", "orbital_speed": 13.07},
    "Saturn": {"radius": 0.07, "distance": 9.58, "color": "gold", "orbital_speed": 9.69},
    "Uranus": {"radius": 0.03, "distance": 19.22, "color": "lightblue", "orbital_speed": 6.81},
    "Neptune": {"radius": 0.03, "distance": 30.05, "color": "blue", "orbital_speed": 5.43},
}

def create_starfield(num_stars=1000):
    star_x = np.random.uniform(-50, 50, num_stars)
    star_y = np.random.uniform(-50, 50, num_stars)
    star_z = np.random.uniform(-50, 50, num_stars)
    return go.Scatter3d(
        x=star_x, y=star_y, z=star_z,
        mode="markers",
        marker=dict(size=1, color="white"),
        name="Stars"
    )

def create_solar_system(time, show_labels, speed):
    fig = go.Figure()
    fig.add_trace(create_starfield())
    for planet, data in PLANET_DATA.items():
        theta = time * data["orbital_speed"] * speed
        x = data["distance"] * np.cos(np.radians(theta))
        y = data["distance"] * np.sin(np.radians(theta))
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[0],
            mode="markers+text" if show_labels else "markers",
            marker=dict(size=data["radius"] * 100, color=data["color"]),
            text=[planet] if show_labels else [],
            textposition="top center",
            name=planet
        ))
    fig.update_layout(
        scene=dict(
            xaxis=dict(title="X (AU)", range=[-35, 35]),
            yaxis=dict(title="Y (AU)", range=[-35, 35]),
            zaxis=dict(title="Z (AU)", range=[-35, 35]),
            aspectmode="manual",
            aspectratio=dict(x=1, y=1, z=1),
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        showlegend=False,
    )
    return fig

def solar_system_page():
    st.title("🌌 Solar System Simulation")
    st.sidebar.header("Controls")
    show_labels = st.sidebar.checkbox("Show Planet Labels", value=True)
    speed = st.sidebar.slider("Orbit Speed", 0.1, 10.0, 1.0)
    time = st.sidebar.slider("Time (Years)", 0, 100, 0)
    fig = create_solar_system(time, show_labels, speed)
    st.plotly_chart(fig, use_container_width=True)

def chatbot_page():
    st.title("💬 Space Chatbot")
    st.write("Ask me anything about space!")

    # Embed the full Tawk.to chatbot page using an iframe
    tawk_iframe = """
    <iframe
        src="https://tawk.to/chat/YOUR_TAWKTO_WIDGET_ID/default"
        width="100%"
        height="600px"
        style="border: none;">
    </iframe>
    """
    st.components.v1.html(tawk_iframe, height=600)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Solar System Simulation", "Chatbot"])
    
    if page == "Solar System Simulation":
        solar_system_page()
    elif page == "Chatbot":
        chatbot_page()

if __name__ == "__main__":
    main()
