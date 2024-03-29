import streamlit as st
from scipy.stats import norm
import numpy as np

def perform_ab_test(control_visitors, control_conversions, experiment_visitors, experiment_conversions, confidence_level=95):
    if control_visitors == 0 or experiment_visitors == 0:
        return "All input fields must be filled."
    
    z_alpha = norm.ppf(1 - (100 - confidence_level) / 200)  # z-score for the given confidence level
    p_control = control_conversions / control_visitors
    p_experiment = experiment_conversions / experiment_visitors
    pooled_p = (control_conversions + experiment_conversions) / (control_visitors + experiment_visitors)
    pooled_sd = np.sqrt(pooled_p * (1 - pooled_p) * (1 / control_visitors + 1 / experiment_visitors))
    z_stat = (p_control - p_experiment) / pooled_sd
    p_value = 2 * norm.cdf(-np.abs(z_stat))  # Two-tailed test
    if p_value < (1 - (100 - confidence_level) / 100):
        if p_control > p_experiment:
            return "Control Group is Better"
        else:
            return "Experiment Group is Better"
    else:
        return "Indeterminate"

def main():
    st.title("A/B Test Hypothesis Testing App")

    # User input
    control_visitors = st.number_input("Enter number of visitors in control group:")
    control_conversions = st.number_input("Enter number of conversions in control group:")
    experiment_visitors = st.number_input("Enter number of visitors in experiment group:")
    experiment_conversions = st.number_input("Enter number of conversions in experiment group:")
    confidence_level = st.slider("Select confidence level (%)", 1, 99, 95)

    # Perform A/B test
    ab_test_result = perform_ab_test(control_visitors, control_conversions, experiment_visitors, experiment_conversions, confidence_level)
    
    # Display result with color bar
    if ab_test_result == "Control Group is Better":
        color = "green"
    elif ab_test_result == "Experiment Group is Better":
        color = "blue"
    else:
        color = "red"

    st.subheader("A/B Test Result:")
    st.markdown(f'<p style="color:{color}; font-size:20px;">{ab_test_result}</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
