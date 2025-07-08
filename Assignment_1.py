import streamlit as st  # type: ignore


st.markdown(
    """
     <style>
     body {
       background-color: black;
       color: white;
    }
    .stApp {
       background: black;
       padding: 30px;
       border-radius: 15px;
       box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    h1{
       text-align: center;
       font-size: 36px;
       color: white;
    }
    .stButton button {
       background: black;
       color: #ffffff;
       font-size: 18px;
       padding: 10px 20px;
       border-radius: 10px;
       transition: 0.3s;
       box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }
    .stButton button:hover {
       transform: scale(1.05);
       color: #ffffff;      
    }
    .result-box{
       color: black;
       font-size: 20px;
       font-weight: bold;
       text-align: center;
       background-color: white;
       padding: 20px;
       border-radius: 10px;
       margin-top: 20px;
       box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);      
    }
    .footer{
       text-align: center;
       margin-top: 50px;
       font-size: 14px;
       color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1>🔄 Unit Converter using Python and Streamlit </h1>", unsafe_allow_html=True)
st.write("Easily convert between different units of length, weight, and temperature. 🌍")

conversion_type = st.sidebar.selectbox("Choose conversion type", ["Length", "Weight", "Temperature"])
value = st.number_input("Enter the value to convert", value=0.0, min_value=0.0, step=0.1)
col1, col2 = st.columns(2)

if conversion_type == "Length":
    with col1:
        from_unit = st.selectbox("From Unit", ["Meter", "Kilometer", "Centimeter", "Millimeter", "Miles", "Yards", "Inches", "Feet"])
    with col2:
        to_unit = st.selectbox("To Unit", ["Meter", "Kilometer", "Centimeter", "Millimeter", "Miles", "Yards", "Inches", "Feet"])

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From", ["Kilogram", "Gram", "Milligram", "Pounds", "Ounces"])
    with col2:
        to_unit = st.selectbox("To", ["Kilogram", "Gram", "Milligram", "Pounds", "Ounces"])

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])

def length_conversion(value, from_unit, to_unit):
    length_units = {
        'Meter': 1.0,
        'Kilometer': 1000.0,
        'Centimeter': 0.01,
        'Millimeter': 0.001,
        'Miles': 1609.344,
        'Yards': 0.9144,
        'Inches': 0.0254,
        'Feet': 0.3048,
    }
    return (value / length_units[from_unit]) * length_units[to_unit]

def weight_conversion(value, from_unit, to_unit):
    weight_units = {
        'Kilogram': 1.0,
        'Gram': 0.001,
        'Milligram': 0.000001,
        'Pounds': 0.45359237,
        'Ounces': 0.02834952,
    }
    return (value / weight_units[from_unit]) * weight_units[to_unit]

def temperature_conversion(value, from_unit, to_unit):
    if from_unit == "Celsius":
        return (value * 9/5) + 32 if to_unit == "Fahrenheit" else (value + 273.15 if to_unit == "Kelvin" else value)
    elif from_unit == "Fahrenheit":
        return ((value - 32) * 5/9) if to_unit == "Celsius" else (((value - 32) * 5/9) + 273.15 if to_unit == "Kelvin" else value)
    elif from_unit == "Kelvin":
        return (value - 273.15) if to_unit == "Celsius" else (((value - 273.15) * 9/5) + 32 if to_unit == "Fahrenheit" else value)
    return value

if st.button("🔄 Convert"):
    if conversion_type == "Length":
        result = length_conversion(value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = weight_conversion(value, from_unit, to_unit)
    elif conversion_type == "Temperature":
        result = temperature_conversion(value, from_unit, to_unit)

    st.markdown(f"<div class='result-box'> {value} {from_unit} = {result:.4f} {to_unit} ✅</div>", unsafe_allow_html=True)