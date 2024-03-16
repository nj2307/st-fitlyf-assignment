import streamlit as st
from scipy.stats import norm
import numpy as np

def perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level=95):
    if control_visitors == 0 or treatment_visitors == 0:
        return "Indeterminate (Zero visitors in one or both groups)"
    
    z_alpha = norm.ppf(1 - (100 - confidence_level) / 200)  # z-score for the given confidence level
    p_control = control_conversions / control_visitors
    p_treatment = treatment_conversions / treatment_visitors
    pooled_p = (control_conversions + treatment_conversions) / (control_visitors + treatment_visitors)
    pooled_sd = np.sqrt(pooled_p * (1 - pooled_p) * (1 / control_visitors + 1 / treatment_visitors))
    z_stat = (p_control - p_treatment) / pooled_sd
    p_value = 2 * norm.cdf(-np.abs(z_stat))  # Two-tailed test
    if p_value < (1 - (100 - confidence_level) / 100):
        if p_control > p_treatment:
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
    treatment_visitors = st.number_input("Enter number of visitors in treatment group:")
    treatment_conversions = st.number_input("Enter number of conversions in treatment group:")
    confidence_level = st.slider("Select confidence level (%)", 1, 99, 95)

    # Perform A/B test
    ab_test_result = perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
    
    # Display result
    st.subheader("A/B Test Result:")
    st.write(ab_test_result)

if __name__ == "__main__":
    main()
